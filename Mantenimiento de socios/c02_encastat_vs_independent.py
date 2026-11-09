"""Criteri 2.2 - Gestors de bases de dades encastats i independents.

    python c02_encastat_vs_independent.py

ENCASTAT (SQLite): el motor es una biblioteca dins del nostre proces.
   La BD es un fitxer. Ni servidor, ni port, ni usuari.
INDEPENDENT (MySQL): un servidor a part que escolta en un port.
   Molts clients alhora, usuaris i permisos, acces per xarxa.

SQLite ve inclos amb Python (modul sqlite3): no cal instal-lar res. Nomes el
fem servir aqui, per comparar; la resta de la RA es MySQL.
"""
import sqlite3
from contextlib import closing

from db import CONFIG, connectar


def gestor_encastat() -> None:
    print("--- Encastat: SQLite ---")
    # connect() nomes demana un fitxer (o :memory: per tenir-la a la RAM).
    with closing(sqlite3.connect(":memory:")) as cn:
        cn.execute("CREATE TABLE prova (id INTEGER PRIMARY KEY, text TEXT)")
        cn.execute("INSERT INTO prova (text) VALUES (?)", ("hola",))   # marcador ?
        cn.commit()
        print("versio motor:", cn.execute("SELECT sqlite_version()").fetchone()[0])
        print("files       :", cn.execute("SELECT COUNT(*) FROM prova").fetchone()[0])
        print("usuari      : no existeix; mana el sistema de fitxers")


def gestor_independent() -> None:
    print("\n--- Independent: MySQL ---")
    with closing(connectar(amb_bd=False)) as cn, closing(cn.cursor()) as cur:
        cur.execute("SELECT VERSION(), CURRENT_USER()")
        versio, usuari = cur.fetchone()
        print("versio motor:", versio)
        print("servidor    :", f"{CONFIG['host']}:{CONFIG['port']}")
        print("usuari      :", usuari, "<- el servidor sap qui ets")

        cur.execute("SHOW STATUS LIKE 'Threads_connected'")
        print("clients ara :", cur.fetchone()[1], "<- n'atén molts alhora")


def quan_fer_servir_cada_un() -> None:
    print("\n--- Quan fer servir cada un ---")
    print(f"{'':<20}{'SQLite (encastat)':<26}{'MySQL (independent)'}")
    files = [
        ("On viu el motor", "dins del programa", "servidor a part"),
        ("Instal-lacio", "cap", "instal-lar servidor"),
        ("Usuaris/permisos", "no", "si (GRANT)"),
        ("Clients alhora", "1 escriptor", "molts"),
        ("Ideal per a", "app mobil/escriptori", "web i backend"),
    ]
    for criteri, a, b in files:
        print(f"{criteri:<20}{a:<26}{b}")


if __name__ == "__main__":
    gestor_encastat()
    gestor_independent()
    quan_fer_servir_cada_un()
