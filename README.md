# Sistema de Gestión de Tareas con API REST y Cliente de Consola

Este proyecto implementa una API REST simple utilizando Flask para gestionar usuarios y sus tareas. Incluye un cliente de consola interactivo para facilitar el uso de la API.

## Características

- **API REST Completa**: Endpoints para registro, login, creación de tareas y consulta de tareas por usuario.
- **Cliente de Consola Interactivo**: Un script `client.py` que permite interactuar con la API de forma sencilla.
- **Persistencia de Datos**: Uso de SQLite para almacenar la información de usuarios y tareas.
- **Seguridad**: Almacenamiento de contraseñas de forma segura utilizando hashing.

## Tecnologías Utilizadas

- **Backend**: Python, Flask
- **Base de Datos**: SQLite
- **Cliente**: Python, requests, getpass

## Instalación y Puesta en Marcha

1.  **Clonar el repositorio (o descargar los archivos).**

2.  **Crear y activar un entorno virtual:** Es una buena práctica para aislar las dependencias.
    ```bash
    # Crear el entorno
    python -m venv .venv
    # Activar en Windows
    .\.venv\Scripts\activate
    # Activar en macOS/Linux
    # source .venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el Servidor:**
    Esto iniciará la API en `http://127.0.0.1:5000` y creará la base de datos `database.db` si no existe.
    ```bash
    python server.py
    ```

5.  **Ejecutar el Cliente:**
    En una **segunda terminal** (manteniendo el servidor corriendo), ejecuta el cliente interactivo.
    ```bash
    python client.py
    ```

## Uso del Cliente Interactivo

Una vez que el cliente está en marcha, verás un menú que te permitirá:
1.  **Registrarte**: Crea una nueva cuenta de usuario.
2.  **Iniciar Sesión (Login)**: Accede a tu cuenta. Al hacerlo, entrarás a un segundo menú donde podrás:
    - **Ver tus tareas**: Lista todas las tareas que has creado.
    - **Crear una nueva tarea**: Agrega una nueva tarea a tu lista.
    - **Cerrar sesión**: Volver al menú principal.
3.  **Salir**: Terminar el programa cliente.

## Documentación de la API (Para uso con Thunder Client, etc.)

### Autenticación

| Endpoint | Método | Descripción | Body (JSON) | Respuesta Exitosa (200 OK) |
| :--- | :--- | :--- | :--- | :--- |
| `/registro` | `POST` | Registra un nuevo usuario. | `{"usuario": "u", "contraseña": "p"}` | `{"message": "Usuario registrado..."}` |
| `/login` | `POST` | Inicia sesión. | `{"usuario": "u", "contraseña": "p"}` | `{"message": "Inicio de sesión...", "user_id": 1}` |

### Tareas

| Endpoint | Método | Descripción | Body (JSON) | Respuesta Exitosa (200 OK) |
| :--- | :--- | :--- | :--- | :--- |
| `/tareas` | `POST` | Crea una nueva tarea. | `{"title": "t", "description": "d", "user_id": 1}` | `{"message": "Tarea creada..."}` |
| `/tareas/<id>`| `GET` | Obtiene todas las tareas de un usuario. | (Ninguno) | `[{"id": 1, "title": "t", ...}]` |
