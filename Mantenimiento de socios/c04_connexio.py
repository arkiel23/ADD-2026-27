"""Criteri 2.4 - Establir la connexio.

    python c04_connexio.py

Obrir la connexio es una linia. El que importa es:
  - saber que hi ha connexio de veritat,
  - distingir QUE ha fallat quan no hi ha connexio,
  - tancar-la SEMPRE, passi el que passi.
"""
import mysql.connector
from mysql.connector import errorcode

from db import CONFIG, connectar


def connexio_basica() -> None:
    print("--- Connexio basica ---")
    cn = connectar()
    try:
        print("connectat?       :", cn.is_connected())
        print("id de connexio   :", cn.connection_id)
        cur = cn.cursor()
        cur.execute("SELECT VERSION(), DATABASE()")
        versio, bd = cur.fetchone()
        cur.close()
        print("versio servidor  :", versio)
        print("base de dades    :", bd)
        print("autocommit       :", cn.autocommit)
    finally:
        cn.close()                     # finally: es tanca encara que peti alguna cosa
        print("tancada. connectat?", cn.is_connected())


def quan_falla() -> None:
    """Cada error de connexio porta el seu numero (errno). Aixi sabem que dir."""
    print("\n--- Quan la connexio falla ---")
    proves = [
        ("contrasenya incorrecta", {**CONFIG, "password": "dolenta"}),
        ("BD inexistent", {**CONFIG, "database": "no_existeix"}),
    ]
    for descripcio, config in proves:
        try:
            cn = mysql.connector.connect(**config)
            cn.close()
            print(f"{descripcio:<24} -> ha connectat (inesperat)")
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:     # 1045 (Usuari equivocat)
                motiu = "usuari o contrasenya incorrectes"
            elif e.errno in (errorcode.ER_BAD_DB_ERROR,          # 1049 (BD inexistent)
                             errorcode.ER_DBACCESS_DENIED_ERROR):  # 1044 (L'usuari existeix pero no te privilegis)
                motiu = "la BD no existeix o no hi tens permis"
            elif e.errno == errorcode.CR_CONN_HOST_ERROR:       # 2003 (Servidor parat o no respon)
                motiu = "el servidor no respon"
            else:
                motiu = "altre error"
            print(f"{descripcio:<24} -> errno {e.errno}: {motiu}")


if __name__ == "__main__":
    connexio_basica()
    quan_falla()
