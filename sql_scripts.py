import mysql.connector
from mysql.connector import errorcode

# Realiza la conexión con la base de datos
def try_conn():
    try:
        cnx = mysql.connector.connect(user='unai', password='unai1234', database='gastrolab')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuario o constraseña incorrectos!")
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Base de datos no existe!")
            return
        else:
            print(err)
            return
    else:
        return cnx

def close_conn(conexion, cursor):
    conexion.close()
    cursor.close()
    return

def validate_user(user, psw):
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    
    query = "SELECT nombre, contrasena FROM usuario WHERE nombre = %s AND contrasena = %s"
    values = (user, psw)
    
    CURSOR.execute(query, values)
    result = CURSOR.fetchone()
    close_conn(CONEXION, CURSOR)
    
    if result is None:
        return False
    return True

def is_admin(user):
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    
    query = "SELECT id_rol FROM usuario WHERE nombre = %s"
    values = (user,)
    
    CURSOR.execute(query, values)
    result = CURSOR.fetchone()
    close_conn(CONEXION, CURSOR)
    
    if result is None:
        return False
    if result[0] != 1:
        return False
    return True

def fetch_recepies_info():
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    
    query = """
    SELECT r.nombre, r.imagen, r.tipo, u.nombre
    FROM receta r INNER JOIN usuario u ON r.id_usuario = u.id_usuario
    """
    CURSOR.execute(query)
    result = CURSOR.fetchall()
    close_conn(CONEXION, CURSOR)
    
    if result is None:
        return
    return result

def insert_recepie(nombre, img, desc, pasos, tiempo_prep, tipo, user_id):
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    query = """
    INSERT INTO receta (nombre, imagen, descripcion, pasos, tiempo_preparacion, tipo, id_usuario) VALUES
    (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (nombre, img, desc, pasos, tiempo_prep, tipo, user_id)
    
    CURSOR.execute(query, values)
    CONEXION.commit()
    close_conn(CURSOR, CONEXION)
    print("datos insertados!")


if __name__ == "__main__":
    insert_recepie("prueba", "none", "Esto es una receta de prueba", "1. Paso1""2. Paso2""3.Paso3", 60, "normal", 1)
