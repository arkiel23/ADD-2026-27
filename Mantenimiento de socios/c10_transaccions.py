"""Criteri 2.10 - Gestionar les transaccions.

    python c10_transaccions.py

Una transaccio es un grup d'operacions que es fan TOTES o CAP.
Fer un prestec son dues operacions:
    1. restar un exemplar disponible al llibre (UPDATE llibre)
    2. apuntar el prestec                     (INSERT prestec)
Si la 2 falla i la 1 ja s'havia guardat, perdem un exemplar "fantasma".

Amb autocommit=False (db.py) la transaccio comenca sola amb la primera
sentencia i acaba quan cridem commit() (guardar) o rollback() (desfer).
"""
from contextlib import closing
from datetime import date

import mysql.connector

from db import connectar


def disponibles(cn, llibre_id: int) -> int:
    with closing(cn.cursor()) as cur:
        cur.execute("SELECT disponibles FROM llibre WHERE id = %s", (llibre_id,))
        return cur.fetchone()[0]


def fer_prestec(cn, soci_id: int, llibre_id: int) -> int:
    """Retorna l'id del prestec. Si alguna cosa falla, no queda res fet."""
    cur = cn.cursor()
    try:
        # Pas 1: nomes resta si en queda algun (la condicio evita negatius)
        cur.execute("UPDATE llibre SET disponibles = disponibles - 1 "
                    "WHERE id = %s AND disponibles > 0", (llibre_id,))
        if cur.rowcount == 0:
            raise ValueError("no queden exemplars d'aquest llibre")

        # Pas 2: apuntar el prestec (falla si el soci no existeix: FK)
        cur.execute("INSERT INTO prestec (soci_id, llibre_id, data_prestec) "
                    "VALUES (%s, %s, %s)", (soci_id, llibre_id, date.today()))
        prestec_id = cur.lastrowid

        cn.commit()                    # tot be: es guarden ELS DOS passos
        return prestec_id
    except (mysql.connector.Error, ValueError):
        cn.rollback()                  # alguna cosa ha fallat: es desfan ELS DOS
        raise                          # i avisem a qui ens ha cridat
    finally:
        cur.close()


def retornar(cn, prestec_id: int) -> None:
    """L'operacio inversa, tambe en una sola transaccio."""
    with closing(cn.cursor()) as cur:
        try:
            cur.execute("UPDATE prestec SET data_retorn = %s "
                        "WHERE id = %s AND data_retorn IS NULL", (date.today(), prestec_id))
            cur.execute("UPDATE llibre SET disponibles = disponibles + 1 "
                        "WHERE id = (SELECT llibre_id FROM prestec WHERE id = %s)", (prestec_id,))
            cn.commit()
        except mysql.connector.Error:
            cn.rollback()
            raise


def esborrar_prestec(cn, prestec_id: int) -> None:
    """Neteja per poder repetir l'exemple."""
    with closing(cn.cursor()) as cur:
        cur.execute("DELETE FROM prestec WHERE id = %s", (prestec_id,))
        cn.commit()


if __name__ == "__main__":
    with closing(connectar()) as cn:
        print("--- 1) Prestec correcte ---")
        print("disponibles abans :", disponibles(cn, 3))
        nou = fer_prestec(cn, soci_id=3, llibre_id=3)
        print(f"prestec {nou} fet -> disponibles: {disponibles(cn, 3)}")

        print("\n--- 2) Falla el pas 1: no queden exemplars ---")
        try:
            fer_prestec(cn, soci_id=3, llibre_id=5)
        except ValueError as e:
            print("rebutjat:", e)

        print("\n--- 3) Falla el pas 2: el soci 999 no existeix ---")
        print("disponibles abans :", disponibles(cn, 3))
        try:
            fer_prestec(cn, soci_id=999, llibre_id=3)
        except mysql.connector.Error as e:
            print(f"error {e.errno} al pas 2 -> rollback")
        print("disponibles despres:", disponibles(cn, 3), "<- el pas 1 tambe s'ha desfet")

        print("\n--- 4) Retornar i deixar-ho tot com estava ---")
        retornar(cn, nou)
        print("retornat -> disponibles:", disponibles(cn, 3))
        esborrar_prestec(cn, nou)
