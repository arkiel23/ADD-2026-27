"""Criteri 2.5 - Definir l'estructura de la base de dades.

    python c05_estructura.py      <- EXECUTA'L EL PRIMER

Crea la BD 'biblioteca', les 4 taules relacionades i unes dades d'exemple.
Es pot tornar a executar sempre que vulguis tornar al punt de partida.

    autor 1 ──< N llibre 1 ──< N prestec N >── 1 soci

Un autor te molts llibres. Un soci fa molts prestecs. Cada prestec
relaciona UN soci amb UN llibre (la taula prestec resol la relacio N:M).
"""
from contextlib import closing

from db import connectar

# L'ordre importa: primer les taules "mare", despres les que hi apunten.
TAULES = {
    "autor": """
        CREATE TABLE autor (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            nom   VARCHAR(100) NOT NULL,
            pais  VARCHAR(50)
        ) ENGINE=InnoDB""",
    "llibre": """
        CREATE TABLE llibre (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            titol        VARCHAR(150) NOT NULL,
            any_pub      SMALLINT,
            disponibles  INT NOT NULL DEFAULT 1 CHECK (disponibles >= 0),
            autor_id     INT NOT NULL,
            CONSTRAINT fk_llibre_autor FOREIGN KEY (autor_id) REFERENCES autor(id)
        ) ENGINE=InnoDB""",
    "soci": """
        CREATE TABLE soci (
            id     INT AUTO_INCREMENT PRIMARY KEY,
            nom    VARCHAR(100) NOT NULL,
            email  VARCHAR(120) NOT NULL UNIQUE
        ) ENGINE=InnoDB""",
    "prestec": """
        CREATE TABLE prestec (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            soci_id       INT  NOT NULL,
            llibre_id     INT  NOT NULL,
            data_prestec  DATE NOT NULL,
            data_retorn   DATE NULL,          -- NULL = encara no l'ha tornat
            CONSTRAINT fk_prestec_soci   FOREIGN KEY (soci_id)   REFERENCES soci(id),
            CONSTRAINT fk_prestec_llibre FOREIGN KEY (llibre_id) REFERENCES llibre(id)
        ) ENGINE=InnoDB""",
}

AUTORS = [("Mercè Rodoreda", "Catalunya"), ("Jaume Cabré", "Catalunya"),
          ("Isaac Asimov", "EUA"), ("Gabriel García Márquez", "Colòmbia")] # Esto es una tupla, grupo ordenado de valores que no se puede modificar después de crearlo

LLIBRES = [  # (titol, any, disponibles, autor_id)
    ("La plaça del Diamant", 1962, 3, 1),
    ("Mirall trencat", 1974, 1, 1),
    ("Jo confesso", 2011, 2, 2),
    ("Fundació", 1951, 2, 3),
    ("Jo, robot", 1950, 0, 3),            # 0 disponibles: servira a c10 i c11
    ("Cent anys de solitud", 1967, 4, 4),
]

SOCIS = [("Laia Puig", "laia@exemple.cat"), ("Marc Soler", "marc@exemple.cat"),
         ("Núria Vidal", "nuria@exemple.cat")]

PRESTECS = [  # (soci_id, llibre_id, data_prestec, data_retorn)
    (1, 1, "2026-09-01", "2026-09-15"),
    (1, 4, "2026-09-20", None),
    (2, 6, "2026-09-25", None),
]


def crear_base_de_dades() -> None:
    """Sense database= a la connexio: la BD encara pot no existir."""
    with closing(connectar(amb_bd=False)) as cn, closing(cn.cursor()) as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS biblioteca "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("1) BD 'biblioteca' a punt")

    #El with closing sirve para cerrar la conexion con la BD, sinó se quedaria abierta


def crear_taules(cur) -> None: # Cur es un parametro, el none es opcional y indica que la funcion no devuelve nada
    # Esborrar en ordre INVERS: si esborres 'autor' abans que 'llibre',
    # MySQL ho impedeix perque quedarien llibres apuntant a un autor inexistent.
    for nom in reversed(list(TAULES)):
        cur.execute(f"DROP TABLE IF EXISTS {nom}")
    for nom, ddl in TAULES.items():
        cur.execute(ddl)
        print(f"2) taula {nom} creada")


def inserir_dades(cn, cur) -> None: # La conexión (cn) es el canal con la base de datos. El cursor (cur) es el objeto que usas para enviar consultas y leer los resultados.
    # executemany(): una sola crida per a moltes files.
    cur.executemany("INSERT INTO autor (nom, pais) VALUES (%s, %s)", AUTORS)
    cur.executemany("INSERT INTO llibre (titol, any_pub, disponibles, autor_id) "
                    "VALUES (%s, %s, %s, %s)", LLIBRES)
    cur.executemany("INSERT INTO soci (nom, email) VALUES (%s, %s)", SOCIS)
    cur.executemany("INSERT INTO prestec (soci_id, llibre_id, data_prestec, data_retorn) "
                    "VALUES (%s, %s, %s, %s)", PRESTECS)
    cn.commit()    # el DDL fa commit sol; els INSERT NO. Sense aixo es perdrien.
    print("3) dades d'exemple inserides")


def mostrar_estructura(cur) -> None:
    """Comprovem l'estructura preguntant al SERVIDOR, no mirant el nostre codi."""
    print("\n--- Estructura real al servidor ---")
    cur.execute("SHOW TABLES")
    for (taula,) in cur.fetchall():
        cur.execute(f"SELECT COUNT(*) FROM {taula}")
        print(f"{taula:<8} {cur.fetchone()[0]} files")

    # Les claus foranes es consulten al cataleg de MySQL: information_schema.
    cur.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME
          FROM information_schema.KEY_COLUMN_USAGE
         WHERE TABLE_SCHEMA = DATABASE() AND REFERENCED_TABLE_NAME IS NOT NULL
         ORDER BY TABLE_NAME""")
    for taula, columna, referenciada in cur.fetchall():
        print(f"FK {taula}.{columna} -> {referenciada}.id")


if __name__ == "__main__":
    crear_base_de_dades()
    with closing(connectar()) as cn, closing(cn.cursor()) as cur:
        crear_taules(cur)
        inserir_dades(cn, cur)
        mostrar_estructura(cur)



# USO DEL FOR EN PYTHON, 
# nombres = ["Laia", "Marc", "Núria"]

# Esto es lo mas comun 
# for nombre in nombres:
#    print(nombre)

# Tambien se puede hacer asi
# for i, nombre in enumerate(nombres):
#    print(i, nombre)
# En python es muy importante la tabulación, si la haces mal el codigo puede no funcionar