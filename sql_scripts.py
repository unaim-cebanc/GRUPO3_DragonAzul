import mysql.connector
from mysql.connector import errorcode
import bcrypt

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

def get_user_id(user):
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    
    query = "SELECT id_usuario FROM usuario WHERE nombre = %s"
    values = (user,)
    
    CURSOR.execute(query, values)
    result = CURSOR.fetchone()
    close_conn(CONEXION, CURSOR)
    
    if result is None:
        print("Usuario no encontrado!")
        return
    return int(result[0])

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

def insert_recepie(nombre, img, desc, ingredientes, cantidades, unidades, pasos, tiempo_prep, tipo, user_id):
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    
    query_receta = """
    INSERT INTO receta (nombre, imagen, descripcion, tiempo_preparacion, tipo, id_usuario) VALUES
    (%s, %s, %s, %s, %s, %s)
    """
    values_receta = (nombre, img, desc, tiempo_prep, tipo, user_id)
    
    CURSOR.execute(query_receta, values_receta)
    CONEXION.commit()
    
    query_id = "SELECT id_receta FROM receta WHERE nombre = %s AND id_usuario = %s"
    values_id = (nombre, user_id)
    CURSOR.execute(query_id, values_id)
    id_receta = CURSOR.fetchone()[0]
    CURSOR.fetchall()
    
    query_ingredientes = """
    INSERT INTO receta_ingrediente (id_receta, nombre, cantidad, unidad) VALUES (%s, %s, %s, %s)
    """
    values_ingredientes = [(id_receta, ing, qty, uni) for ing, qty, uni in zip(ingredientes, cantidades, unidades)]
    
    CURSOR.executemany(query_ingredientes, values_ingredientes)
    CONEXION.commit()
    
    query_pasos = """
    INSERT INTO pasos (id_receta, paso) VALUES (%s, %s)
    """
    values_pasos = [(id_receta, paso) for paso in pasos]
    
    CURSOR.executemany(query_pasos, values_pasos)
    CONEXION.commit()
    
    close_conn(CURSOR, CONEXION)
    print("datos insertados!")

def register_user(nombre, email, contrasena):
    CONEXION = try_conn()
    CURSOR = CONEXION.cursor()
    
    query = """
        INSERT INTO usuario (nombre, email, contrasena) VALUES (%s, %s, %s)
    """
    secure_psw = encrypt_password(contrasena)
    values = (nombre, email, secure_psw)
    
    CURSOR.execute(query, values)
    CONEXION.commit()
    print("Usuario registrado!")
    close_conn(CURSOR, CONEXION)

def encrypt_password(psw):
    salt = bcrypt.gensalt()
    psw_hash = bcrypt.hashpw(psw.encode("utf-8"), salt)
    return psw_hash

if __name__ == "__main__":
    usuario = input("usuario: ")
    psw = input("contraseña: ")
    email = input("email: ")
    register_user(usuario, email, psw)