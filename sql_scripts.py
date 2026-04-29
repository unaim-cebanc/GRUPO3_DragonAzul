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

if __name__ == "__main__":
    recetas = fetch_recepies_info()
    print(recetas)