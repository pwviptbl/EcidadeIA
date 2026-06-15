## cadastro.averba



> Fonte manual: `knowledge/manual/cadastro/averba.md`



### 6.1 Relacionamentos diretos

| Tabela | Relação | Uso |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = averba.j55_matric` | Vincula a averbação à matrícula imobiliária |
| `cgm` | `cgm.z01_numcgm = averba.j55_numcgm` | Recupera o CGM associado à averbação |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Recupera o lote da matrícula |
| `cgm as a` | `a.z01_numcgm = iptubase.j01_numcgm` | Recupera o CGM do proprietário principal da matrícula |
