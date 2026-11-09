# RA2 · Accés a dades amb Python i MySQL

Projecte d'exemple de la RA2 (MP06 Accés a dades, DAM): una **biblioteca** amb 4 taules
relacionades i un fitxer Python per cada criteri d'avaluació.

```
autor 1 ──< N llibre 1 ──< N prestec N >── 1 soci
```

## Posada en marxa

1. **Un cop, com a root** (MySQL Workbench): executa `00_admin.sql`.
2. Instal·la el connector: `pip install -r requirements.txt`
3. Revisa `db.py` (host, usuari, contrasenya). També es pot fer amb variables d'entorn
   `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`.
4. **Executa primer `c05_estructura.py`**: crea les taules i les dades. Es pot repetir
   sempre que vulguis tornar a l'estat inicial.
5. La resta, en qualsevol ordre: `python c08_consultes.py`

## Mapa criteri → fitxer

| Criteri | Fitxer | Què demostra |
|---|---|---|
| 2.1 | `c01_connectors.py` | apilevel, paramstyle, injecció SQL vs paràmetres, balanç |
| 2.2 | `c02_encastat_vs_independent.py` | SQLite (encastat) vs MySQL (servidor) |
| 2.3 | `c03_connector_idoni.py` | per què mysql-connector-python i alternatives |
| 2.4 | `db.py`, `c04_connexio.py` | paràmetres de connexió, errors 1045/1044/1049, tancar sempre |
| 2.5 | `c05_estructura.py` | CREATE DATABASE/TABLE amb PK, FK, UNIQUE, CHECK |
| 2.6 | `c06_modificar.py` | INSERT, executemany, UPDATE, DELETE, lastrowid, rowcount, FK |
| 2.7 | `c07_objectes_resultat.py` | tupla, diccionari, `@dataclass Llibre` |
| 2.8 | `c08_consultes.py` | fetchone/fetchall/fetchmany, JOIN, LEFT JOIN + GROUP BY, LIKE |
| 2.9 | `c09_alliberar_recursos.py` | try/finally, `with closing`, fuita de connexions, DROP VIEW |
| 2.10 | `c10_transaccions.py` | préstec = UPDATE + INSERT, commit/rollback |
| 2.11 | `c11_procediments.py` | `callproc` amb OUT, SIGNAL, `stored_results`, FUNCTION |

Provat amb Python 3.12/3.13, mysql-connector-python 9.1.0 i MySQL 8.0.
