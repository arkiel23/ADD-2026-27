
from contextlib import closing
import mysql.connector
from db import connectar


def alta_soci(cn, nom: str, email: str) -> int:
    """Inserta un socio y devuelve su ID."""
    with closing(cn.cursor()) as cur:
        cur.execute("INSERT INTO soci (nom, email) VALUES (%s, %s)", (nom, email))
        return cur.lastrowid


def canviar_nom(cn, id: int, nom: str) -> bool:
    """Cambia el nombre y comprueba si se modifico una fila."""
    with closing(cn.cursor()) as cur:
        cur.execute("UPDATE soci SET nom = %s WHERE id = %s", (nom, id))
        return cur.rowcount == 1


def baixa_soci(cn, id: int) -> bool:
    """Borra un socio si no tiene prestamos."""
    with closing(cn.cursor()) as cur:
        cur.execute("DELETE FROM soci WHERE id = %s", (id,))
        return cur.rowcount == 1


def main() -> None:
    with closing(connectar()) as cn:
        try:
            print("MANTENIMIENTO DE SOCIOS")
            nom = input("Nombre del socio nuevo: ")
            email = input("Email nuevo (no registrado): ")
            nou_nom = input("Nombre para modificarlo: ")

            print("\n1. ALTA")
            try:
                nou_id = alta_soci(cn, nom, email)
                print("ID del socio nuevo:", nou_id)
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:
                    print("Error 1062: el email ya existe.")
                    return
                raise

            print("\n2. EMAIL REPETIDO")
            try:
                alta_soci(cn, "Otro socio", email)
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:
                    print("Error 1062: el email ya existe.")
                else:
                    raise

            print("\n3. CAMBIAR NOMBRE")
            print("Socio existente:", canviar_nom(cn, nou_id, nou_nom))
            print("Socio inexistente:", canviar_nom(cn, -1, nou_nom))

            print("\n4. BAJA")
            with closing(cn.cursor()) as cur:
                cur.execute("SELECT soci_id FROM prestec LIMIT 1")
                prestec = cur.fetchone()
            if prestec:
                try:
                    baixa_soci(cn, prestec[0])
                except mysql.connector.IntegrityError as e:
                    if e.errno == 1451:
                        print("Error 1451: el socio tiene prestamos.")
                    else:
                        raise
            else:
                print("No hay prestamos para probar el error 1451.")
            print("Baja del socio nuevo:", baixa_soci(cn, nou_id))
        finally:
            cn.rollback()
            print("\nROLLBACK: se deshacen todos los cambios de la prueba.")


if __name__ == "__main__":
    main()
