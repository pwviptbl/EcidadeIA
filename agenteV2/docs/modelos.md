# Estrategia de Modelos

## Decisao inicial

Usar modelo mais forte onde ha raciocinio e modelo barato onde ha tarefa simples.

## Recomendacao

### Gemini 2.5 Flash

Usar em:

- `IntentExtractor`;
- `BusinessResolver`;
- `SchemaPlanner`;
- `PlanValidator` quando usar LLM;
- `SqlCritic`;
- `RepairLoop`;
- `AnswerSynthesizer`.

Motivo: essas etapas exigem seguir regra, interpretar contexto e corrigir
decisoes. O custo maior e aceitavel porque evita semanas de retrabalho e erro
silencioso.

Configuracao:

- temperatura: `0.0` a `0.2`;
- JSON mode ou structured output quando a saida for contrato;
- prompts curtos, separados por etapa;
- contexto filtrado por RAG, nao dump completo do catalogo.

### Gemini Flash Lite

Usar em:

- titulo de conversa;
- resumo curto de historico;
- classificacao preliminar barata, se necessario;
- tarefas que nao decidem SQL nem regra de negocio.

## Regra de custo

O planner e caro porque decide. Se ele errar, todo o fluxo custa mais.

Preferencia:

```text
gastar um pouco mais no plano
-> reduzir tentativa falha
-> reduzir SQL errado
-> reduzir retrabalho manual
```

## Proibicoes

- Nao usar modelo barato para `SchemaPlanner` em pergunta complexa.
- Nao pedir SQL direto ao modelo como caminho principal.
- Nao aceitar resposta textual quando a etapa exige JSON validavel.
