"""Criteri 2.9 - Eliminar els objectes un cop finalitzada la funcio.

    python c09_alliberar_recursos.py

Cada connexio oberta ocupa un fil al servidor (Threads_connected) i memoria.
Cada cursor pot tenir resultats pendents. Si no es tanquen, un backend que
rep milers de peticions acaba esgotant el servidor ("Too many connections").

Dues coses s'han d'eliminar:
  1. Els objectes de Python: cursors i connexions -> close()
  2. Els objectes temporals creats a la BD: vistes, taules temporals -> DROP
"""
from contextlib import closing

from db import connectar


def connexions_obertes(cur) -> int:
    cur.execute("SHOW STATUS LIKE 'Threads_connected'")
    return int(cur.fetchone()[1])


def forma_manual() -> None:
    """try/finally: el finally s'executa SEMPRE, fins i tot si hi ha excepcio."""
    print("--- 1) try / finally ---")
    cn = connectar()
    cur = cn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM soci")
        print("socis:", cur.fetchone()[0])
    finally:
        cur.close()             # primer el cursor...
        cn.close()              # ...despres la connexio
    print("connexio oberta?", cn.is_connected())


def forma_recomanada() -> None:
    """with closing(...): fa el mateix que el try/finally, en una linia."""
    print("\n--- 2) with closing() ---")
    with closing(connectar()) as cn, closing(cn.cursor()) as cur:
        cur.execute("SELECT COUNT(*) FROM llibre")
        print("llibres:", cur.fetchone()[0])
    print("connexio oberta?", cn.is_connected(), "<- tancada en sortir del with")


def la_fuita() -> None:
    """Que passa si obrim connexions i NO les tanquem."""
    print("\n--- 3) La fuita de connexions ---")
    with closing(connectar()) as control, closing(control.cursor()) as cur:
        abans = connexions_obertes(cur)
        oblidades = [connectar() for _ in range(5)]      # 5 connexions sense tancar
        print(f"abans: {abans}  ara: {connexions_obertes(cur)}  <- +5 fils al servidor")
        for cn in oblidades:
            cn.close()
        print(f"despres de tancar-les: {connexions_obertes(cur)}")


def objectes_temporals() -> None:
    """Una VISTA creada per a una tasca s'ha d'esborrar quan s'acaba.
    Una TEMPORARY TABLE s'esborra sola en tancar la connexio, pero millor fer-ho explicit."""
    print("\n--- 4) Objectes temporals a la BD ---")
    with closing(connectar()) as cn, closing(cn.cursor()) as cur:
        cur.execute("""CREATE OR REPLACE VIEW v_pendents AS
                       SELECT soci_id, llibre_id FROM prestec WHERE data_retorn IS NULL""")
        cur.execute("CREATE TEMPORARY TABLE tmp_resum AS "
                    "SELECT soci_id, COUNT(*) AS n FROM v_pendents GROUP BY soci_id")
        cur.execute("SELECT COUNT(*) FROM tmp_resum")
        print("socis amb prestecs pendents:", cur.fetchone()[0])

        cur.execute("DROP TEMPORARY TABLE IF EXISTS tmp_resum")
        cur.execute("DROP VIEW IF EXISTS v_pendents")
        cur.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        print("vistes que queden:", cur.fetchall() or "cap")


if __name__ == "__main__":
    forma_manual()
    forma_recomanada()
    la_fuita()
    objectes_temporals()
