"""Criteri 2.8 - Aplicacions que fan consultes.

    python c08_consultes.py

fetchone()  -> una fila (o None)
fetchall()  -> totes les files en una llista
fetchmany(n)-> les n seguents (per paginar sense carregar-ho tot)
Les consultes interessants uneixen taules: JOIN.
"""
from contextlib import closing

from db import connectar


def comptar_llibres(cn) -> int:
    """fetchone(): quan el resultat es una sola fila."""
    with closing(cn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM llibre")
        return cur.fetchone()[0]


def cercar_per_titol(cn, text: str) -> list:
    """Cerca parametritzada. El % del LIKE va DINS del parametre, no al SQL."""
    with closing(cn.cursor()) as cur:
        cur.execute("SELECT titol, any_pub FROM llibre WHERE titol LIKE %s",
                    (f"%{text}%",))
        return cur.fetchall()


def prestecs_pendents(cn) -> list:
    """JOIN de 3 taules: qui te QUIN llibre i des de quan."""
    with closing(cn.cursor(dictionary=True)) as cur: # Con dictionary=True, cada fila es un diccionario y accedes por nombre de columna:
        cur.execute("""
            SELECT s.nom AS soci, l.titol, p.data_prestec
              FROM prestec p
              JOIN soci   s ON s.id = p.soci_id
              JOIN llibre l ON l.id = p.llibre_id
             WHERE p.data_retorn IS NULL
             ORDER BY p.data_prestec""")
        return cur.fetchall()


def prestecs_per_soci(cn) -> list:
    """LEFT JOIN + GROUP BY: tambe surten els socis amb 0 prestecs."""
    with closing(cn.cursor()) as cur:
        cur.execute("""
            SELECT s.nom, COUNT(p.id), s.email l.llibre AS total
            FROM soci s LEFT JOIN prestec p ON p.soci_id = s.id
            LEFT JOIN Llibre l ON l.llibre id = p.llibre_id
            GROUP BY s.id, s.nom s.email
            ORDER BY total DESC""")
        return cur.fetchall()


def escribir_Correo(nom, email, llibre):
    print(f"Querido {nom} {email} {llibre}, debe usted un libro")

def llistar_paginat(cn, mida: int = 2) -> None:
    """fetchmany(): portem les files a trossos, com faria un backend amb pagines."""
    with closing(cn.cursor()) as cur:
        cur.execute("SELECT titol FROM llibre ORDER BY titol")
        pagina = 1
        while files := cur.fetchmany(mida): # Operador walrus, En Python, una lista vacía cuenta como falsa y una lista con elementos cuenta como verdadera.
            # files := cur.fetchmany(2) significa: guarda el resultado en files y, además, úsalo como condición. En cada vuelta:
            print(f"  pagina {pagina}:", [f[0] for f in files])
            pagina += 1


if __name__ == "__main__":
    with closing(connectar()) as cn:
        print("llibres en total:", comptar_llibres(cn))
        peli = "robot"
        print("cerca", peli, " : ", cercar_per_titol(cn, peli))
        print("\nprestecs pendents:")
        for p in prestecs_pendents(cn):
            print(f"  {p['soci']:<12} {p['titol']:<24} des del {p['data_prestec']}")
        print("\nprestecs per soci:")
        for nom, total, email, llibre in prestecs_per_soci(cn):
            if(total>0):
                escribir_Correo(nom, email)
            print(f"  {nom:<12} {total} {email} {llibre}")
        print("\nllibres paginats de 2 en 2:")
        llistar_paginat(cn)
