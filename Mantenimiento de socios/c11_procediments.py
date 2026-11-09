"""Criteri 2.11 - Executar procediments emmagatzemats a la base de dades.

    python c11_procediments.py

Un procediment emmagatzemat es codi que viu DINS de MySQL. Es crea un cop
i el pot cridar qualsevol aplicacio (Python, Java, PHP...).

    PROCEDURE -> es crida amb cursor.callproc(); pot tenir parametres OUT
    FUNCTION  -> retorna un valor i s'usa dins d'un SELECT

Nota: el DELIMITER $$ del MySQL Workbench NO s'escriu des de Python.
Es una ordre del client, no del servidor: enviem el CREATE sencer d'un cop.
"""
from contextlib import closing

import mysql.connector

from db import connectar

# Fa el mateix que fer_prestec() de c10, pero dins del servidor.
SP_PRESTAR = """
CREATE PROCEDURE sp_prestar(IN p_soci INT, IN p_llibre INT, OUT p_prestec INT)
BEGIN
    DECLARE v_disp INT;
    SELECT disponibles INTO v_disp FROM llibre WHERE id = p_llibre FOR UPDATE;

    IF v_disp IS NULL OR v_disp = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No queden exemplars';
    END IF;

    UPDATE llibre SET disponibles = disponibles - 1 WHERE id = p_llibre;
    INSERT INTO prestec (soci_id, llibre_id, data_prestec)
         VALUES (p_soci, p_llibre, CURDATE());
    SET p_prestec = LAST_INSERT_ID();
END"""

# Retorna files (un SELECT) en lloc d'un parametre OUT.
SP_HISTORIAL = """
CREATE PROCEDURE sp_historial(IN p_soci INT)
BEGIN
    SELECT l.titol, p.data_prestec, p.data_retorn
      FROM prestec p JOIN llibre l ON l.id = p.llibre_id
     WHERE p.soci_id = p_soci
     ORDER BY p.data_prestec;
END"""

FN_PENDENTS = """
CREATE FUNCTION fn_pendents(p_soci INT) RETURNS INT
DETERMINISTIC READS SQL DATA
BEGIN
    RETURN (SELECT COUNT(*) FROM prestec
             WHERE soci_id = p_soci AND data_retorn IS NULL);
END"""


def crear_rutines(cur) -> None:
    """CREATE PROCEDURE falla si ja existeix: primer DROP ... IF EXISTS."""
    for tipus, nom, codi in (("PROCEDURE", "sp_prestar", SP_PRESTAR),
                             ("PROCEDURE", "sp_historial", SP_HISTORIAL),
                             ("FUNCTION", "fn_pendents", FN_PENDENTS)):
        cur.execute(f"DROP {tipus} IF EXISTS {nom}")
        try:
            cur.execute(codi)
            print(f"{tipus:<9} {nom} creat")
        except mysql.connector.Error as e:
            # 1419: el servidor te el registre binari actiu i no confia en
            # funcions creades per usuaris normals. Ho arregla l'admin un cop:
            #   SET GLOBAL log_bin_trust_function_creators = 1;   (00_admin.sql)
            print(f"{tipus:<9} {nom} NO creat -> errno {e.errno}: mira 00_admin.sql")


def cridar_amb_out(cn, cur) -> int:
    """callproc() retorna els parametres; els OUT ja venen omplerts."""
    print("\n--- callproc amb parametre OUT ---")
    resultat = cur.callproc("sp_prestar", (3, 6, 0))   # el 0 es nomes un lloc pel OUT
    cn.commit()
    print("callproc ha retornat:", resultat, "-> id del prestec =", resultat[2])
    return resultat[2]


def quan_el_procediment_diu_que_no(cn, cur) -> None:
    """El SIGNAL del procediment arriba a Python com una excepcio normal."""
    print("\n--- El procediment rebutja l'operacio ---")
    try:
        cur.callproc("sp_prestar", (3, 5, 0))           # llibre 5: 0 exemplars
        cn.commit()
    except mysql.connector.Error as e:
        cn.rollback()
        print(f"rebutjat: sqlstate {e.sqlstate} -> {e.msg}")


def procediment_que_retorna_files(cur) -> None:
    """Els SELECT de dins del procediment es llegeixen amb stored_results().

    Amb el connector 9.x funciona sense avisos. Les versions mes noves mostren
    un DeprecationWarning (sera una propietat), pero el resultat es el mateix.
    """
    print("\n--- Procediment que retorna files ---")
    cur.callproc("sp_historial", (1,))
    for resultat in cur.stored_results():
        for titol, data_p, data_r in resultat.fetchall():
            print(f"  {titol:<24} {data_p}  retornat: {data_r or 'no'}")


def cridar_funcio(cur) -> None:
    """Una FUNCTION es fa servir com qualsevol funcio SQL (COUNT, UPPER...)."""
    print("\n--- Funcio dins d'un SELECT ---")
    cur.execute("SELECT COUNT(*) FROM information_schema.ROUTINES "
                "WHERE ROUTINE_SCHEMA = DATABASE() AND ROUTINE_NAME = 'fn_pendents'")
    if cur.fetchone()[0] == 0:
        print("  fn_pendents no existeix (executa 00_admin.sql com a root)")
        return
    cur.execute("SELECT nom, fn_pendents(id) FROM soci ORDER BY id")
    for nom, n in cur.fetchall():
        print(f"  {nom:<12} {n} prestec(s) pendent(s)")


if __name__ == "__main__":
    with closing(connectar()) as cn, closing(cn.cursor()) as cur:
        crear_rutines(cur)
        nou = cridar_amb_out(cn, cur)
        quan_el_procediment_diu_que_no(cn, cur)
        procediment_que_retorna_files(cur)
        cridar_funcio(cur)

        # Neteja (criteri 2.9): desfem el prestec de prova
        cur.execute("DELETE FROM prestec WHERE id = %s", (nou,))
        cur.execute("UPDATE llibre SET disponibles = disponibles + 1 WHERE id = 6")
        cn.commit()
        print(f"\nprestec de prova {nou} esborrat")
