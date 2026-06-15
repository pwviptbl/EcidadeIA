## ecidade



> Fonte manual: `knowledge/manual/ecidade.md`



### 1. Visão geral

O **e-Cidade** é um software público de **gestão municipal**, utilizado para apoiar processos administrativos, financeiros, tributários, patrimoniais e operacionais de municípios.

O sistema é organizado em **áreas principais**, **módulos** e **aplicações complementares**. Cada módulo possui regras de negócio próprias e, no banco de dados, costuma estar associado a um **schema específico**.

Este documento descreve o contexto geral do e-Cidade para uso em catálogo semântico, documentação técnica, agentes de IA, consultas assistidas e análise de dados.

### 4. Organização do banco de dados

O banco de dados do e-Cidade é organizado em **schemas**.

Em geral, cada schema representa uma área, módulo ou domínio funcional do sistema. As tabelas de um módulo costumam ficar agrupadas no schema correspondente.

Exemplo:

| Módulo | Área | Schema esperado |
|---|---|---|
| Contabilidade | Financeiro | `contabilidade` |

As tabelas normalmente possuem **chaves primárias** e **chaves estrangeiras** para representar vínculos entre entidades do sistema.

A maioria das relações entre tabelas deve ser interpretada preferencialmente por:

1. Foreign keys existentes no banco;
2. Nomes e descrições de campos;
3. Regras de negócio do módulo;
4. Documentação funcional;
5. Validação com usuários técnicos ou especialistas do domínio.

### 5.3 Departamento

O **departamento** representa uma unidade administrativa interna da estrutura municipal.

Pode ser usado para identificar setores, divisões, unidades gestoras, locais de execução ou responsáveis operacionais, dependendo do módulo.

O significado exato de departamento pode variar por área e deve ser validado conforme o módulo analisado.

Uso comum:

- Agrupamento administrativo;
- Vínculo de usuários;
- Responsabilidade por processos;
- Controle orçamentário ou operacional;
- Filtro em relatórios internos.

### 5.5 Fonte de recurso

A **fonte de recurso** identifica a origem ou vinculação dos recursos utilizados em operações orçamentárias, financeiras e contábeis.

É um conceito importante principalmente para análises de:

- Receita;
- Despesa;
- Empenho;
- Orçamento;
- Prestação de contas;
- Relatórios contábeis;
- Execução financeira por origem de recurso.

A fonte de recurso ajuda a responder perguntas como:

- De onde veio o recurso?
- Qual recurso financiou determinada despesa?
- Quais despesas estão vinculadas a uma fonte específica?
- Como os recursos foram executados por exercício, órgão ou programa?

### 6. Relações entre tabelas

As tabelas do e-Cidade geralmente se relacionam por meio de **foreign keys**.

Essas relações representam vínculos entre entidades, como:

- Matrícula e imóvel;
- Empenho e CGM;
- Usuário e operação realizada;
- Receita e fonte de recurso;
- Departamento e movimentação;
- Instituição e lançamento;
- Processo e documentos;
- Aluno e matrícula;
- Paciente e atendimento.

Para agentes de IA e consultas assistidas, as foreign keys são fundamentais para evitar inferências incorretas.

Regra recomendada:

> Sempre que existir foreign key documentada, ela deve ter prioridade sobre inferências baseadas apenas em nomes de campos.
