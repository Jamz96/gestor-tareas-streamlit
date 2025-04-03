import sqlite3
import hashlib

# ======== Conexión ========
def conectar():
    conexion = sqlite3.connect("gestor_tareas.db")
    cursor = conexion.cursor()
    return conexion, cursor

# ======== Seguridad ========
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ======== Crear tablas (una sola vez) ========
def crear_tablas():
    conexion, cursor = conectar()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tarea TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    """)
    conexion.commit()
    conexion.close()

# ======== Operaciones sobre usuarios ========
def registrar_usuario(username, password):
    conexion, cursor = conectar()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conexion.commit()
        resultado = True
    except sqlite3.IntegrityError:
        resultado = False  # Usuario ya existe
    conexion.close()
    return resultado

def verificar_usuario(username, password):
    conexion, cursor = conectar()
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conexion.close()
    if resultado and hash_password(password) == resultado[0]:
        return True
    else:
        return False

def obtener_id_usuario(username):
    conexion, cursor = conectar()
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conexion.close()
    if resultado:
        return resultado[0]
    return None

# ======== Operaciones sobre tareas ========
def agregar_tarea(usuario_id, tarea):
    conexion, cursor = conectar()
    cursor.execute("INSERT INTO tareas (usuario_id, tarea) VALUES (?, ?)", 
                   (usuario_id, tarea))
    conexion.commit()
    conexion.close()

def obtener_tareas(usuario_id):
    conexion, cursor = conectar()
    cursor.execute("SELECT id, tarea FROM tareas WHERE usuario_id = ?", (usuario_id,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def eliminar_tarea(tarea_id):
    conexion, cursor = conectar()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
    conexion.commit()
    conexion.close()

def contar_tareas_por_usuario():
    conexion, cursor = conectar()
    cursor.execute("""
    SELECT usuarios.username, COUNT(tareas.id) 
    FROM usuarios
    LEFT JOIN tareas ON usuarios.id = tareas.usuario_id
    GROUP BY usuarios.username
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos
