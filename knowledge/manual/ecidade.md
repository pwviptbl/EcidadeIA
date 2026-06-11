# e-Cidade — Contexto Geral

## 1. Visão geral

O **e-Cidade** é um software público de **gestão municipal**, utilizado para apoiar processos administrativos, financeiros, tributários, patrimoniais e operacionais de municípios.

O sistema é organizado em **áreas principais**, **módulos** e **aplicações complementares**. Cada módulo possui regras de negócio próprias e, no banco de dados, costuma estar associado a um **schema específico**.

Este documento descreve o contexto geral do e-Cidade para uso em catálogo semântico, documentação técnica, agentes de IA, consultas assistidas e análise de dados.

## 2. Áreas principais do e-Cidade

O e-Cidade é composto por **7 áreas principais**:

| Área | Descrição resumida |
|---|---|
| Financeiro | Gestão orçamentária, contábil, empenhos, receitas, despesas e execução financeira. |
| Patrimonial | Gestão de bens patrimoniais, inventário, movimentações e controle patrimonial. |
| Tributário | Gestão de tributos municipais, cadastro imobiliário, arrecadação, dívida ativa e fiscalização. |
| Folha de pagamento | Gestão de servidores, vínculos, remuneração, eventos de folha e obrigações relacionadas. |
| Educação | Gestão escolar, alunos, matrículas, turmas, calendário, transporte e processos educacionais. |
| Saúde | Gestão de atendimentos, unidades, pacientes, produção, agendamentos e dados operacionais de saúde. |
| Processo eletrônico | Gestão de processos administrativos, tramitação, documentos, protocolos e fluxos internos. |

## 3. Aplicações complementares

Além das áreas principais, o ecossistema e-Cidade pode possuir aplicações secundárias ou complementares, como:

- Portal da Transparência
- Serviços Online
- Aplicativo móvel
- BI
- Central de Vagas
- Portal do Aluno
- Nota Fiscal Eletrônica

Essas aplicações podem consumir dados dos módulos principais ou disponibilizar interfaces específicas para cidadãos, gestores, servidores e órgãos de controle.

## 4. Organização do banco de dados

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

## 5. Conceitos gerais

### 5.1 CGM — Cadastro Geral do Município

O **CGM** é o Cadastro Geral do Município.

Ele concentra o cadastro de **pessoas físicas** e **pessoas jurídicas** utilizadas por diversos módulos do sistema.

Normalmente, campos relacionados ao CGM possuem nomes como:

- `numcgm`
- `*_numcgm`
- campos específicos com sufixo ou prefixo relacionado ao módulo

Exemplo:

| Campo | Tabela | Significado |
|---|---|---|
| `e60_numcgm` | `empempenho` | Código do CGM da pessoa física ou jurídica vinculada ao empenho. |

O CGM deve ser tratado como uma entidade transversal do e-Cidade, pois pode aparecer em módulos financeiros, tributários, patrimoniais, educacionais, de saúde e administrativos.

### 5.2 Instituição

A **instituição** representa a forma como a organização municipal é dividida dentro do sistema.

Ela pode representar estruturas como:

- Administração direta;
- Administração indireta;
- Câmara municipal;
- Autarquias;
- Fundações;
- Secretarias ou órgãos vinculados, conforme a configuração do município.

A administração direta é composta por órgãos sem personalidade jurídica própria, como prefeitura e secretarias.

A administração indireta é formada por entidades descentralizadas, como autarquias e fundações.

A câmara municipal atua como o poder legislativo independente.

A instituição é uma dimensão importante para análises financeiras, contábeis, orçamentárias, patrimoniais e administrativas.

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

### 5.4 Usuário

O **usuário** representa a conta utilizada por servidores, operadores ou responsáveis para acessar e operar o sistema.

Campos de usuário geralmente aparecem em tabelas para registrar:

- Quem cadastrou um registro;
- Quem alterou uma informação;
- Quem executou uma rotina;
- Quem autorizou, cancelou ou baixou determinado dado;
- Auditoria e rastreabilidade operacional.

Campos típicos podem seguir nomes como:

- `usuario`
- `id_usuario`
- `*_usuario`

O usuário não deve ser confundido com o CGM. O CGM representa pessoa física ou jurídica no cadastro geral; o usuário representa credencial ou operador do sistema.

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

## 6. Relações entre tabelas

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

## 7. Glossário inicial

| Termo | Definição |
|---|---|
| e-Cidade | Software público de gestão municipal. |
| Área | Agrupamento funcional principal do sistema. |
| Módulo | Componente funcional dentro de uma área. |
| Schema | Organização lógica das tabelas no banco de dados. |
| CGM | Cadastro Geral do Município, usado para pessoas físicas e jurídicas. |
| Instituição | Estrutura organizacional municipal representada no sistema. |
| Departamento | Unidade administrativa ou operacional, conforme o módulo. |
| Usuário | Conta ou operador que acessa e executa ações no sistema. |
| Fonte de recurso | Origem ou vinculação dos recursos financeiros/orçamentários. |
| Foreign key | Chave estrangeira que representa vínculo entre tabelas. |


