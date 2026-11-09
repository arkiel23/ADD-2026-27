"""Criteri 2.3 - Utilitzar el connector idoni a l'aplicacio.

    python c03_connector_idoni.py

Per a MySQL hi ha diversos connectors. Triem mysql-connector-python perque:
  1. Es l'OFICIAL (Oracle, el fabricant de MySQL).
  2. Compleix la DB-API 2.0 sense afegir capes: veiem el SQL real.
  3. S'instal-la amb pip i no necessita compilar res.
La decisio queda tancada a db.py: si un dia es canvia, es canvia alla.
"""
from contextlib import closing

import mysql.connector

from db import connectar

ALTERNATIVES = [
    ("mysql-connector-python", "Oficial d'Oracle", "El que fem servir"),
    ("PyMySQL", "Python pur, molt lleuger", "Si no pots instal-lar res compilat"),
    ("mysqlclient", "Embolcall en C, el mes rapid", "Molta carrega (Django l'usa)"),
    ("SQLAlchemy", "ORM: va PER SOBRE d'un connector", "Projectes grans; amaga el SQL"),
]


def que_tinc_installat() -> None:
    print("--- El connector instal-lat ---")
    print("paquet   : mysql-connector-python", mysql.connector.__version__)
    # El paquet porta una implementacio en Python pur i, si pot, una en C.
    print("extensio C disponible:", getattr(mysql.connector, "HAVE_CEXT", False))


def comprovar_que_funciona() -> None:
    """Fem servir connectar() de db.py: aquest fitxer no sap ni el host."""
    with closing(connectar()) as cn, closing(cn.cursor()) as cur:
        cur.execute("SELECT VERSION()")
        print("connectat a:", cn.server_host, "| versio servidor:", cur.fetchone()[0])


def alternatives() -> None:
    print("\n--- Alternatives i quan triar-les ---")
    for nom, que_es, quan in ALTERNATIVES:
        print(f"{nom:<24}{que_es:<34}{quan}")


if __name__ == "__main__":
    que_tinc_installat()
    comprovar_que_funciona()
    alternatives()
