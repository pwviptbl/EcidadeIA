from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from config import (
    AGENTE_ANSWER_LLM_MODEL,
    AGENTE_ANSWER_LLM_PROVIDER,
    AGENTE_PLANNER_LLM_MODEL,
    AGENTE_PLANNER_LLM_PROVIDER,
    AGENTE_STOP_AFTER_STAGE,
    AGENTE_VALIDATE_RESULTS,
    DEFAULT_LIMIT,
)
from services.catalog import Catalog
from services.logger import log_event
from services.llm_client import LLMClient, LLMError


@dataclass
class AgentResult:
    answer: str
    sql: str | None = None
    rows: list | None = None
    metadata: dict | None = None


class AgentPlanner:
    """
    Agente de consulta orientado por IA.

    O Python apenas orquestra:
    pergunta -> IA identifica assunto/tabelas -> API fornece catalogo/metadados
    -> IA monta SQL -> e-Cidade executa -> IA valida/ajusta ou responde.
    """

    MAX_ATTEMPTS = 5
    BUILD_ID = "planner-generic-rag-v1"

    def __init__(
        self,
        catalog: Catalog,
        client: Any,
        llm: LLMClient | None = None,
        planner_llm: LLMClient | None = None,
        answer_llm: LLMClient | None = None,
    ):
        self.catalog = catalog
        self.client = client
        self.planner_llm = planner_llm or llm or LLMClient(
            provider=AGENTE_PLANNER_LLM_PROVIDER,
            model=AGENTE_PLANNER_LLM_MODEL,
        )
        self.answer_llm = answer_llm or llm or LLMClient(
            provider=AGENTE_ANSWER_LLM_PROVIDER,
            model=AGENTE_ANSWER_LLM_MODEL,
        )
        self.llm = self.planner_llm

    def handle(self, message: str, history: list[dict] | None = None) -> AgentResult:
        question = message.strip()
        if not question:
            return AgentResult(answer="Pergunta vazia.")

        history = history or []

        try:
            log_event("handle.start", {"question": question})
            route = self._route_question(question, history)
            log_event("route.done", route)
            context = self._build_context(question, route, history)
            context["semantic_intent"] = self._detect_intent_from_catalog(question, context)
            log_event(
                "context.done",
                {
                    "tables": route.get("tables", []),
                    "context_bytes": len(json.dumps(context, ensure_ascii=False, default=str)),
                    "metadata_errors": context.get("metadata_errors", []),
                    "semantic_intent": context.get("semantic_intent", {}),
                },
            )
            log_event("route.rag_context", self._route_debug_payload(route, context))
            if AGENTE_STOP_AFTER_STAGE in ("route", "rag", "context"):
                return AgentResult(
                    answer=self._route_debug_answer(route, context),
                    metadata={
                        "stage": "context",
                        "route": route,
                        "context": self._route_debug_payload(route, context),
                    },
                )
            relationship_error = self._multi_table_relationship_error(context)
            if relationship_error:
                log_event("relationship.guard.blocked", relationship_error)
                return AgentResult(
                    answer=self._relationship_guard_answer(relationship_error),
                    metadata={
                        "error": "catalogo_insuficiente_para_join",
                        "relationship_guard": relationship_error,
                        "context": context,
                    },
                )
            sql_plan = self._deterministic_sql_plan(context) or self._create_sql(question, context)
            log_event("sql.plan", {"sql": sql_plan.get("sql"), "limit": sql_plan.get("limit"), "plan": sql_plan.get("plan")})
            return self._execute_and_validate(question, context, sql_plan)
        except LLMError as exc:
            log_event("llm.error", {"error": str(exc)})
            return AgentResult(
                answer=(
                    "Nao consegui acionar a IA para planejar a consulta.\n\n"
                    f"Erro: {exc}"
                ),
                metadata={"error": str(exc)},
            )
        except Exception as exc:
            log_event("agent.error", {"error": str(exc)})
            return AgentResult(
                answer=f"Falha no agente ao orquestrar a consulta: {exc}",
                metadata={"error": str(exc)},
            )

    def _route_question(self, question: str, history: list[dict]) -> dict:
        candidates = self._compact_search_results(self.catalog.search(question, limit=10))
        selected = self._validated_query_route(question, candidates)
        if not selected:
            selected = self._simple_count_route(question, candidates)
        if not selected:
            selected = self._select_tables_with_llm(question, candidates)
        tables = selected.get("tables") or []
        return {
            "reasoning": selected.get("reasoning") or "Tabelas candidatas selecionadas pela IA.",
            "domain": "ecidade",
            "tables": self._normalize_tables(tables),
            "candidate_tables": candidates,
            "needs_relationships": len(tables) > 1,
        }

    def _simple_count_route(self, question: str, candidates: list[dict]) -> dict | None:
        if not candidates:
            return None

        question_text = str(question or "").lower()
        asks_count = any(
            term in question_text
            for term in (
                "quantos",
                "quantas",
                "quanto",
                "quanta",
                "total de",
                "contar",
                "conte",
                "numero de",
                "número de",
            )
        )
        if not asks_count:
            return None

        first = candidates[0]
        table = str(first.get("table") or "").strip()
        if not table:
            return None

        first_score = int(first.get("score") or 0)
        second_score = int(candidates[1].get("score") or 0) if len(candidates) > 1 else 0
        table_name = table.split(".", 1)[-1].lower()
        description = str(first.get("description") or "").lower()
        query_terms = [
            term
            for term in re.findall(r"[a-z0-9_]+", question_text)
            if len(term) >= 4 and not term.isdigit()
        ]
        direct_match = any(term in table_name or term in description for term in query_terms)
        score_gap_ok = first_score >= second_score + 20 or first_score >= int(second_score * 1.2)
        has_markdown_evidence = any(
            str(evidence.get("kind") or "").startswith("markdown_")
            for evidence in (first.get("rag_evidence") or [])
            if isinstance(evidence, dict)
        )

        if not (direct_match or score_gap_ok or has_markdown_evidence):
            return None

        log_event(
            "route.simple_count_shortcut",
            {
                "table": table,
                "reason": "count_question_top_candidate",
                "score": first_score,
                "second_score": second_score,
            },
        )
        return {
            "tables": [table],
            "reasoning": "Tabela escolhida por atalho deterministico de contagem simples.",
        }

    def _validated_query_route(self, question: str, candidates: list[dict]) -> dict | None:
        if not candidates:
            return None

        first = candidates[0]
        table = str(first.get("table") or "").strip()
        if not table:
            return None

        evidences = [
            evidence for evidence in (first.get("rag_evidence") or [])
            if isinstance(evidence, dict) and evidence.get("kind") == "validated_query"
        ]
        if not evidences:
            return None

        question_text = str(question or "").lower()
        asks_sum = any(
            term in question_text
            for term in (
                "soma",
                "somar",
                "calcule a soma",
                "calcular a soma",
                "qual a soma",
                "qual e a soma",
                "qual é a soma",
            )
        )
        if not asks_sum:
            return None

        log_event(
            "route.validated_query_shortcut",
            {
                "table": table,
                "reason": "top_candidate_has_validated_query",
                "evidence": evidences[0].get("text"),
            },
        )
        return {
            "tables": [table],
            "reasoning": "Tabela escolhida por consulta validada aderente no catalogo/RAG.",
        }

    def _select_tables_with_llm(self, question: str, candidates: list[dict]) -> dict:
        if not candidates:
            raise LLMError("Catalogo/RAG nao retornou candidatos para a pergunta.")

        allowed_tables = {str(row.get("table")) for row in candidates if row.get("table")}
        user = {
            "task": (
                "Escolha a tabela ou tabelas candidatas relevantes para responder a pergunta. "
                "Responda somente JSON curto, sem raciocinio longo. "
                "Use apenas nomes de tabelas existentes em candidates. "
                "Nesta etapa decida o assunto e a fonte de dados; nao monte SQL. "
                "Priorize table e description. Score e rag_evidence sao apenas sinais auxiliares. "
                "Se uma tabela de score menor tiver descricao de negocio mais aderente, escolha ela."
            ),
            "question": question,
            "candidates": self._route_candidates_for_llm(candidates),
            "candidate_selection_rules": [
                "Compare semanticamente a pergunta com table e description antes de considerar o score.",
                "Se uma candidata tiver rag_evidence kind=validated_query aderente a pergunta, escolha essa tabela.",
                "Evidencias markdown_rule e markdown_sql vieram de documentacao humana; priorize essas evidencias sobre nome de coluna isolado.",
                "Se a pergunta pedir soma/valor, escolha a tabela que possui a medida/valor; tabela de historico/classificacao deve entrar apenas como apoio.",
                "Quando houver evidencia classification/filter_semantics, inclua a tabela principal e a tabela de classificacao necessaria.",
                "Nao escolha tabela operacional, configuracao, historico ou dominio auxiliar quando houver tabela principal de cadastro/fato.",
                "Nao escolha tabela so porque tem coluna numerica, data, municipio, codigo ou valor.",
                "Se a pergunta for de contagem simples, escolha a tabela que representa a entidade que esta sendo contada.",
                "Se a pergunta pedir atributo de outra entidade, selecione tambem a tabela de apoio.",
            ],
            "response_schema": {
                "tables": ["schema.tabela"],
                "reasoning": "motivo curto da escolha",
            },
        }
        try:
            result = self.planner_llm.json(
                self._routing_system_prompt(),
                "/no_think\n" + json.dumps(user, ensure_ascii=False),
                num_predict=80,
            )
            selected = [
                table
                for table in self._normalize_tables(result.get("tables") or [])
                if table in allowed_tables
            ]
            if selected:
                log_event("route.llm_selection", {"tables": selected, "reasoning": result.get("reasoning")})
                return {"tables": selected[:3], "reasoning": result.get("reasoning") or "Tabelas escolhidas pela IA."}
            log_event(
                "route.llm_selection.empty",
                {"raw_tables": result.get("tables"), "allowed_tables": sorted(allowed_tables)},
            )
            raise LLMError("IA nao selecionou nenhuma tabela valida para a pergunta.")
        except Exception as exc:
            log_event("route.llm_selection.error", {"error": str(exc)})
            if isinstance(exc, LLMError):
                raise
            raise LLMError(f"Falha na selecao de tabelas pela IA: {exc}") from exc

    def _fallback_candidate_tables(self, candidates: list[dict]) -> list[str]:
        if not candidates:
            return []

        first_score = int(candidates[0].get("score") or 0)
        second_score = int(candidates[1].get("score") or 0) if len(candidates) > 1 else 0
        if first_score and (
            first_score >= max(1, second_score * 2)
            or first_score >= second_score + 50
            or first_score >= int(second_score * 1.15)
        ):
            return [candidates[0]["table"]] if candidates[0].get("table") else []
        return [row["table"] for row in candidates[:3] if row.get("table")]

    def _fallback_single_candidate_table(self, candidates: list[dict]) -> list[str]:
        if not candidates:
            return []

        first = candidates[0]
        top_score = int(first.get("score") or 0)

        recommended = [
            row for row in candidates[:5]
            if row.get("table") and bool(row.get("recommended"))
        ]
        if recommended:
            best_recommended = max(recommended, key=lambda row: int(row.get("score") or 0))
            recommended_score = int(best_recommended.get("score") or 0)
            if (
                recommended_score >= max(1, int(top_score * 0.9))
                or recommended_score >= top_score - 10
            ):
                return [best_recommended["table"]]

        return [first["table"]] if first.get("table") else []

    def _has_clear_top_candidate(self, candidates: list[dict]) -> bool:
        if len(candidates) < 2:
            return bool(candidates)
        first_score = int(candidates[0].get("score") or 0)
        second_score = int(candidates[1].get("score") or 0)
        return bool(first_score and first_score >= max(1, second_score * 3))

    def _should_trust_catalog_ranking(self, question: str, candidates: list[dict]) -> bool:
        if not candidates:
            return False
        if len(candidates) > 1 and not self._has_clear_top_candidate(candidates):
            return False

        first = candidates[0]
        first_score = int(first.get("score") or 0)
        second_score = int(candidates[1].get("score") or 0) if len(candidates) > 1 else 0
        query_terms = set(re.findall(r"[a-z0-9_]+", str(question or "").lower()))
        table_name = str(first.get("table") or "").split(".", 1)[-1].lower()
        description = str(first.get("description") or "").lower()

        direct_match = any(term in table_name or term in description for term in query_terms if len(term) >= 4)
        strong_gap = first_score >= second_score * 3
        return bool(direct_match and strong_gap)

    def _forced_tables_for_question(self, question: str, candidates: list[dict]) -> list[str]:
        return []

    def _build_context(self, question: str, route: dict, history: list[dict]) -> dict:
        tables = route.get("tables", [])
        metadata_tables = []
        metadata_errors = []
        metadata_schemas = {}

        try:
            metadata_schemas = self.client.schemas()
        except Exception as exc:
            metadata_schemas = {"error": str(exc)}

        for full_name in tables[:3]:
            schema, table = self._split_table(full_name)
            try:
                metadata_tables.append(self._compact_table_metadata(self.client.table(schema, table)))
            except Exception as exc:
                metadata_errors.append({"table": full_name, "error": str(exc)})

        docs = []
        try:
            docs.extend(
                self.client.search_rag_docs(
                    question,
                    limit=12,
                    kinds=[
                        "business_rule",
                        "classification",
                        "filter_semantics",
                        "validated_query",
                        "grouping_rule",
                        "markdown_rule",
                        "markdown_sql",
                        "markdown_reference",
                    ],
                ).get("results", [])
            )
        except Exception:
            pass
        for term in (route.get("doc_terms") or [])[:5]:
            try:
                docs.extend(self.client.search_docs(str(term)).get("results", [])[:10])
            except Exception:
                continue

        selected_catalog = self._selected_catalog(tables)
        self._merge_catalog_metadata(selected_catalog, metadata_tables)
        expanded_tables = self._expand_context_from_catalog_rules(question, selected_catalog, metadata_tables, metadata_errors)

        relationships = {}
        if route.get("needs_relationships", True) or len(expanded_tables) > len(tables):
            try:
                relationships = self.client.relationships(expanded_tables)
            except Exception as exc:
                relationships = {"error": str(exc)}

        return {
            "question": question,
            "recent_history": self._compact_history(history),
            "route": route,
            "catalog": selected_catalog,
            "available_schemas": metadata_schemas,
            "metadata_tables": metadata_tables,
            "metadata_errors": metadata_errors,
            "relationships": self._filter_relationships(relationships, expanded_tables),
            "docs": docs[:30],
            "api_rules": {
                "endpoint": "POST /query/readonly",
                "allowed": "SELECT ou WITH read-only",
                "max_limit": DEFAULT_LIMIT,
                "schemas": self.catalog.schemas(),
                "important_validator_limitation": (
                    "Use schema.tabela em FROM/JOIN. Aliases declarados em FROM/JOIN sao permitidos. "
                    "CTEs declaradas no WITH podem ser referenciadas sem schema. "
                    "Use aliases ASCII, sem acentos. Nao aplique MAX/MIN diretamente em boolean."
                ),
            },
        }

    def _create_sql(self, question: str, context: dict, previous_error: dict | None = None) -> dict:
        system = self._system_prompt()
        sql_context = self._sql_context(context)
        user = {
            "task": "Monte apenas uma SQL PostgreSQL read-only para responder a pergunta. Responda JSON compacto.",
            "question": question,
            "context": sql_context,
            "previous_error": previous_error,
            "sql_compatibility_rules": [
                "Use somente tabelas e colunas listadas no contexto.",
                "Use schema.tabela em FROM/JOIN; aliases declarados em FROM/JOIN sao permitidos.",
                "CTEs declaradas no WITH podem ser referenciadas sem schema.",
                "Para contar registros, use count(1).",
                "Para comparacoes temporais com entity_key, compare a mesma entidade entre periodos.",
                "Quando o contexto trouxer classificacao_por_tipo, use a tabela de classificacao indicada antes de somar ou filtrar valores.",
                "SQL somente SELECT/WITH e aliases ASCII.",
            ],
            "response_schema": {
                "sql": "SQL SELECT/WITH sem ponto-e-virgula",
                "limit": DEFAULT_LIMIT
            },
        }
        result = self.planner_llm.json(system, json.dumps(user, ensure_ascii=False))
        log_event("llm.sql.raw", result)
        sql = self._extract_sql(result)
        result["sql"] = sql
        result["limit"] = self._safe_limit(result.get("limit"))
        if not sql:
            raise LLMError(f"IA nao retornou SQL em formato reconhecivel. Resposta: {self._compact_error_payload(result)}")
        semantic_errors = self._semantic_validate_sql(sql, context)
        if semantic_errors:
            raise LLMError("SQL nao passou na validacao semantica do catalogo: " + "; ".join(semantic_errors))
        return result

    def _execute_and_validate(self, question: str, context: dict, sql_plan: dict) -> AgentResult:
        attempts = []
        current_plan = sql_plan
        seen_sqls: set[str] = set()

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            sql = str(current_plan.get("sql") or "").strip().rstrip(";")
            limit = self._safe_limit(current_plan.get("limit"))
            execution = {"attempt": attempt, "sql": sql, "limit": limit}

            try:
                log_event("execute.attempt", {"attempt": attempt, "sql": sql, "limit": limit})
                if sql in seen_sqls:
                    raise RuntimeError("O agente repetiu a mesma SQL de uma tentativa anterior.")
                seen_sqls.add(sql)
                self._preflight_sql(sql)
                payload = self.client.readonly_query(sql, limit=limit)
                execution["payload"] = self._compact_payload(payload)
                log_event("execute.done", execution["payload"])
                if current_plan.get("template"):
                    validation = {
                        "status": "ok",
                        "reasoning": "Consulta gerada por template analitico validado pelo catalogo.",
                        "final_answer": "",
                    }
                elif not AGENTE_VALIDATE_RESULTS:
                    validation = {
                        "status": "ok",
                        "reasoning": "Consulta executada; validacao LLM pos-execucao desativada.",
                        "final_answer": "",
                    }
                else:
                    validation = self._validate_result(question, context, current_plan, payload, attempts)
            except Exception as exc:
                execution["error"] = str(exc)
                attempts.append(execution)
                log_event("execute.error", execution)
                if "repetiu a mesma SQL" in str(exc):
                    return AgentResult(
                        answer=self._failure_answer(question, attempts),
                        sql=sql,
                        metadata={"attempts": attempts, "context": context},
                    )
                if attempt >= self.MAX_ATTEMPTS:
                    return AgentResult(
                        answer=self._failure_answer(question, attempts),
                        sql=sql,
                        metadata={"attempts": attempts, "context": context},
                    )
                current_plan = self._create_sql(question, context, previous_error=execution)
                continue

            attempts.append(execution)
            if validation.get("status") == "retry" and attempt < self.MAX_ATTEMPTS:
                retry_sql = str(validation.get("retry_sql") or "").strip().rstrip(";")
                if retry_sql and retry_sql != sql:
                    current_plan = {
                        "plan": validation.get("plan") or current_plan.get("plan") or [],
                        "sql": retry_sql,
                        "limit": self._safe_limit(validation.get("limit")),
                    }
                    continue
                if payload.get("row_count", 0) > 0:
                    return AgentResult(
                        answer=self._explain_result(question, context, current_plan, payload),
                        sql=sql,
                        rows=payload.get("rows", []),
                        metadata={
                            "attempts": attempts,
                            "context": context,
                            "validation": validation,
                            "payload": self._compact_payload(payload),
                        },
                    )

            final_answer = self._final_answer_text(validation.get("final_answer"))
            if not final_answer:
                final_answer = self._deterministic_answer(question, context, current_plan, payload)
            if not final_answer:
                final_answer = self._explain_result(question, context, current_plan, payload)
            final_answer = self._guard_final_answer(final_answer, context)

            return AgentResult(
                answer=final_answer,
                sql=sql,
                rows=payload.get("rows", []),
                metadata={
                    "attempts": attempts,
                    "context": context,
                    "validation": validation,
                    "payload": self._compact_payload(payload),
                },
            )

        return AgentResult(
            answer=self._failure_answer(question, attempts),
            sql=str(current_plan.get("sql") or ""),
            metadata={"attempts": attempts, "context": context},
        )

    def _validate_result(self, question: str, context: dict, sql_plan: dict, payload: dict, attempts: list[dict]) -> dict:
        system = self._system_prompt()
        validation_context = self._validation_context(context)
        user = {
            "task": (
                "Verifique se o resultado da consulta responde a pergunta. "
                "Se nao responder, retorne retry_sql corrigido. "
                "Se responder, gere a mensagem final em pt-BR explicando os dados retornados. "
                "Nao responda apenas que a SQL esta correta ou aprovada. "
                "Se o resultado ja trouxer metricas suficientes para responder, prefira status ok. "
                "Nao peca refinamento opcional."
            ),
            "question": question,
            "context": validation_context,
            "sql_plan": sql_plan,
            "query_result": self._compact_payload(payload),
            "previous_attempts": attempts,
            "response_schema": {
                "status": "ok ou retry",
                "reasoning": "criterio de validacao",
                "retry_sql": "SQL PostgreSQL corrigido quando status=retry",
                "limit": DEFAULT_LIMIT,
                "final_answer": "resposta final quando status=ok",
            },
        }
        result = self.answer_llm.json(system, json.dumps(user, ensure_ascii=False))
        log_event("llm.validation.raw", result)
        if result.get("status") not in ("ok", "retry"):
            result["status"] = "ok"
        return result

    def _explain_result(self, question: str, context: dict, sql_plan: dict, payload: dict) -> str:
        system = self._system_prompt()
        user = {
            "task": (
                "Explique o resultado da consulta em pt-BR de forma objetiva. "
                "Use somente os dados retornados e o contexto do catalogo. "
                "Respeite rotulos, unidades, papeis semanticos e restricoes de metricas quando existirem no catalogo. "
                "Separe fatos observados de inferencias. "
                "Nao invente causas, regras de negocio ou eventos externos que nao estejam nos dados retornados. "
                "Se a consulta nao responder totalmente a pergunta, deixe isso explicito sem inventar dados. "
                "Nao proponha nova SQL."
            ),
            "question": question,
            "context": self._validation_context(context),
            "allowed_claims": [
                "Pode descrever totais, medias, contagens, rankings e variacoes presentes no resultado.",
                "Pode apontar possiveis fatores somente quando eles forem colunas ou metricas retornadas pela consulta.",
                "Deve informar limites da analise quando o resultado for amostra, ranking ou nao trouxer causa direta.",
            ],
            "forbidden_claims_without_data": self._forbidden_claims_without_data(),
            "sql_plan": {
                "sql": sql_plan.get("sql"),
                "limit": sql_plan.get("limit"),
            },
            "query_result": self._compact_payload(payload),
            "response_schema": {
                "final_answer": "resposta final em pt-BR",
            },
        }
        try:
            result = self.answer_llm.json(system, json.dumps(user, ensure_ascii=False))
            log_event("llm.answer.raw", result)
            final_answer = self._final_answer_text(result.get("final_answer"))
            if final_answer:
                return self._guard_final_answer(final_answer, context)
        except Exception as exc:
            log_event("llm.answer.error", {"error": str(exc)})
        return self._fallback_final_answer(sql_plan, payload)

    def _final_answer_text(self, value) -> str:
        if isinstance(value, dict):
            for key in ("final_answer", "answer", "message", "resposta"):
                text = self._final_answer_text(value.get(key))
                if text:
                    return text
            return ""
        if isinstance(value, list):
            return " ".join(filter(None, (self._final_answer_text(item) for item in value))).strip()

        text = str(value or "").strip()
        if not text:
            return ""

        lowered = text.lower()
        non_answers = [
            "consulta sql aprovada",
            "sql aprovada",
            "nenhuma correcao",
            "nenhuma correção",
            "nao ha necessidade de correcoes",
            "não há necessidade de correções",
            "consulta correta",
        ]
        if any(term in lowered for term in non_answers):
            return ""
        return text

    def _detect_intent_from_catalog(self, question: str, context: dict) -> dict:
        years = [int(year) for year in re.findall(r"\b(20\d{2})\b", str(question or "").lower())]
        question_text = str(question or "").lower()
        if any(
            term in question_text
            for term in (
                "quantos",
                "quantas",
                "quanto",
                "quanta",
                "total de",
                "contar",
                "conte",
                "numero de",
                "número de",
            )
        ):
            return {"intent": "count_records", "years": years, "source": "fallback"}
        return {"intent": "generic_sql", "years": years, "source": "fallback"}

    def _template_sql_plan(self, context: dict) -> dict | None:
        return None

    def _deterministic_sql_plan(self, context: dict) -> dict | None:
        plan = (
            self._template_sql_plan(context)
            or self._count_records_sql_plan(context)
        )
        if plan:
            log_event(
                "sql.deterministic_plan",
                {
                    "template": plan.get("template"),
                    "sql": plan.get("sql"),
                    "limit": plan.get("limit"),
                },
            )
        return plan

    def _template_debug_info(self, context: dict) -> dict:
        intent = context.get("semantic_intent", {})
        selected = context.get("catalog", {}).get("tables", {})
        table = self._select_template_table(context)
        return {
            "build_id": self.BUILD_ID,
            "intent": intent,
            "selected_tables": list(selected.keys()),
            "selected_table_has_template_shape": bool(table),
            "selected_table": table.get("table") if table else None,
            "selected_table_entity_key": table.get("entity_key") if table else None,
            "selected_table_time_key": table.get("time_key") if table else None,
            "inferred_metrics": [metric.get("expression") for metric in (self._select_variation_metrics(table) if table else [])],
        }

    def _count_records_sql_plan(self, context: dict) -> dict | None:
        if context.get("semantic_intent", {}).get("intent") != "count_records":
            return None

        selected = context.get("catalog", {}).get("tables", {})
        if len(selected) != 1:
            return None

        table_name = next(iter(selected.keys()))
        return {
            "sql": f"select count(1) as total_registros from {table_name}",
            "limit": 1,
            "template": "count_records",
        }

    def _count_filtered_sql_plan(self, context: dict) -> dict | None:
        return None

    def _select_template_table(self, context: dict) -> dict | None:
        selected = context.get("catalog", {}).get("tables", {})
        for full_name, table in selected.items():
            entity_key = table.get("entity_key") or self._infer_entity_keys(table)
            time_key = table.get("time_key") or self._infer_time_key(table)
            if entity_key and time_key:
                enriched = dict(table)
                enriched["table"] = full_name
                enriched["entity_key"] = entity_key
                enriched["time_key"] = time_key
                return enriched
        return None

    def _select_variation_metrics(self, table: dict | str) -> list[dict]:
        table_name = table["table"] if isinstance(table, dict) else str(table)
        metrics = []
        for name, metric in self.catalog.data.get("metrics", {}).items():
            if metric.get("table") != table_name:
                continue
            if not metric.get("explain_variation"):
                continue
            item = dict(metric)
            item["name"] = name
            metrics.append(item)
        if metrics:
            return metrics[:8]
        if isinstance(table, dict):
            return self._infer_variation_metrics_from_table(table)
        return self._infer_variation_metrics_from_table({"table": table_name, **(self.catalog.table(table_name) or {})})

    def _build_compare_periods_sql(self, table: dict, metrics: list[dict], period_a: int, period_b: int) -> str:
        table_name = table["table"]
        entity_key = table["entity_key"][0]
        time_key = table["time_key"]
        select_parts = ["count(1) as entidades_comparadas"]

        for metric in metrics:
            expression = metric["expression"]
            alias = self._safe_alias(metric["name"])
            select_parts.extend(
                [
                    f"avg(a.{expression}) as media_{period_a}_{alias}",
                    f"avg(b.{expression}) as media_{period_b}_{alias}",
                    f"avg(b.{expression} - a.{expression}) as media_delta_{alias}",
                    f"sum(b.{expression} - a.{expression}) as soma_delta_{alias}",
                ]
            )

        filters = [
            f"a.{time_key} = {period_a}",
            f"b.{time_key} = {period_b}",
        ]
        for template in table.get("default_filters", []):
            filters.append(str(template).format(alias="a"))
            filters.append(str(template).format(alias="b"))

        return (
            "select\n  "
            + ",\n  ".join(select_parts)
            + f"\nfrom {table_name} a\njoin {table_name} b\n  on b.{entity_key} = a.{entity_key}\nwhere "
            + "\n  and ".join(filters)
        )

    def _semantic_validate_sql(
        self,
        sql: str,
        context: dict,
        table: dict | None = None,
        metrics: list[dict] | None = None,
    ) -> list[str]:
        errors = []
        lowered = " ".join(str(sql or "").lower().split())
        intent = context.get("semantic_intent", {})
        table = table or self._select_template_table(context)
        metrics = metrics or self._metrics_for_sql(sql)

        if intent.get("intent") == "compare_periods" and table:
            entity_keys = table.get("entity_key", [])
            time_key = table.get("time_key")
            if table.get("comparison_strategy", intent.get("comparison_strategy")) == "same_entity":
                if " join " not in lowered:
                    errors.append("Comparacao entre periodos exige JOIN para comparar a mesma entidade.")
                for key in entity_keys:
                    if key.lower() not in lowered:
                        errors.append(f"Comparacao entre periodos exige entity_key {key}.")
            if time_key and time_key.lower() not in lowered:
                errors.append(f"Consulta nao usa time_key {time_key}.")

        for metric in metrics:
            metric_name = metric.get("name") or metric.get("expression")
            for forbidden in metric.get("forbidden_aliases", []):
                if re.search(rf"\bas\s+{re.escape(str(forbidden).lower())}\b", lowered):
                    errors.append(f"Alias proibido para metrica {metric_name}: {forbidden}.")

        if re.search(r"\blike\s+'%[^']*%'", lowered):
            errors.append("Nao use LIKE com padrao '%...%'; use position('texto' in lower(coluna)) > 0.")

        known_columns = {
            str(column).lower()
            for table_info in self._compact_context_tables(context)
            for column in (table_info.get("columns") or [])
        }
        for column_name in sorted(set(re.findall(r"\bj\d+_[a-z0-9_]+\b", lowered))):
            if known_columns and column_name not in known_columns:
                errors.append(f"Coluna nao listada no contexto: {column_name}.")

        return errors

    def _metrics_for_sql(self, sql: str) -> list[dict]:
        lowered = str(sql or "").lower()
        metrics = []
        for name, metric in self.catalog.data.get("metrics", {}).items():
            expression = str(metric.get("expression") or "").lower()
            if expression and re.search(rf"\b{re.escape(expression)}\b", lowered):
                item = dict(metric)
                item["name"] = name
                metrics.append(item)
        return metrics

    def _safe_alias(self, value: str) -> str:
        alias = re.sub(r"[^a-z0-9_]+", "_", str(value or "").lower()).strip("_")
        return alias or "metric"

    def _infer_time_key(self, table: dict) -> str | None:
        columns = table.get("columns", {}) or {}
        if isinstance(columns, dict):
            candidates = list(columns.keys())
        elif isinstance(columns, list):
            candidates = [str(name) for name in columns]
        else:
            candidates = []
        for name in candidates:
            lower = name.lower()
            if "anousu" in lower or re.search(r"(^|_)(ano|data)(_|$)", lower):
                return name
        for name in table.get("primary_key", []) or []:
            lower = str(name).lower()
            if "anousu" in lower or re.search(r"(^|_)(ano|data)(_|$)", lower):
                return str(name)
        return None

    def _infer_entity_keys(self, table: dict) -> list[str]:
        time_key = table.get("time_key") or self._infer_time_key(table)
        primary_key = [str(item) for item in (table.get("primary_key") or [])]
        entity_keys = [name for name in primary_key if name != time_key]
        if entity_keys:
            return entity_keys[:1]

        columns = table.get("columns", {}) or {}
        if isinstance(columns, dict):
            candidates = list(columns.keys())
        elif isinstance(columns, list):
            candidates = [str(name) for name in columns]
        else:
            candidates = []
        for name in candidates:
            lower = name.lower()
            if any(token in lower for token in ("matric", "codigo", "cgm", "id")) and name != time_key:
                return [name]
        return []

    def _infer_variation_metrics_from_table(self, table: dict) -> list[dict]:
        table_name = str(table.get("table") or "")
        columns = table.get("columns", {}) or {}
        if not isinstance(columns, dict):
            return []

        blocked_names = {"manual", "matric", "anousu", "gerafinanc", "tipocalculo", "tipoim"}
        blocked_prefixes = ("j01_",)
        metrics = []
        for name, info in columns.items():
            lower = str(name).lower()
            if any(token in lower for token in blocked_names):
                continue
            if lower.startswith(blocked_prefixes):
                continue
            col_type = str((info or {}).get("type") or "").lower()
            if col_type not in ("double precision", "numeric", "real", "integer", "bigint", "smallint"):
                continue
            metrics.append(
                {
                    "name": lower,
                    "label": (info or {}).get("description") or name,
                    "table": table_name,
                    "expression": name,
                    "unit": "BRL" if "vlr" in lower or "valor" in lower or "aliq" in lower else None,
                    "explain_variation": True,
                    "is_final_metric": False,
                    "effect_on_final_value": "decreases_when_increases" if "isen" in lower else "increases_when_increases",
                }
            )
        preferred = ["j23_vlrter", "j23_m2terr", "j23_arealo", "j23_areaed", "j23_aliq", "j23_vlrisen"]
        metrics.sort(
            key=lambda item: (
                preferred.index(item["expression"]) if item["expression"] in preferred else len(preferred),
                item["expression"],
            )
        )
        return metrics[:6]

    def _merge_catalog_metadata(self, selected_catalog: dict, metadata_tables: list[dict]) -> None:
        tables = selected_catalog.get("tables", {})
        for metadata in metadata_tables:
            if not isinstance(metadata, dict):
                continue
            table_name = metadata.get("table")
            catalog_info = metadata.get("catalog")
            if not table_name or table_name not in tables or not isinstance(catalog_info, dict):
                continue
            merged = dict(tables[table_name])
            for key in (
                "description",
                "primary_key",
                "grain",
                "entity_key",
                "time_key",
                "default_filters",
                "recommended",
                "columns",
                "blocked_columns",
                "foreign_keys",
                "business_logic",
                "filter_semantics",
                "type_classification",
                "recommended_groupings",
                "validated_queries",
                "business_notes",
            ):
                value = catalog_info.get(key)
                if value not in (None, "", [], {}):
                    merged[key] = value
            tables[table_name] = merged

    def _expand_context_from_catalog_rules(
        self,
        question: str,
        selected_catalog: dict,
        metadata_tables: list[dict],
        metadata_errors: list[dict],
    ) -> list[str]:
        tables = selected_catalog.get("tables", {})
        expanded = list(tables.keys())
        if not self._question_needs_type_classification(question):
            return expanded

        for source_table, table_info in list(tables.items()):
            classifications = table_info.get("type_classification") or {}
            if not isinstance(classifications, dict):
                continue
            for details in classifications.values():
                if not isinstance(details, dict):
                    continue
                reference = str(details.get("tabela_referencia") or details.get("reference_table") or "").strip()
                if not reference or reference in tables:
                    continue
                if reference not in self.catalog.compact_index().get("tables", {}):
                    continue
                schema, table = self._split_table(reference)
                try:
                    metadata = self._compact_table_metadata(self.client.table(schema, table))
                    metadata_tables.append(metadata)
                    selected_catalog["tables"][reference] = self.catalog.compact_index().get("tables", {}).get(reference, {})
                    self._merge_catalog_metadata(selected_catalog, [metadata])
                    expanded.append(reference)
                    log_event(
                        "context.expanded_by_catalog_rule",
                        {
                            "source_table": source_table,
                            "reference_table": reference,
                            "reason": "classificacao_por_tipo",
                        },
                    )
                except Exception as exc:
                    metadata_errors.append({"table": reference, "error": str(exc), "source_table": source_table})
        return expanded

    def _question_needs_type_classification(self, question: str) -> bool:
        lowered = str(question or "").lower()
        return any(
            token in lowered
            for token in (
                "hist",
                "historico",
                "histórico",
                "receita",
                "rec",
                "tipo",
                "composicao",
                "composição",
                "taxa",
                "valor",
                "soma",
            )
        )

    def _guard_final_answer(self, answer: str, context: dict) -> str:
        text = str(answer or "").strip()
        if not text:
            return text

        lower = text.lower()
        hits = [term for term in self._forbidden_claims_without_data() if term in lower]
        if not hits:
            return text

        observation = (
            "Observacao: causas externas como legislacao, inflacao, novos imoveis, "
            "crescimento economico ou valorizacao imobiliaria nao foram comprovadas pela consulta executada. "
            "A analise deve ser lida apenas com base nas metricas retornadas."
        )
        if observation.lower() in lower:
            return text
        return f"{text}\n\n{observation}"

    def _deterministic_answer(self, question: str, context: dict, sql_plan: dict, payload: dict) -> str:
        rows = payload.get("rows") or []
        first_row = rows[0] if rows and isinstance(rows[0], dict) else {}
        template = str(sql_plan.get("template") or "")

        if template == "count_records":
            value = first_row.get("total_registros")
            if value is None:
                return ""
            table_name = next(iter((context.get("catalog", {}).get("tables") or {}).keys()), "")
            table_info = (context.get("catalog", {}).get("tables") or {}).get(table_name, {})
            description = str(table_info.get("description") or "").strip()
            detail = f" ({description})" if description else ""
            return f"Temos {value} registros em {table_name}{detail}."

        return ""

    def _format_brl(self, value: Any) -> str:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return str(value)
        formatted = f"{number:,.2f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    def _forbidden_claims_without_data(self) -> list[str]:
        return [
            "crescimento economico",
            "crescimento econômico",
            "mudanca na legislacao",
            "mudança na legislação",
            "mudancas na legislacao",
            "mudanças na legislação",
            "novos imoveis",
            "novos imóveis",
            "inflacao",
            "inflação",
            "valorizacao imobiliaria",
            "valorização imobiliária",
        ]

    def _system_prompt(self) -> str:
        return """
Voce e um agente de dados read-only do e-Cidade.
Responda somente JSON valido no schema pedido.
Use apenas tabelas/campos do contexto.
SQL somente SELECT/WITH.
Dialeto obrigatorio: PostgreSQL.
Nao use funcoes ou sintaxe de MySQL como GROUP_CONCAT, SEPARATOR, IFNULL ou crases.
Use schema.tabela no FROM/JOIN. Aliases declarados em FROM/JOIN sao permitidos.
CTEs declaradas no WITH podem ser referenciadas sem schema.
Nao invente nomes de colunas.
Nao invente causas externas que nao estejam nos dados retornados.
""".strip()

    def _routing_system_prompt(self) -> str:
        return """
Voce e um roteador semantico de catalogo do e-Cidade.
Sua tarefa e escolher a fonte de dados correta para a pergunta.
Responda somente JSON valido no schema pedido.
Responda direto, sem cadeia de pensamento.
Nao monte SQL.
Use apenas tabelas existentes em candidates.
Priorize significado de negocio em table e description.
Score e rag_evidence sao auxiliares, nao decisao final.
""".strip()

    def _normalize_tables(self, tables: list) -> list[str]:
        normalized = []
        known = set(self.catalog.table_names())
        for item in tables:
            value = str(item or "").strip()
            if not value:
                continue
            if "." not in value:
                default_schema = self.catalog.default_schema()
                if not default_schema:
                    continue
                value = f"{default_schema}.{value}"
            if value in known and value not in normalized:
                normalized.append(value)
        return normalized

    def _split_table(self, full_name: str) -> tuple[str, str]:
        parts = full_name.split(".", 1)
        if len(parts) == 1:
            return self.catalog.default_schema() or "", parts[0]
        return parts[0], parts[1]

    def _candidate_schemas(self, route: dict, tables: list[str]) -> list[str]:
        allowed = set(self.catalog.schemas())
        candidates = []

        for schema in route.get("schemas") or []:
            schema = str(schema or "").strip()
            if schema in allowed and schema not in candidates:
                candidates.append(schema)

        for table in tables:
            schema, _ = self._split_table(table)
            if schema in allowed and schema not in candidates:
                candidates.append(schema)

        if not candidates:
            candidates = self.catalog.schemas()

        return candidates

    def _filter_relationships(self, relationships: dict, tables: list[str]) -> dict:
        if not isinstance(relationships, dict) or relationships.get("error"):
            return relationships

        selected_full = {str(table) for table in tables}
        table_names = {self._split_table(table)[1] for table in tables}
        filtered = {}
        for key in ("relationships", "foreign_keys", "heuristics"):
            rows = relationships.get(key, [])
            filtered[key] = [
                row for row in rows
                if self._relationship_mentions_any_selected_table(row, selected_full, table_names)
            ][:80]
        return filtered

    def _multi_table_relationship_error(self, context: dict) -> dict | None:
        tables = context.get("route", {}).get("tables", []) or []
        if len(tables) <= 1:
            return None

        relationships = context.get("relationships", {})
        if not isinstance(relationships, dict) or relationships.get("error"):
            return {
                "tables": tables,
                "reason": "Nao foi possivel consultar relacionamentos do catalogo.",
                "relationships": relationships,
            }

        relationship_rows = relationships.get("relationships") or []
        foreign_keys = relationships.get("foreign_keys") or []
        heuristics = relationships.get("heuristics") or []
        usable = [
            row
            for row in [*relationship_rows, *foreign_keys, *heuristics]
            if isinstance(row, dict) and self._relationship_connects_selected_tables(row, tables)
        ]
        if usable:
            return None

        catalog_rule = self._catalog_rule_connects_selected_tables(context, tables)
        if catalog_rule:
            log_event("relationship.guard.catalog_rule", catalog_rule)
            return None

        return {
            "tables": tables,
            "reason": "A IA selecionou mais de uma tabela, mas o catalogo nao trouxe relacionamento claro entre elas.",
            "relationships": relationship_rows[:10],
            "foreign_keys": foreign_keys[:10],
            "heuristics": heuristics[:10],
        }

    def _relationship_mentions_any_selected_table(
        self,
        relationship: dict,
        selected_full: set[str],
        selected_names: set[str],
    ) -> bool:
        if not isinstance(relationship, dict):
            return False
        values = {
            str(relationship.get("source") or ""),
            str(relationship.get("target") or ""),
            str(relationship.get("source_table") or ""),
            str(relationship.get("target_table") or ""),
            str(relationship.get("table") or ""),
            str(relationship.get("references") or ""),
        }
        leaves = {value.split(".", 1)[-1] for value in values if value}
        return bool(selected_full.intersection(values) or selected_names.intersection(values) or selected_names.intersection(leaves))

    def _catalog_rule_connects_selected_tables(self, context: dict, tables: list[str]) -> dict | None:
        selected = {str(table) for table in tables}
        catalog_tables = context.get("catalog", {}).get("tables", {})
        if not isinstance(catalog_tables, dict):
            return None

        for source_table, table_info in catalog_tables.items():
            if source_table not in selected or not isinstance(table_info, dict):
                continue
            classifications = table_info.get("type_classification") or {}
            if not isinstance(classifications, dict):
                continue
            for rule_name, details in classifications.items():
                if not isinstance(details, dict):
                    continue
                reference_table = str(
                    details.get("tabela_referencia")
                    or details.get("reference_table")
                    or details.get("target_table")
                    or ""
                ).strip()
                if not reference_table or reference_table not in selected:
                    continue
                return {
                    "source_table": source_table,
                    "reference_table": reference_table,
                    "rule": rule_name,
                    "reason": "type_classification",
                    "source_column": details.get("coluna_origem") or details.get("source_column"),
                    "reference_column": details.get("coluna_referencia") or details.get("reference_column"),
                }
        return None

    def _relationship_connects_selected_tables(self, relationship: dict, tables: list[str]) -> bool:
        selected_full = {str(table) for table in tables}
        selected_names = {self._split_table(table)[1] for table in tables}
        values = {
            str(relationship.get("source") or ""),
            str(relationship.get("target") or ""),
            str(relationship.get("source_table") or ""),
            str(relationship.get("target_table") or ""),
            str(relationship.get("table") or ""),
            str(relationship.get("references") or ""),
        }
        hits = selected_full.intersection(values)
        hits.update(selected_names.intersection(values))
        if len(hits) >= 2:
            return True

        source = str(relationship.get("source_table") or relationship.get("table") or "")
        target = str(relationship.get("target_table") or relationship.get("references") or "")
        target_leaf = target.split(".", 1)[-1] if target else ""
        return source in selected_names and target_leaf in selected_names

    def _relationship_guard_answer(self, error: dict) -> str:
        tables = ", ".join(error.get("tables") or [])
        reason = error.get("reason") or "Relacionamento ausente no catalogo."
        return (
            "Catalogo insuficiente para montar join seguro.\n\n"
            f"Tabelas selecionadas: {tables}\n"
            f"Motivo: {reason}\n\n"
            "Nao vou inventar relacionamento entre tabelas. Enriqueca o catalogo com a chave estrangeira "
            "ou relacionamento correto e gere o RAG novamente."
        )

    def _safe_limit(self, value) -> int:
        try:
            limit = int(value or DEFAULT_LIMIT)
        except (TypeError, ValueError):
            limit = DEFAULT_LIMIT
        return max(1, min(limit, DEFAULT_LIMIT))

    def _preflight_sql(self, sql: str):
        try:
            sql.encode("ascii")
        except UnicodeEncodeError as exc:
            raise RuntimeError(
                "SQL contem caracteres nao ASCII. Reescreva aliases sem acentos, usando apenas letras, numeros e underscore."
            ) from exc
        if re.search(r"\bcampo_[a-z0-9_]*\b", sql, flags=re.I):
            raise RuntimeError("SQL contem placeholder generico campo_*. Use somente colunas reais do contexto.")
        if re.search(r"\b(group_concat|separator|ifnull)\b", sql, flags=re.I) or "`" in sql:
            raise RuntimeError("SQL usa sintaxe/funcoes fora do dialeto PostgreSQL.")
        cte_names = self._cte_names(sql)
        # Evita falso positivo com sintaxe como EXTRACT(YEAR FROM coluna).
        table_scan_sql = re.sub(
            r"\bextract\s*\(\s*[^)]*\bfrom\b\s+[a-z_][a-z0-9_]*\s*\)",
            "extract(...)",
            sql,
            flags=re.I,
        )
        for table_ref in re.finditer(r"\b(from|join)\s+([a-z_][a-z0-9_]*)(?!\s*\.)\b", table_scan_sql, flags=re.I):
            table_name = table_ref.group(2)
            if table_name.lower() not in ("select",) and table_name.lower() not in cte_names:
                raise RuntimeError(
                    f"Tabela sem schema no SQL: {table_name}. Use schema.tabela conforme o contexto."
                )

    def _cte_names(self, sql: str) -> set[str]:
        text = str(sql or "")
        if not re.match(r"^\s*with\b", text, flags=re.I):
            return set()
        return {
            match.group(1).lower()
            for match in re.finditer(
                r"(?:\bwith\b|,)\s+(?:recursive\s+)?([a-z_][a-z0-9_]*)\s+as\s*\(",
                text,
                flags=re.I,
            )
        }

    def _compact_payload(self, payload: dict) -> dict:
        rows = payload.get("rows", [])
        return {
            "sql": payload.get("sql"),
            "limit": payload.get("limit"),
            "row_count": payload.get("row_count", len(rows)),
            "duration_ms": payload.get("duration_ms"),
            "rows_sample": rows[:8],
        }

    def _sql_context(self, context: dict) -> dict:
        return {
            "tables": self._compact_context_tables(context),
            "semantic_intent": context.get("semantic_intent", {}),
            "metrics": self._compact_metrics(),
            "templates": self.catalog.data.get("templates", {}),
            "relationships": context.get("relationships", {}),
            "business_rules": self._compact_rag_rules(context),
            "max_limit": DEFAULT_LIMIT,
        }

    def _validation_context(self, context: dict) -> dict:
        return {
            "tables": [
                {
                    "table": table.get("table"),
                    "description": table.get("description"),
                    "entity_key": table.get("entity_key", []),
                    "time_key": table.get("time_key"),
                }
                for table in self._compact_context_tables(context)
            ],
            "semantic_intent": context.get("semantic_intent", {}),
            "metrics": self._compact_metrics(),
        }

    def _compact_context_tables(self, context: dict) -> list[dict]:
        selected = context.get("catalog", {}).get("tables", {})
        metadata_by_table = {
            item.get("table"): item
            for item in context.get("metadata_tables", [])
            if isinstance(item, dict) and item.get("table")
        }
        tables = []
        for full_name, info in selected.items():
            metadata = metadata_by_table.get(full_name, {})
            columns = []
            for column in metadata.get("columns", [])[:18]:
                name = column.get("column_name")
                if name:
                    columns.append(name)
            if not columns:
                columns = (info.get("columns") or [])[:18]
            tables.append(
                {
                    "table": full_name,
                    "description": info.get("description"),
                    "primary_key": info.get("primary_key", []),
                    "grain": info.get("grain", []),
                    "entity_key": info.get("entity_key", []),
                    "time_key": info.get("time_key"),
                    "default_filters": info.get("default_filters", []),
                    "business_logic": info.get("business_logic", []),
                    "filter_semantics": info.get("filter_semantics", {}),
                    "type_classification": info.get("type_classification", {}),
                    "recommended_groupings": info.get("recommended_groupings", []),
                    "validated_queries": info.get("validated_queries", []),
                    "business_notes": info.get("business_notes", []),
                    "foreign_keys": info.get("foreign_keys", []),
                    "columns": columns,
                }
            )
        return tables

    def _compact_rag_rules(self, context: dict) -> list[dict]:
        selected_tables = set((context.get("catalog") or {}).get("tables", {}).keys())
        compact = []
        seen = set()
        for doc in context.get("docs", []) or []:
            if not isinstance(doc, dict):
                continue
            metadata = doc.get("metadata") or {}
            table = metadata.get("table")
            kind = doc.get("kind")
            if selected_tables and table and table not in selected_tables:
                continue
            if kind not in {
                "business_rule",
                "classification",
                "filter_semantics",
                "validated_query",
                "grouping_rule",
                "markdown_rule",
                "markdown_sql",
                "markdown_reference",
            }:
                continue
            key = (kind, table, doc.get("id"))
            if key in seen:
                continue
            seen.add(key)
            compact.append(
                {
                    "kind": kind,
                    "table": table,
                    "score": doc.get("score"),
                    "text": str(doc.get("text") or "")[:900],
                    "metadata": {
                        name: metadata.get(name)
                        for name in ("classification", "reference_table", "filter", "question", "rule_type", "section", "source_file")
                        if metadata.get(name) not in (None, "", [], {})
                    },
                }
            )
            if len(compact) >= 12:
                break
        return compact

    def _compact_metrics(self) -> dict:
        compact = {}
        for name, metric in self.catalog.data.get("metrics", {}).items():
            compact[name] = {
                "label": metric.get("label"),
                "table": metric.get("table"),
                "expression": metric.get("expression"),
                "unit": metric.get("unit"),
                "explain_variation": bool(metric.get("explain_variation")),
                "is_final_metric": metric.get("is_final_metric"),
                "effect_on_final_value": metric.get("effect_on_final_value"),
                "forbidden_aliases": metric.get("forbidden_aliases", []),
            }
        return compact

    def _extract_sql(self, result: dict) -> str:
        candidates = [
            result.get("sql"),
            result.get("query"),
            result.get("consulta"),
            result.get("consulta_sql"),
            result.get("sql_query"),
            result.get("statement"),
        ]
        for candidate in candidates:
            sql = self._clean_sql_candidate(candidate)
            if sql:
                return sql

        for value in self._walk_values(result):
            sql = self._clean_sql_candidate(value)
            if sql:
                return sql
        return ""

    def _walk_values(self, value):
        if isinstance(value, dict):
            for item in value.values():
                yield from self._walk_values(item)
        elif isinstance(value, list):
            for item in value:
                yield from self._walk_values(item)
        else:
            yield value

    def _clean_sql_candidate(self, value) -> str:
        text = str(value or "").strip()
        if not text:
            return ""
        if "```" in text:
            match = re.search(r"```(?:sql)?\s*([\s\S]*?)```", text, flags=re.I)
            if match:
                text = match.group(1).strip()
        match = re.search(r"\b(with|select)\b[\s\S]*", text, flags=re.I)
        if match:
            text = match.group(0).strip()
        text = text.strip().rstrip(";").strip()
        if re.match(r"^(select|with)\b", text, flags=re.I):
            return text
        return ""

    def _compact_error_payload(self, payload: dict) -> str:
        text = json.dumps(payload, ensure_ascii=False, default=str)
        return text[:1200]

    def _compact_table_metadata(self, metadata: dict) -> dict:
        if not isinstance(metadata, dict):
            return {}
        columns = metadata.get("columns", [])
        compact_columns = []
        for column in columns[:25]:
            if not isinstance(column, dict):
                continue
            compact_columns.append(
                {
                    "column_name": column.get("column_name"),
                    "data_type": column.get("data_type"),
                    "is_nullable": column.get("is_nullable"),
                }
            )
        return {
            "table": metadata.get("table"),
            "catalog": metadata.get("catalog", {}),
            "columns": compact_columns,
        }

    def _compact_search_results(self, rows: list[dict]) -> list[dict]:
        compact = []
        for row in rows[:20]:
            columns = row.get("columns", {})
            if isinstance(columns, dict):
                column_names = list(columns.keys())[:15]
            elif isinstance(columns, list):
                column_names = columns[:15]
            else:
                column_names = []
            compact.append(
                {
                    "table": row.get("table"),
                    "description": row.get("description"),
                    "columns": column_names,
                    "grain": row.get("grain", []),
                    "entity_key": row.get("entity_key", []),
                    "time_key": row.get("time_key"),
                    "recommended": bool(row.get("recommended")),
                    "score": row.get("score"),
                    "rag_evidence": row.get("rag_evidence", [])[:5],
                }
            )
        return compact

    def _route_debug_payload(self, route: dict, context: dict) -> dict:
        return {
            "selected_tables": route.get("tables", []),
            "reasoning": route.get("reasoning"),
            "candidate_tables": [
                {
                    "table": item.get("table"),
                    "description": item.get("description"),
                    "score": item.get("score"),
                    "entity_key": item.get("entity_key", []),
                    "time_key": item.get("time_key"),
                    "rag_evidence": item.get("rag_evidence", []),
                }
                for item in (route.get("candidate_tables") or [])[:10]
            ],
            "semantic_intent": context.get("semantic_intent", {}),
            "catalog_tables": list((context.get("catalog", {}) or {}).get("tables", {}).keys()),
        }

    def _route_debug_answer(self, route: dict, context: dict) -> str:
        lines = [
            "Execucao interrompida apos o contexto do RAG/roteamento.",
            f"Tabelas selecionadas: {', '.join(route.get('tables', [])) or 'nenhuma'}",
            f"Motivo: {route.get('reasoning') or 'sem justificativa'}",
            "",
            "Candidatos do RAG/catalogo:",
        ]
        for item in (route.get("candidate_tables") or [])[:10]:
            evidence = item.get("rag_evidence", [])[:3]
            evidence_text = ", ".join(
                f"{entry.get('kind')}:{entry.get('column') or entry.get('metric') or '-'}:{entry.get('score')}"
                for entry in evidence
            ) or "sem evidencia"
            lines.append(
                f"- {item.get('table')} | score={item.get('score')} | entity_key={item.get('entity_key', [])} | time_key={item.get('time_key')} | evidencia={evidence_text}"
            )
        lines.extend(
            [
                "",
                f"Intent detectada: {context.get('semantic_intent', {}).get('intent')}",
                f"Anos detectados: {context.get('semantic_intent', {}).get('years', [])}",
            ]
        )
        return "\n".join(lines)

    def _route_candidates_for_llm(self, candidates: list[dict]) -> list[dict]:
        return [
            {
                "table": row.get("table"),
                "description": row.get("description"),
                "recommended": bool(row.get("recommended")),
                "score": row.get("score"),
                "rag_evidence": [
                    {
                        "kind": item.get("kind"),
                        "score": item.get("score"),
                        "text": str(item.get("text") or "")[:600],
                    }
                    for item in (row.get("rag_evidence") or [])[:3]
                ],
            }
            for row in candidates[:15]
        ]

    def _selected_catalog(self, tables: list[str]) -> dict:
        selected = {}
        source = self.catalog.compact_index().get("tables", {})
        for table in tables:
            if table in source:
                selected[table] = source[table]
        return {
            "schemas": self.catalog.schemas(),
            "tables": selected,
            "intents": self.catalog.data.get("intents", {}),
            "metrics": self.catalog.data.get("metrics", {}),
            "templates": self.catalog.data.get("templates", {}),
        }

    def _compact_history(self, history: list[dict]) -> list[dict]:
        compact = []
        for item in history[-8:]:
            role = str(item.get("role") or "").strip()
            content = " ".join(str(item.get("content") or "").split())
            if not role or not content:
                continue
            compact.append({"role": role, "content": content[:1200]})
        return compact

    def _fallback_final_answer(self, sql_plan: dict, payload: dict) -> str:
        return (
            "Consulta executada, mas a IA nao retornou uma mensagem final estruturada.\n\n"
            f"Linhas retornadas: {payload.get('row_count', len(payload.get('rows', [])))}\n\n"
            f"SQL usado:\n```sql\n{sql_plan.get('sql')}\n```"
        )

    def _failure_answer(self, question: str, attempts: list[dict]) -> str:
        lines = [
            "Nao consegui chegar a uma consulta valida depois das tentativas do agente.",
            f"Pergunta: {question}",
            "",
            "Tentativas:",
        ]
        for attempt in attempts:
            lines.append(f"- Tentativa {attempt.get('attempt')}: {attempt.get('error') or 'sem resposta valida'}")
            if attempt.get("sql"):
                lines.append(f"```sql\n{attempt.get('sql')}\n```")
        return "\n".join(lines)
