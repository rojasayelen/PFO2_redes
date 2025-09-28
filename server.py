import sys
import os
import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Environment Check
if sys.prefix == sys.base_prefix:
    print("ERROR: You are not in a virtual environment. Please activate it.")
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Scripts', 'activate')
    print(f"Run this command to activate it: {venv_path}")
    sys.exit(1)

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Modified init_db to create the tasks table
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'pendiente',
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
    print("Base de datos inicializada y tablas 'users' y 'tasks' creadas/verificadas.")

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'message': 'Faltan datos'}), 400

    username = data['usuario']
    password = data['contraseña']
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    try:
        with conn:
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed_password)
            )
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'El nombre de usuario ya existe'}), 409
    except Exception as e:
        return jsonify({'message': f'Error en el servidor: {e}'}), 500

# Modified /login to return user_id
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'message': 'Faltan datos'}), 400

    username = data['usuario']
    password = data['contraseña']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user['id']}), 200
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

@app.route('/tareas', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'titulo' not in data or 'user_id' not in data:
        return jsonify({'message': 'Faltan datos: se requiere título y user_id'}), 400

    title = data['titulo']
    description = data.get('descripcion', '')
    user_id = data['user_id']

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO tasks (titulo, descripcion, user_id) VALUES (?, ?, ?)',
            (title, description, user_id)
        )
        conn.commit() # Explicitly commit the transaction
        return jsonify({'message': 'Tarea creada exitosamente'}), 201
    except Exception as e:
        conn.rollback() # Roll back the transaction on error
        return jsonify({'message': f'Error en el servidor: {e}'}), 500
    finally:
        conn.close() # Ensure the connection is always closed

# Modified endpoint to get tasks for a user
@app.route('/tareas/<int:user_id>', methods=['GET'])
def get_tasks(user_id):
    conn = get_db_connection()
    tasks_cursor = conn.execute('SELECT id, titulo, descripcion, status FROM tareas WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    tasks = [dict(row) for row in tasks_cursor]
    return jsonify(tasks), 200

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
