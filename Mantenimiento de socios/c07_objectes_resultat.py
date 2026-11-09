"""Criteri 2.7 - Definir els objectes que emmagatzemen el resultat de les consultes.

    python c07_objectes_resultat.py

Una fila pot arribar a Python de tres maneres:
  1. tupla      -> fila[1]          (rapid, pero que era la posicio 1?)
  2. diccionari -> fila["titol"]    (llegible, depen del nom de la columna)
  3. objecte    -> llibre.titol     (una classe nostra: el que fa un backend)
"""
from contextlib import closing
from dataclasses import dataclass

from db import connectar

SQL = """SELECT l.id, l.titol, l.any_pub, l.disponibles, a.nom AS autor
           FROM llibre l JOIN autor a ON a.id = l.autor_id
          ORDER BY l.id"""


@dataclass
class Llibre:
    """La 'forma' d'un llibre dins del nostre programa."""
    id: int
    titol: str
    any_pub: int
    disponibles: int
    autor: str

    def es_pot_prestar(self) -> bool:
        return self.disponibles > 0


def com_a_tuples(cn) -> None:
    print("--- 1) Tuples (per defecte) ---")
    with closing(cn.cursor()) as cur:
        cur.execute(SQL)
        print("columnes:", cur.column_names)        # els noms, a part
        fila = cur.fetchone()
        print("fila    :", fila, "-> titol =", fila[1])
        cur.fetchall()     # llegir la resta abans de tancar (si no: 'Unread result')


def com_a_diccionaris(cn) -> None:
    print("\n--- 2) Diccionaris: cursor(dictionary=True) ---")
    with closing(cn.cursor(dictionary=True)) as cur:
        cur.execute(SQL)
        fila = cur.fetchall()[0]
        print("fila    :", fila)
        print("titol   :", fila["titol"])


def com_a_objectes(cn) -> list:
    print("\n--- 3) Objectes de la nostra classe Llibre ---")
    with closing(cn.cursor(dictionary=True)) as cur:
        cur.execute(SQL)
        # Cada diccionari es converteix en un Llibre: **fila reparteix les claus
        llibres = [Llibre(**fila) for fila in cur.fetchall()]
    for l in llibres:
        estat = "disponible" if l.es_pot_prestar() else "ESGOTAT"
        print(f"{l.titol:<24} {l.autor:<24} {estat}")
    return llibres


if __name__ == "__main__":
    with closing(connectar()) as cn:
        com_a_tuples(cn)
        com_a_diccionaris(cn)
        com_a_objectes(cn)
