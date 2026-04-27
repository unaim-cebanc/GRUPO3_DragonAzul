--  GASTROLAB - Base de Datos
--  Archivo: gastrolab.sql

CREATE DATABASE IF NOT EXISTS gastrolab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gastrolab;

-- TABLAS

CREATE TABLE IF NOT EXISTS rol (
    id_rol      INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    contrasena      VARCHAR(255) NOT NULL,
    id_rol          INT NOT NULL DEFAULT 2,
    fecha_registro  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE IF NOT EXISTS personal (
    id_personal     INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    puesto          VARCHAR(100),
    salario         DECIMAL(10,2),
    id_usuario      INT UNIQUE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS nomina (
    id_nomina       INT AUTO_INCREMENT PRIMARY KEY,
    id_personal     INT NOT NULL,
    fecha           DATE NOT NULL,
    salario_base    DECIMAL(10,2) NOT NULL,
    extras          DECIMAL(10,2) DEFAULT 0,
    total           DECIMAL(10,2) GENERATED ALWAYS AS (salario_base + extras) STORED,
    FOREIGN KEY (id_personal) REFERENCES personal(id_personal)
);

CREATE TABLE IF NOT EXISTS receta (
    id_receta           INT AUTO_INCREMENT PRIMARY KEY,
    nombre              VARCHAR(150) NOT NULL,
    descripcion         TEXT,
    pasos               TEXT,
    tiempo_preparacion  INT,
    tipo                ENUM('normal','vegetariana','vegana') DEFAULT 'normal',
    id_usuario          INT,
    fecha_creacion      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS ingrediente (
    id_ingrediente  INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL UNIQUE,
    calorias        DECIMAL(8,2)
);

CREATE TABLE IF NOT EXISTS receta_ingrediente (
    id_receta       INT NOT NULL,
    id_ingrediente  INT NOT NULL,
    cantidad        DECIMAL(8,2),
    unidad          VARCHAR(30),
    PRIMARY KEY (id_receta, id_ingrediente),
    FOREIGN KEY (id_receta)      REFERENCES receta(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES ingrediente(id_ingrediente)
);

CREATE TABLE IF NOT EXISTS menu (
    id_menu     INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(150) NOT NULL,
    fecha       DATE,
    tipo        VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS menu_receta (
    id_menu     INT NOT NULL,
    id_receta   INT NOT NULL,
    PRIMARY KEY (id_menu, id_receta),
    FOREIGN KEY (id_menu)   REFERENCES menu(id_menu),
    FOREIGN KEY (id_receta) REFERENCES receta(id_receta)
);

CREATE TABLE IF NOT EXISTS valoracion (
    id_valoracion   INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario      INT NOT NULL,
    id_receta       INT NOT NULL,
    puntuacion      TINYINT NOT NULL CHECK (puntuacion BETWEEN 1 AND 5),
    comentario      TEXT,
    fecha           DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unico_voto (id_usuario, id_receta),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_receta)  REFERENCES receta(id_receta)
);

CREATE TABLE IF NOT EXISTS multimedia (
    id_multimedia   INT AUTO_INCREMENT PRIMARY KEY,
    titulo          VARCHAR(200) NOT NULL,
    tipo            VARCHAR(50),
    url             VARCHAR(500),
    exclusivo       BOOLEAN DEFAULT TRUE,
    fecha           DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- datos iniciales de roles
INSERT INTO rol (nombre) VALUES ('admin'), ('usuario'), ('alumno')
    ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);


-- VISTAS

-- recetas con su puntuacion media
CREATE OR REPLACE VIEW vista_recetas_valoradas AS
SELECT
    r.id_receta,
    r.nombre,
    r.tipo,
    r.tiempo_preparacion,
    u.nombre AS autor,
    ROUND(AVG(v.puntuacion), 2) AS media_puntuacion,
    COUNT(v.id_valoracion)      AS total_votos
FROM receta r
LEFT JOIN usuario    u ON r.id_usuario = u.id_usuario
LEFT JOIN valoracion v ON r.id_receta  = v.id_receta
GROUP BY r.id_receta, r.nombre, r.tipo, r.tiempo_preparacion, u.nombre;

-- solo las veganas ordenadas por puntuacion
CREATE OR REPLACE VIEW vista_recetas_veganas AS
SELECT * FROM vista_recetas_valoradas
WHERE tipo = 'vegana'
ORDER BY media_puntuacion DESC;

-- menu del dia de hoy
CREATE OR REPLACE VIEW vista_menu_hoy AS
SELECT
    m.nombre  AS menu,
    m.tipo,
    r.nombre  AS receta,
    r.tipo    AS tipo_receta
FROM menu m
JOIN menu_receta mr ON m.id_menu    = mr.id_menu
JOIN receta      r  ON mr.id_receta = r.id_receta
WHERE m.fecha = CURDATE();

-- nominas con nombre del empleado
CREATE OR REPLACE VIEW vista_nominas_personal AS
SELECT
    p.nombre AS empleado,
    p.puesto,
    n.fecha,
    n.salario_base,
    n.extras,
    n.total
FROM personal p
JOIN nomina n ON p.id_personal = n.id_personal
ORDER BY n.fecha DESC;

-- calorias totales por receta sumando todos sus ingredientes
CREATE OR REPLACE VIEW vista_calorias_receta AS
SELECT
    r.id_receta,
    r.nombre AS receta,
    r.tipo,
    SUM(i.calorias * ri.cantidad)   AS calorias_totales,
    COUNT(ri.id_ingrediente)        AS num_ingredientes
FROM receta r
JOIN receta_ingrediente ri ON r.id_receta       = ri.id_receta
JOIN ingrediente        i  ON ri.id_ingrediente = i.id_ingrediente
GROUP BY r.id_receta, r.nombre, r.tipo;

-- multimedia solo para usuarios registrados
CREATE OR REPLACE VIEW vista_multimedia_exclusiva AS
SELECT id_multimedia, titulo, tipo, url, fecha
FROM multimedia
WHERE exclusivo = TRUE;


-- CONTROL DE ACCESO (DCL)

-- usuario para alumnos, solo lectura de vistas publicas
CREATE USER IF NOT EXISTS 'gastro_lector'@'localhost' IDENTIFIED BY 'Lector_2024!';
GRANT SELECT ON gastrolab.vista_recetas_valoradas  TO 'gastro_lector'@'localhost';
GRANT SELECT ON gastrolab.vista_recetas_veganas    TO 'gastro_lector'@'localhost';
GRANT SELECT ON gastrolab.vista_menu_hoy           TO 'gastro_lector'@'localhost';

-- usuario registrado: puede ver recetas y dejar valoraciones
CREATE USER IF NOT EXISTS 'gastro_usuario'@'localhost' IDENTIFIED BY 'Usuario_2024!';
GRANT SELECT ON gastrolab.receta                     TO 'gastro_usuario'@'localhost';
GRANT SELECT ON gastrolab.vista_calorias_receta      TO 'gastro_usuario'@'localhost';
GRANT SELECT ON gastrolab.vista_multimedia_exclusiva TO 'gastro_usuario'@'localhost';
GRANT INSERT, UPDATE ON gastrolab.valoracion         TO 'gastro_usuario'@'localhost';
GRANT INSERT ON gastrolab.receta                     TO 'gastro_usuario'@'localhost';

-- admin: acceso completo
CREATE USER IF NOT EXISTS 'gastro_admin'@'localhost' IDENTIFIED BY 'Admin_2024!';
GRANT SELECT, INSERT, UPDATE, DELETE ON gastrolab.usuario    TO 'gastro_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON gastrolab.receta     TO 'gastro_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON gastrolab.personal   TO 'gastro_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON gastrolab.nomina     TO 'gastro_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON gastrolab.multimedia TO 'gastro_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON gastrolab.menu       TO 'gastro_admin'@'localhost';

FLUSH PRIVILEGES;


-- FUNCIONES

DELIMITER $$

-- devuelve las calorias totales de una receta
CREATE FUNCTION IF NOT EXISTS fn_calorias_receta(p_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10,2) DEFAULT 0;

    SELECT COALESCE(SUM(i.calorias * ri.cantidad), 0)
    INTO   total
    FROM   receta_ingrediente ri
    JOIN   ingrediente i ON ri.id_ingrediente = i.id_ingrediente
    WHERE  ri.id_receta = p_id;

    RETURN total;
END$$

-- clasifica una receta segun sus calorias
CREATE FUNCTION IF NOT EXISTS fn_categoria_calorica(p_calorias DECIMAL(10,2))
RETURNS VARCHAR(20)
DETERMINISTIC
NO SQL
BEGIN
    DECLARE categoria VARCHAR(20);

    IF p_calorias < 300 THEN
        SET categoria = 'ligera';
    ELSEIF p_calorias < 700 THEN
        SET categoria = 'media';
    ELSE
        SET categoria = 'contundente';
    END IF;

    RETURN categoria;
END$$

DELIMITER ;


-- TRIGGERS

DELIMITER $$

-- comprueba que la puntuacion este entre 1 y 5 antes de insertar
CREATE TRIGGER IF NOT EXISTS antes_insertar_valoracion
BEFORE INSERT ON valoracion
FOR EACH ROW
BEGIN
    IF NEW.puntuacion < 1 OR NEW.puntuacion > 5 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La puntuacion debe estar entre 1 y 5';
    END IF;
END$$

-- no permite borrar un usuario si tiene recetas publicadas
CREATE TRIGGER IF NOT EXISTS antes_borrar_usuario
BEFORE DELETE ON usuario
FOR EACH ROW
BEGIN
    DECLARE total INT DEFAULT 0;

    SELECT COUNT(*) INTO total
    FROM receta WHERE id_usuario = OLD.id_usuario;

    IF total > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No se puede eliminar un usuario con recetas publicadas';
    END IF;
END$$

