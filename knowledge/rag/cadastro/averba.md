## cadastro.averba



> Fonte manual: `knowledge/manual/cadastro/averba.md`



### 6.1 Relacionamentos diretos

| Tabela | Relação | Uso |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = averba.j55_matric` | Vincula a averbação à matrícula imobiliária |
| `cgm` | `cgm.z01_numcgm = averba.j55_numcgm` | Recupera o CGM associado à averbação |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Recupera o lote da matrícula |
| `cgm as a` | `a.z01_numcgm = iptubase.j01_numcgm` | Recupera o CGM do proprietário principal da matrícula |

### 11.4 Averbações com dados da matrícula e proprietário principal

```sql
select
  averba.j55_codave,
  averba.j55_matric,
  averba.j55_data,
  averba.j55_regimo,
  averba.j55_cidade,
  averba.j55_numcgm,
  cgm.z01_nome as nome_cgm_averbacao,
  iptubase.j01_numcgm as numcgm_proprietario_atual,
  proprietario_atual.z01_nome as nome_proprietario_atual,
  lote.j34_idbql
from averba
     inner join iptubase on iptubase.j01_matric = averba.j55_matric
