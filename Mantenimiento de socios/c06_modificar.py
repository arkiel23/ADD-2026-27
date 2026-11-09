"""Criteri 2.6 - Aplicacions que modifiquen el contingut de la BD.

    python c06_modificar.py

INSERT, UPDATE i DELETE des de Python. Tres regles:
  1. Sempre amb parametres %s, mai concatenant text.
  2. Despres de modificar: commit() perque quedi guardat.
  3. Mirar rowcount / lastrowid per saber que ha passat de veritat.
El fitxer deixa la BD com l'ha trobat: es pot repetir.
"""
from contextlib import closing

import mysql.connector

from db import connectar


def alta_soci(cn, nom: str, email: str) -> int:
    """INSERT d'una fila. Retorna l'id que li ha donat AUTO_INCREMENT."""
    with closing(cn.cursor()) as cur:
        cur.execute("INSERT INTO soci (nom, email) VALUES (%s, %s)", (nom, email))
        cn.commit() #Sin el cn.commit no sirve de nada el execute
        return cur.lastrowid


def alta_llibres(cn, llibres: list) -> int:
    """Moltes files d'un cop amb executemany(). Retorna quantes s'han inserit."""
    with closing(cn.cursor()) as cur:
        cur.executemany("INSERT INTO llibre (titol, any_pub, disponibles, autor_id) "
                        "VALUES (%s, %s, %s, %s)", llibres)
        cn.commit()
        return cur.rowcount

def alta_autor(cn, nom: str, pais: str) -> int:
    """INSERT d'un autor. Retorna l'id que li ha donat AUTO_INCREMENT."""
    with closing(cn.cursor()) as cur:
        cur.execute("INSERT INTO autor (nom, pais) VALUES (%s, %s)", (nom, pais))
        cn.commit()
        return cur.lastrowid


def canviar_email(cn, soci_id: int, nou_email: str) -> bool:
    """UPDATE. rowcount diu quantes files han canviat (0 = no existia)."""
    with closing(cn.cursor()) as cur:
        cur.execute("UPDATE soci SET email = %s WHERE id = %s", (nou_email, soci_id))
        cn.commit()
        return cur.rowcount == 1


def esborrar_soci(cn, soci_id: int) -> bool:
    with closing(cn.cursor()) as cur:
        cur.execute("DELETE FROM soci WHERE id = %s", (soci_id,))
        cn.commit()
        return cur.rowcount == 1


def esborrar_autor(cn, autor_id: int) -> None:
    """Les claus foranes protegeixen les dades: no pots esborrar un autor
    que encara te llibres. MySQL respon amb un IntegrityError (errno 1451)."""
    try:
        with closing(cn.cursor()) as cur:
            cur.execute("DELETE FROM autor WHERE id = %s", (autor_id,))
            cn.commit()
            print("autor esborrat")
    except mysql.connector.IntegrityError as e:
        cn.rollback() #La execució no es fa bé y tornem a enrere
        print(f"no es pot esborrar l'autor {autor_id}: errno {e.errno} (te llibres)")


if __name__ == "__main__":
    with closing(connectar()) as cn:
        nou = alta_soci(cn, "Pau Ferrer", "pau@exemple.cat")
        print("INSERT   -> nou soci amb id", nou)

        n = alta_llibres(cn, [("El temps de les cireres", 1977, 2, 1),
                              ("Les veus del Pamano", 2004, 1, 2)])
        print("INSERT x2 -> files inserides:", n)

        print("UPDATE   -> email canviat?", canviar_email(cn, nou, "pau.f@exemple.cat"))
        print("UPDATE   -> soci 999 existeix?", canviar_email(cn, 999, "x@x.cat"))

        esborrar_autor(cn, 1)

        # Neteja: deixem la BD com estava (criteri 2.9)
        print("DELETE   -> soci esborrat?", esborrar_soci(cn, nou))
        with closing(cn.cursor()) as cur:
            cur.execute("DELETE FROM llibre WHERE titol IN (%s, %s)",
                        ("El temps de les cireres", "Les veus del Pamano"))
            cn.commit()
            print("DELETE   -> llibres de prova esborrats:", cur.rowcount)

        Nou_Autor = alta_autor(cn, "Pau Gómez", "Catalunya")
        print("INSERT   -> nou autor", Nou_Autor)

        esborrar_autor(cn, Nou_Autor)