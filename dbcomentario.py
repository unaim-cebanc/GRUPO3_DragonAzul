import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "tu_usuario",
    "password": "tu_contraseña",
    "database": "tu_base_de_datos"
}   

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def obtener_comentarios():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM valoracion ORDER BY fecha DESC")
    resultado = cursor.fetchall()
    cursor.close()
    db.close()
    return resultado

def insertar_comentario(nombre, mensaje, fecha):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO valoracion (nombre, mensaje, fecha) VALUES (%s, %s, %s)",
        (nombre, mensaje, fecha)
    )
    db.commit()
    cursor.close()
    db.close()