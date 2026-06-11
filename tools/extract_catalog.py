from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row


BASE_DIR = Path(__file__).resolve().parent
SYSTEM_SCHEMAS = {
    "information_schema",
    "pg_catalog",
    "pg_toast",
}


def log(message: str) -> None:
    print(f"[catalog-extractor] {message}", file=sys.stderr, flush=True)


def load_env(path: Path = BASE_DIR / ".env") -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def connect(prefix: str):
    return psycopg.connect(
        host=os.getenv(f"{prefix}_HOST", "localhost"),
        port=int(os.getenv(f"{prefix}_PORT", "5432")),
        dbname=os.getenv(f"{prefix}_DATABASE", ""),
        user=os.getenv(f"{prefix}_USERNAME", ""),
        password=os.getenv(f"{prefix}_PASSWORD", ""),
        row_factory=dict_row,
        connect_timeout=10,
    )


def fetch_rows(conn, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]


def fetch_schemas(conn) -> list[str]:
    rows = fetch_rows(
        conn,
        """
        select schema_name
        from information_schema.schemata
        where schema_name not like 'pg_%%'
          and schema_name <> 'information_schema'
        order by schema_name
        """,
    )
    return [row["schema_name"] for row in rows if row["schema_name"] not in SYSTEM_SCHEMAS]


def fetch_tables(conn, schemas: list[str]) -> list[dict[str, Any]]:
    return fetch_rows(
        conn,
        """
        select
            table_schema,
            table_name,
            table_type
        from information_schema.tables
        where table_schema = any(%s)
          and table_type in ('BASE TABLE', 'VIEW')
        order by table_schema, table_name
        """,
        (schemas,),
    )


def fetch_columns(conn, schemas: list[str]) -> list[dict[str, Any]]:
    return fetch_rows(
        conn,
        """
        select
            table_schema,
            table_name,
            column_name,
            ordinal_position,
            data_type,
            udt_name,
            is_nullable,
            character_maximum_length,
            numeric_precision,
            numeric_scale,
            column_default
        from information_schema.columns
        where table_schema = any(%s)
        order by table_schema, table_name, ordinal_position
        """,
        (schemas,),
    )


def fetch_primary_keys(conn, schemas: list[str]) -> dict[tuple[str, str], list[str]]:
    rows = fetch_rows(
        conn,
        """
        select
            tc.table_schema,
            tc.table_name,
            kcu.column_name,
            kcu.ordinal_position
        from information_schema.table_constraints tc
        join information_schema.key_column_usage kcu
          on kcu.constraint_schema = tc.constraint_schema
         and kcu.constraint_name = tc.constraint_name
         and kcu.table_schema = tc.table_schema
         and kcu.table_name = tc.table_name
        where tc.constraint_type = 'PRIMARY KEY'
          and tc.table_schema = any(%s)
        order by tc.table_schema, tc.table_name, kcu.ordinal_position
        """,
        (schemas,),
    )
    keys: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in rows:
        keys[(row["table_schema"], row["table_name"])].append(row["column_name"])
    return dict(keys)


def fetch_foreign_keys(conn, schemas: list[str]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    rows = fetch_rows(
        conn,
        """
        select
            tc.constraint_name,
            tc.table_schema as source_schema,
            tc.table_name as source_table,
            kcu.column_name as source_column,
            ccu.table_schema as target_schema,
            ccu.table_name as target_table,
            ccu.column_name as target_column,
            kcu.ordinal_position
        from information_schema.table_constraints tc
        join information_schema.key_column_usage kcu
          on kcu.constraint_schema = tc.constraint_schema
         and kcu.constraint_name = tc.constraint_name
         and kcu.table_schema = tc.table_schema
         and kcu.table_name = tc.table_name
        join information_schema.constraint_column_usage ccu
          on ccu.constraint_schema = tc.constraint_schema
         and ccu.constraint_name = tc.constraint_name
        where tc.constraint_type = 'FOREIGN KEY'
          and tc.table_schema = any(%s)
        order by tc.table_schema, tc.table_name, tc.constraint_name, kcu.ordinal_position
        """,
        (schemas,),
    )
    foreign_keys: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}

    for row in rows:
        key = (row["source_schema"], row["source_table"], row["constraint_name"])
        fk = grouped.setdefault(
            key,
            {
                "constraint": row["constraint_name"],
                "columns": [],
                "references": f"{row['target_schema']}.{row['target_table']}",
                "referenced_columns": [],
            },
        )
        fk["columns"].append(row["source_column"])
        fk["referenced_columns"].append(row["target_column"])

    for source_schema, source_table, _ in grouped:
        foreign_keys[(source_schema, source_table)].append(grouped[(source_schema, source_table, _)])

    return dict(foreign_keys)


def fetch_dictionary(conn) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    rows = fetch_rows(
        conn,
        """
        select
            a.codarq,
            trim(a.nomearq) as nomearq,
            trim(coalesce(a.descricao, '')) as tabela_descricao,
            trim(coalesce(a.rotulo, '')) as tabela_rotulo,
            trim(coalesce(a.sigla, '')) as sigla,
            a.tipotabela,
            c.codcam,
            trim(c.nomecam) as nomecam,
            trim(coalesce(c.conteudo, '')) as conteudo,
            trim(coalesce(c.descricao, '')) as campo_descricao,
            trim(coalesce(c.rotulo, '')) as campo_rotulo,
            trim(coalesce(c.rotulorel, '')) as campo_rotulo_rel,
            c.tamanho,
            c.nulo,
            c.maiusculo,
            c.autocompl,
            c.aceitatipo,
            trim(coalesce(c.tipoobj, '')) as tipoobj,
            ac.seqarq,
            ac.codsequencia
        from configuracoes.db_sysarquivo a
        left join configuracoes.db_sysarqcamp ac
          on ac.codarq = a.codarq
        left join configuracoes.db_syscampo c
          on c.codcam = ac.codcam
        order by a.nomearq, ac.seqarq nulls last, c.nomecam
        """,
    )

    tables: dict[str, dict[str, Any]] = {}
    columns: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        table_name = clean_identifier(row.get("nomearq"))
        if not table_name:
            continue
        tables.setdefault(
            table_name,
            {
                "description": first_text(row.get("tabela_descricao"), row.get("tabela_rotulo"), table_name),
                "rotulo": text_or_none(row.get("tabela_rotulo")),
                "sigla": text_or_none(row.get("sigla")),
                "codarq": row.get("codarq"),
                "tipotabela": row.get("tipotabela"),
            },
        )

        column_name = clean_identifier(row.get("nomecam"))
        if not column_name:
            continue
        columns[(table_name, column_name)] = {
            "label": first_text(row.get("campo_rotulo"), row.get("campo_rotulo_rel"), column_name),
            "description": first_text(row.get("campo_descricao"), row.get("campo_rotulo"), column_name),
            "dictionary_type": text_or_none(row.get("conteudo")),
            "dictionary_size": row.get("tamanho"),
            "dictionary_nullable": row.get("nulo"),
            "uppercase": row.get("maiusculo"),
            "widget": text_or_none(row.get("tipoobj")),
            "codcam": row.get("codcam"),
            "sequence": row.get("seqarq"),
            "sequence_code": row.get("codsequencia"),
        }

    return tables, columns


def build_catalogs(
    schemas: list[str],
    tables: list[dict[str, Any]],
    columns: list[dict[str, Any]],
    primary_keys: dict[tuple[str, str], list[str]],
    foreign_keys: dict[tuple[str, str], list[dict[str, Any]]],
    dict_tables: dict[str, dict[str, Any]],
    dict_columns: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    catalogs = {
        schema: {
            "domain": schema,
            "rotulo": schema.replace("_", " ").title(),
            "descricao": f"Catalogo extraido automaticamente para o schema {schema}.",
            "schema_principal": schema,
            "intencoes": default_intents_template(),
            "metricas": {},
            "templates": default_query_templates(),
            "tabelas": {},
            "exemplos": [],
        }
        for schema in schemas
    }

    for row in tables:
        schema = row["table_schema"]
        table_name = row["table_name"]
        full_name = f"{schema}.{table_name}"
        dictionary = dict_tables.get(table_name, {})
        catalogs[schema]["tabelas"][full_name] = {
            "descricao": first_text(dictionary.get("description"), dictionary.get("rotulo")),
            "grao": [],
            "chave_negocio": [],
            "coluna_tempo": None,
            "filtros_padrao": [],
            "recomendada": False,
            "colunas": {},
        }
        pk = primary_keys.get((schema, table_name), [])
        if pk:
            catalogs[schema]["tabelas"][full_name]["chave_primaria"] = pk

        fk = foreign_keys.get((schema, table_name), [])
        if fk:
            for item in fk:
                item["referencia"] = item.pop("references")
                item["colunas_referenciadas"] = item.pop("referenced_columns")
            catalogs[schema]["tabelas"][full_name]["chaves_estrangeiras"] = fk

    for row in columns:
        schema = row["table_schema"]
        table_name = row["table_name"]
        full_name = f"{schema}.{table_name}"
        table = catalogs.get(schema, {}).get("tabelas", {}).get(full_name)
        if table is None:
            continue

        column_name = row["column_name"]
        dictionary = dict_columns.get((table_name, column_name), {})
        table["colunas"][column_name] = {
            "descricao": first_text(dictionary.get("description"), dictionary.get("label")),
            "tipo": row.get("data_type"),
            "papel": "",
            "metrica": "",
        }

    return catalogs


def default_intents_template() -> dict[str, Any]:
    return {
        "comparar_periodos": {
            "descricao": "Compara metricas entre dois periodos ou exercicios.",
            "gatilhos": [
                "comparar",
                "aumento",
                "reducao",
                "redução",
                "variacao",
                "variação",
                "evolucao",
                "evolução",
            ],
            "estrategia_comparacao": "mesma_entidade",
            "dimensoes_obrigatorias": ["tempo"],
            "exige_chave_negocio": True,
            "template_padrao": "comparar_periodos_mesma_entidade",
            "regras": [
                "Comparar a mesma entidade quando houver chave_negocio.",
                "Nao usar media por periodo como unica evidencia de variacao.",
                "Nao inferir causa sem metrica retornada.",
            ],
        },
        "contar_registros": {
            "descricao": "Conta registros de uma entidade ou tabela.",
            "gatilhos": ["quantos", "quantas", "total", "contar", "existem", "existe"],
            "agregacao_padrao": "contagem",
        },
    }


def default_query_templates() -> dict[str, Any]:
    return {
        "comparar_periodos_mesma_entidade": {
            "intencao": "comparar_periodos",
            "estrategia": "autojuncao_mesma_tabela",
            "requer": ["tabela", "chave_negocio", "coluna_tempo", "metricas", "periodo_a", "periodo_b"],
            "agregacoes_permitidas": ["contagem", "media_delta", "soma_delta", "media_periodo"],
        }
    }


def clean_identifier(value: Any) -> str:
    return str(value or "").strip().lower()


def normalize_text(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""

    # Corrige mojibake comum de textos Latin-1/Windows-1252 interpretados como UTF-8.
    if any(token in text for token in ("Ã", "Â", "â", "�")):
        for source_encoding in ("latin1", "cp1252"):
            try:
                repaired = text.encode(source_encoding).decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            if repaired and repaired != text:
                text = repaired
                break

    return " ".join(text.split())


def text_or_none(value: Any) -> str | None:
    text = normalize_text(value)
    return text or None


def first_text(*values: Any) -> str:
    for value in values:
        text = normalize_text(value)
        if text:
            return text
    return ""


def write_catalog(catalog: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrai catalogos JSON por schema unindo estrutura real e dicionario de dados do e-Cidade."
    )
    parser.add_argument("--schema", default=os.getenv("CATALOG_SCHEMA", "cadastro"), help="Schema alvo ou 'all'.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(os.getenv("CATALOG_OUTPUT_DIR", "../catalog")),
    )
    parser.add_argument("--output", type=Path, default=None, help="Arquivo de saida quando --schema nao for all.")
    return parser.parse_args()


def selected_schemas(prod_conn, schema_arg: str) -> list[str]:
    if schema_arg.lower() == "all":
        return fetch_schemas(prod_conn)
    return [item.strip() for item in schema_arg.split(",") if item.strip()]


def main() -> None:
    load_env()
    args = parse_args()

    log("conectando no banco real e no dicionario")
    with connect("PROD_DB") as prod_conn, connect("DICT_DB") as dict_conn:
        schemas = selected_schemas(prod_conn, args.schema)
        log(f"schemas selecionados: {len(schemas)} ({', '.join(schemas[:12])}{'...' if len(schemas) > 12 else ''})")
        tables = fetch_tables(prod_conn, schemas)
        log(f"tabelas reais carregadas: {len(tables)}")
        columns = fetch_columns(prod_conn, schemas)
        log(f"campos reais carregados: {len(columns)}")
        primary_keys = fetch_primary_keys(prod_conn, schemas)
        log(f"tabelas com PK: {len(primary_keys)}")
        foreign_keys = fetch_foreign_keys(prod_conn, schemas)
        log(f"tabelas com FK: {len(foreign_keys)}")
        dict_tables, dict_columns = fetch_dictionary(dict_conn)
        log(f"dicionario carregado: {len(dict_tables)} tabelas, {len(dict_columns)} campos")

    log("montando catalogos por schema")
    catalogs = build_catalogs(
        schemas=schemas,
        tables=tables,
        columns=columns,
        primary_keys=primary_keys,
        foreign_keys=foreign_keys,
        dict_tables=dict_tables,
        dict_columns=dict_columns,
    )

    written = []
    for schema, catalog in catalogs.items():
        output = args.output if args.output and len(catalogs) == 1 else args.output_dir / f"{schema}.json"
        write_catalog(catalog, output)
        log(
            f"gravado {output}: "
            f"{len(catalog['tabelas'])} tabelas, "
            f"{sum(len(table.get('colunas', {})) for table in catalog['tabelas'].values())} campos"
        )
        written.append(
            {
                "schema": schema,
                "output": str(output),
                "tables": len(catalog["tabelas"]),
                "columns": sum(len(table.get("colunas", {})) for table in catalog["tabelas"].values()),
            }
        )

    log("extracao concluida")
    print(json.dumps({"written": written}, ensure_ascii=False))


if __name__ == "__main__":
    main()
