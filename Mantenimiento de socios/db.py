"""db.py - L'UNIC lloc del projecte on es decideix COM es connecta a MySQL.

Criteris 2.3 i 2.4. Tots els fitxers c0X importen connectar() d'aqui.

Per que un modul a part?
  - Si canvia el servidor, l'usuari o fins i tot el connector, nomes es toca
    aquest fitxer. La resta del programa no se n'assabenta.
  - Es exactament el que fara qualsevol backend (Flask, FastAPI, Django...):
    una capa d'acces a dades separada de la logica.

Les dades sensibles es poden passar per variables d'entorn (MYSQL_HOST,
MYSQL_USER, MYSQL_PASSWORD). Si no hi son, s'usen els valors de classe.
Aixi la contrasenya no queda escrita al codi quan es passi a produccio.
"""
# Conexió amb la BD, tota la estona la cridem
import os

import mysql.connector

CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),  # servidor
    "port": int(os.getenv("MYSQL_PORT", "3306")),     # port MySQL
    "user": os.getenv("MYSQL_USER", "alumne"),
    "password": os.getenv("MYSQL_PASSWORD", "123456"),
    "database": "biblioteca",                         # BD de treball
    "charset": "utf8mb4",                             # Unicode complet
    "connection_timeout": 5,                          # no penjar-se
    "autocommit": False,                              # commit a ma
}


def connectar(amb_bd: bool = True):
    """Obre i retorna una connexio nova a MySQL.

    amb_bd=False serveix per connectar SENSE triar base de dades: cal per
    fer CREATE DATABASE (no et pots connectar a una BD que encara no existeix).
    Qui crida aquesta funcio es responsable de tancar la connexio (criteri 2.9).
    """
    config = dict(CONFIG)
    if not amb_bd:
        config.pop("database")
    return mysql.connector.connect(**config)
