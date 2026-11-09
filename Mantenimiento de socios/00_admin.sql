-- 00_admin.sql  ->  L'executa UN COP l'administrador (root) al MySQL Workbench.
-- Prepara la base de dades i un usuari amb els permisos justos per a la RA2.

CREATE DATABASE IF NOT EXISTS biblioteca
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- '%' = des de qualsevol maquina de la xarxa (el servidor es a una altra IP).
CREATE USER IF NOT EXISTS 'alumne'@'%' IDENTIFIED BY '123456';

-- Tots els permisos, pero NOMES sobre la BD biblioteca (no sobre el servidor).
-- Inclou CREATE, DROP, CREATE ROUTINE, EXECUTE... el que necessiten c05 i c11.
GRANT ALL PRIVILEGES ON biblioteca.* TO 'alumne'@'%';

-- Nomes cal si c11 diu "errno 1419": permet crear FUNCTIONS amb el
-- registre binari actiu (opcio per defecte a MySQL 8).
SET GLOBAL log_bin_trust_function_creators = 1;
