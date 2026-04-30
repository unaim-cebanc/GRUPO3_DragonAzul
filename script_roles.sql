# Creación de rol y permisos
CREATE ROLE 'ADMIN_ROL';
GRANT SELECT, INSERT, DELETE, UPDATE ON gastrolab.* TO 'ADMIN_ROL';
CREATE ROLE "USUARIO_ROL";
GRANT SELECT, INSERT ON gastrolab.ingrediente TO "USUARIO_ROL";
GRANT SELECT, INSERT ON gastrolab.menu TO "USUARIO_ROL";
GRANT SELECT, INSERT ON gastrolab.receta TO "USUARIO_ROL";
GRANT SELECT, INSERT ON gastrolab.usuario TO "USUARIO_ROL";
GRANT SELECT, INSERT ON gastrolab.valoracion TO "USUARIO_ROL";


# Creación de usuario y asignación
CREATE USER 'unai'@'%' IDENTIFIED BY 'unai1234';
CREATE USER 'marko'@'%' IDENTIFIED BY 'marko1234';
CREATE USER 'peru'@'%' IDENTIFIED BY 'peru1234';
CREATE USER 'marta'@'%' IDENTIFIED BY 'marta1234';
CREATE USER "usuario"@"%" IDENTIFIED BY "usuario1234";

-- crear rol aparte que pueda hacer solo lo basico, usuario q en principio utiliza la pagina web, solamente acceso a lo básico --

GRANT 'ADMIN_ROL' TO 'unai'@'%';
GRANT 'ADMIN_ROL' TO 'marko'@'%';
GRANT 'ADMIN_ROL' TO 'peru'@'%';
GRANT 'ADMIN_ROL' TO 'marta'@'%';
GRANT "USUARIO_ROL" TO "usuario"@"%";
GRANT USAGE ON gastrolab.* TO 'ADMIN_ROL';
SET DEFAULT ROLE ALL TO 'unai'@'%';
SET DEFAULT ROLE ALL TO 'marko'@'%';
SET DEFAULT ROLE ALL TO 'peru'@'%';
SET DEFAULT ROLE ALL TO 'marta'@'%';

