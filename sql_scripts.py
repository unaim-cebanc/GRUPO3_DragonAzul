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

if __name__ == "__main__":
    
    usuario = input("Introduce tu nombre de usuario: ").strip().lower()
    contraseña = input("Introduce tu contraseña: ").strip()
    
    if validate_user(usuario, contraseña):
        if is_admin(usuario):
            print("Sesion iniciada como admin")
        else:
            print("Sesion iniciada como invitado")
    else:
        print("Credenciales incorrectas")