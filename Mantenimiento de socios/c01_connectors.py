"""Criteri 2.1 - Avantatges i inconvenients d'utilitzar connectors.

    python c01_connectors.py

Un connector (driver) es la biblioteca que tradueix les crides de Python
al protocol de xarxa de MySQL. mysql-connector-python compleix la PEP 249
(DB-API 2.0): connect, cursor, execute, fetch*, commit, rollback.
No necessita cap taula: es pot executar abans de c05.
"""
from contextlib import closing

import mysql.connector

from db import connectar


def fitxa_del_connector() -> None:
    """El connector declara com es comporta: no cal endevinar-ho."""
    print("--- Fitxa del connector ---")
    print("versio      :", mysql.connector.__version__)
    print("apilevel    :", mysql.connector.apilevel, " <- compleix la DB-API 2.0")
    print("paramstyle  :", mysql.connector.paramstyle, "<- els parametres s'escriuen %s")


def parametres_vs_concatenar() -> None:
    """L'avantatge mes important: el connector escapa els parametres.

    Simulem que un usuari escriu aixo en un formulari de cerca.
    """
    print("\n--- Concatenar vs parametritzar ---")
    entrada = "x' OR '1'='1"

    # MALAMENT: el text de l'usuari passa a formar part del SQL.
    sql_perillos = "SELECT * FROM soci WHERE email = '" + entrada + "'"
    print("concatenant  :", sql_perillos)
    print("               ^ la condicio sempre es certa: injeccio SQL")

    # BE: el SQL i les dades viatgen per separat. El connector ho escapa.
    with closing(connectar(amb_bd=False)) as cn, closing(cn.cursor()) as cur:
        cur.execute("SELECT %s", (entrada,))
        print("parametritzat:", cur.fetchone()[0], "<- nomes es un text, no codi SQL")


def balanc() -> None:
    print("\n--- Balanc ---")
    print("AVANTATGES")
    print(" + Una API estandard (PEP 249): el codi s'assembla per a qualsevol SGBD.")
    print(" + No cal programar el protocol de xarxa de MySQL.")
    print(" + Parametres escapats: defensa real contra la injeccio SQL.")
    print(" + Converteix tipus: DATE -> date, DECIMAL -> Decimal, NULL -> None.")
    print("INCONVENIENTS")
    print(" - Una dependencia mes a instal-lar i mantenir (pip).")
    print(" - Cada execute() es un viatge per la xarxa: cal fer poques consultes.")
    print(" - El SQL segueix sent del dialecte de MySQL: no es 100% portable.")


if __name__ == "__main__":
    fitxa_del_connector()
    parametres_vs_concatenar()
    balanc()
