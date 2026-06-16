from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agente_v2.stages.business_resolver import BusinessResolver
from agente_v2.stages.answer_synthesizer import AnswerSynthesizer
from agente_v2.stages.executor import Executor
from agente_v2.stages.schema_planner import SchemaPlanner
from agente_v2.contracts.models import SqlArtifact
from agente_v2.stages.sql_compiler import SqlCompiler
from agente_v2.stages.sql_critic import SqlCritic


FIXTURES = ROOT / "tests" / "fixtures"


class ContractNormalizationTest(unittest.TestCase):
    def test_business_resolver_normalizes_filters_without_sql_condition(self) -> None:
        resolver = BusinessResolver(None)  # type: ignore[arg-type]
        raw = {
            "metrics": [
                {
                    "metric_name": "Valor Total",
                    "aggregation": "sum",
                    "column": "fin.mov.valor",
                }
            ],
            "filters": [
                {
                    "filter_name": "Situacao Ativa",
                    "table": "dim.entidade",
                    "column": "status",
                    "condition": "= 'ATIVA'",
                },
                {
                    "filter_name": "Exercicio",
                    "table": "fin.mov",
                    "column": "ano",
                    "condition": "IN ('2025', '2026')",
                },
            ],
            "dimensions": [
                {
                    "dimension_name": "Exercicio",
                    "column": "fin.mov.ano",
                }
            ],
        }
        out = resolver._sanitize(raw)
        self.assertEqual(out["metrics"][0]["table"], "fin.mov")
        self.assertEqual(out["metrics"][0]["column"], "valor")
        self.assertEqual(out["filters"][0]["operator"], "=")
        self.assertEqual(out["filters"][0]["value"], "ATIVA")
        self.assertEqual(out["filters"][1]["operator"], "IN")
        self.assertEqual(out["filters"][1]["value"], ["2025", "2026"])
        self.assertNotIn("condition", out["filters"][0])
        self.assertNotIn("condition", out["filters"][1])

    def test_schema_planner_normalizes_grain_joins_and_filters(self) -> None:
        planner = SchemaPlanner(None)  # type: ignore[arg-type]
        business = {
            "metrics": [
                {
                    "metric_name": "Valor Total",
                    "table": "fin.mov",
                    "column": "valor",
                    "aggregation": "SUM",
                }
            ],
            "filters": [
                {
                    "filter_name": "Exercicio",
                    "table": "fin.mov",
                    "column": "ano",
                    "operator": "IN",
                    "value": ["2025", "2026"],
                }
            ],
            "dimensions": [
                {
                    "dimension_name": "Exercicio",
                    "table": "fin.mov",
                    "column": "ano",
                }
            ],
        }
        raw = {
            "entity": "movimento",
            "grain": ["Exercicio"],
            "time_axis": {"table": "fin.mov", "column": "ano"},
            "tables": ["fin.mov", "dim.entidade"],
            "joins": [
                {
                    "source_table": "fin.mov",
                    "source_column": "entidade_id",
                    "target_table": "dim.entidade",
                    "target_column": "entidade_id",
                    "type": "INNER JOIN",
                }
            ],
            "group_by": ["Exercicio"],
            "metrics": ["Valor Total"],
            "filters": ["Exercicio"],
        }
        out = planner._sanitize(raw, business)
        self.assertEqual(out["grain"], ["fin.mov.ano"])
        self.assertEqual(out["joins"][0]["source_columns"], ["entidade_id"])
        self.assertEqual(out["joins"][0]["target_columns"], ["entidade_id"])
        self.assertEqual(out["group_by"][0]["column"], "ano")
        self.assertEqual(out["filters"][0]["operator"], "IN")

    def test_schema_planner_merges_partial_metric_filter_and_join_type(self) -> None:
        planner = SchemaPlanner(None)  # type: ignore[arg-type]
        business = {
            "metrics": [
                {
                    "metric_name": "quantidade_de_construcoes",
                    "table": "cadastro.carconstr",
                    "column": "j48_idcons",
                    "aggregation": "COUNT_DISTINCT",
                }
            ],
            "filters": [
                {
                    "filter_name": "tipo_de_caracteristica",
                    "table": "cadastro.cargrup",
                    "column": "j32_tipo",
                    "operator": "=",
                    "value": "C",
                }
            ],
            "dimensions": [
                {
                    "dimension_name": "caracteristica",
                    "table": "cadastro.caracter",
                    "column": "j31_descr",
                }
            ],
        }
        raw = {
            "entity": "construcoes",
            "grain": ["cadastro.carconstr.j48_matric", "cadastro.carconstr.j48_idcons", "cadastro.carconstr.j48_caract"],
            "time_axis": {},
            "tables": ["cadastro.carconstr", "cadastro.caracter", "cadastro.cargrup"],
            "joins": [
                {
                    "source_table": "cadastro.carconstr",
                    "source_columns": ["j48_caract"],
                    "target_table": "cadastro.caracter",
                    "target_columns": ["j31_codigo"],
                    "join_type": "INNER",
                }
            ],
            "group_by": [{"table": "cadastro.caracter", "column": "j31_descr"}],
            "metrics": [{"metric_name": "quantidade_de_construcoes", "table": "cadastro.carconstr", "column": "j48_caract"}],
            "filters": [{"table": "cadastro.cargrup", "column": "j32_tipo"}],
        }
        out = planner._sanitize(raw, business)
        self.assertEqual(out["metrics"][0]["aggregation"], "COUNT_DISTINCT")
        self.assertEqual(out["metrics"][0]["column"], "j48_caract")
        self.assertEqual(out["filters"][0]["operator"], "=")
        self.assertEqual(out["filters"][0]["value"], "C")
        self.assertEqual(out["joins"][0]["join_type"], "INNER JOIN")


class RegressionFixturesTest(unittest.TestCase):
    def _load(self, name: str) -> dict:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def test_phase1_fixtures_follow_contract(self) -> None:
        for name in (
            "quantas_ruas.phase1.json",
            "compare_periods.phase1.json",
            "construcoes_caracteristica.phase1.json",
        ):
            data = self._load(name)
            for metric in data["schema_plan"]["metrics"]:
                self.assertTrue(metric.get("table"), name)
                self.assertTrue(metric.get("column"), name)
                self.assertTrue(metric.get("aggregation"), name)
            for join in data["schema_plan"]["joins"]:
                self.assertIsInstance(join.get("source_columns"), list, name)
                self.assertIsInstance(join.get("target_columns"), list, name)
            for item in data["schema_plan"]["filters"]:
                self.assertNotIn("condition", item, name)
                self.assertNotIn("condition_text", item, name)

    def test_compile_and_critic_ruas_fixture(self) -> None:
        data = self._load("quantas_ruas.phase1.json")
        artifact = SqlCompiler().run(data["intent_spec"], data["business_spec"], data["schema_plan"])
        critic = SqlCritic().run(artifact, data["business_spec"], data["schema_plan"])
        self.assertIn("COUNT(DISTINCT t1.j14_codigo)", artifact.sql)
        self.assertTrue(critic.ok)

    def test_compile_and_critic_compare_periods_fixture(self) -> None:
        data = self._load("compare_periods.phase1.json")
        artifact = SqlCompiler().run(data["intent_spec"], data["business_spec"], data["schema_plan"])
        critic = SqlCritic().run(artifact, data["business_spec"], data["schema_plan"])
        self.assertIn("JOIN dim.entidade t2", artifact.sql)
        self.assertIn("t1.entidade_id = t2.entidade_id", artifact.sql)
        self.assertIn("t1.ano IN ('2025', '2026')", artifact.sql)
        self.assertIn("t2.status = 'ATIVA'", artifact.sql)
        self.assertIn("SUM(b.fin__mov__valor)", artifact.sql)
        self.assertTrue(critic.ok)

    def test_compile_and_critic_construcoes_fixture(self) -> None:
        data = self._load("construcoes_caracteristica.phase1.json")
        artifact = SqlCompiler().run(data["intent_spec"], data["business_spec"], data["schema_plan"])
        critic = SqlCritic().run(artifact, data["business_spec"], data["schema_plan"])
        self.assertNotIn("WITH base AS", artifact.sql)
        self.assertIn("INNER JOIN cadastro.caracter", artifact.sql)
        self.assertIn("GROUP BY", artifact.sql)
        self.assertIn("cadastro__caracter__j31_descr", artifact.sql)
        self.assertIn("COUNT(DISTINCT", artifact.sql)
        self.assertTrue(critic.ok)

    def test_compile_and_critic_ranking_uses_order_by_and_limit(self) -> None:
        intent = {"intent": "ranking", "ranking_direction": "DESC", "ranking_limit": 1}
        business = {
            "metrics": [
                {
                    "metric_name": "IPTU",
                    "table": "cadastro.iptucalv",
                    "column": "j21_valor",
                    "aggregation": "SUM",
                }
            ],
            "dimensions": [
                {
                    "dimension_name": "Bairro",
                    "table": "cadastro.bairro",
                    "column": "j13_descr",
                }
            ],
        }
        schema_plan = {
            "entity": "Bairro",
            "grain": ["cadastro.bairro.j13_codi"],
            "time_axis": {},
            "tables": ["cadastro.bairro", "cadastro.lote", "cadastro.iptubase", "cadastro.iptucalv", "cadastro.iptucalh"],
            "joins": [
                {"source_table": "cadastro.bairro", "source_columns": ["j13_codi"], "target_table": "cadastro.lote", "target_columns": ["j34_bairro"], "join_type": "JOIN"},
                {"source_table": "cadastro.lote", "source_columns": ["j34_idbql"], "target_table": "cadastro.iptubase", "target_columns": ["j01_idbql"], "join_type": "JOIN"},
                {"source_table": "cadastro.iptubase", "source_columns": ["j01_matric"], "target_table": "cadastro.iptucalv", "target_columns": ["j21_matric"], "join_type": "JOIN"},
                {"source_table": "cadastro.iptucalv", "source_columns": ["j21_codhis"], "target_table": "cadastro.iptucalh", "target_columns": ["j17_codhis"], "join_type": "JOIN"},
            ],
            "group_by": [{"table": "cadastro.bairro", "column": "j13_codi"}, {"table": "cadastro.bairro", "column": "j13_descr"}],
            "metrics": [{"metric_name": "IPTU", "table": "cadastro.iptucalv", "column": "j21_valor", "aggregation": "SUM"}],
            "filters": [
                {"table": "cadastro.iptucalv", "column": "j21_anousu", "operator": "EQUAL", "value": 2025},
                {"table": "cadastro.iptucalh", "column": "j17_descr", "operator": "CONTAINS", "value": "IPTU"},
            ],
            "risks": [],
            "open_questions": [],
        }
        artifact = SqlCompiler().run(intent, business, schema_plan, question="Qual Bairro teve o maior IPTU em 2025?")
        critic = SqlCritic().run(artifact, business, schema_plan)
        self.assertEqual(artifact.operation, "ranking")
        self.assertIn("order by iptu desc", artifact.sql.lower())
        self.assertIn("LIMIT 1", artifact.sql)
        self.assertIn("GROUP BY", artifact.sql)
        self.assertTrue(critic.ok)

    def test_compile_and_critic_sum_by_dimension(self) -> None:
        intent = {"intent": "sum_by_dimension"}
        business = {
            "metrics": [
                {
                    "metric_name": "valor total",
                    "table": "fin.mov",
                    "column": "valor",
                    "aggregation": "SUM",
                }
            ],
            "dimensions": [
                {
                    "dimension_name": "exercicio",
                    "table": "fin.mov",
                    "column": "ano",
                }
            ],
        }
        schema_plan = {
            "entity": "movimento",
            "grain": ["fin.mov.ano"],
            "time_axis": {},
            "tables": ["fin.mov"],
            "joins": [],
            "group_by": [{"table": "fin.mov", "column": "ano", "dimension_name": "exercicio"}],
            "metrics": [{"metric_name": "valor total", "table": "fin.mov", "column": "valor", "aggregation": "SUM"}],
            "filters": [],
            "risks": [],
            "open_questions": [],
        }
        artifact = SqlCompiler().run(intent, business, schema_plan)
        critic = SqlCritic().run(artifact, business, schema_plan)
        self.assertIn("GROUP BY", artifact.sql)
        self.assertIn("SUM(t1.valor)", artifact.sql)
        self.assertTrue(critic.ok)

    def test_executor_uses_readonly_query(self) -> None:
        class FakeMcp:
            def __init__(self) -> None:
                self.calls = []

            def readonly_query(self, sql: str, limit: int = 1000, statement_timeout_ms: int | None = None) -> dict:
                self.calls.append({"sql": sql, "limit": limit, "statement_timeout_ms": statement_timeout_ms})
                return {"sql": sql, "limit": limit, "row_count": 2, "duration_ms": 7, "rows": [{"x": 1}, {"x": 2}]}

        fake = FakeMcp()
        artifact = SqlCompiler().run(
            {"intent": "count_by_dimension"},
            {"metrics": [{"metric_name": "quantidade de ruas", "table": "cadastro.ruas", "column": "j14_codigo", "aggregation": "COUNT_DISTINCT"}]},
            {"entity": "ruas", "grain": ["cadastro.ruas.j14_codigo"], "tables": ["cadastro.ruas"], "joins": [], "group_by": [], "metrics": [{"metric_name": "quantidade de ruas", "table": "cadastro.ruas", "column": "j14_codigo", "aggregation": "COUNT_DISTINCT"}], "filters": [], "risks": [], "open_questions": []},
        )
        execution = Executor(fake).run(artifact)
        self.assertTrue(execution.ok)
        self.assertEqual(execution.row_count, 2)
        self.assertEqual(fake.calls[0]["limit"], 1000)
        self.assertIsNotNone(fake.calls[0]["statement_timeout_ms"])
        self.assertIn("COUNT(DISTINCT", fake.calls[0]["sql"])

    def test_answer_synthesizer_collapses_sql_by_default(self) -> None:
        class FakeLlm:
            def text(self, system: str, user: dict, json_mode: bool = False) -> str:
                return "O resultado mostra 1 rua cadastrada."

        artifact = SqlArtifact(
            operation="count_by_dimension",
            sql="SELECT\n  COUNT(DISTINCT j14_codigo) AS quantidade_de_ruas\nFROM cadastro.ruas",
            limit=1000,
            tables=["cadastro.ruas"],
            joins=[],
            filters=[],
            metrics=[],
            group_by=[],
            time_axis={},
            notes=["nota"],
        )
        execution = type(
            "Execution",
            (),
            {
                "ok": True,
                "sql": artifact.sql,
                "limit": 1000,
                "row_count": 1,
                "duration_ms": 10,
                "rows": [{"quantidade_de_ruas": 1}],
                "error": "",
                "notes": [],
            },
        )()
        result = AnswerSynthesizer(FakeLlm()).run("quantas ruas temos ?", {"question": "quantas ruas temos ?"}, artifact, execution, {}, {})
        self.assertIn("O resultado mostra 1 rua cadastrada.", result.answer)
        self.assertIn("<details><summary>Fonte tecnica e SQL usada</summary>", result.answer)
        self.assertIn("```sql", result.answer)
        self.assertIn("COUNT(DISTINCT j14_codigo)", result.answer)


if __name__ == "__main__":
    unittest.main()
