import requests
import getpass

BASE_URL = 'http://127.0.0.1:5000'

def register():
    """Registers a new user."""
    username = input("Ingrese un usuario: ")
    password = getpass.getpass("Ingrese contraseña: ")
    try:
        response = requests.post(f"{BASE_URL}/registro", json={{'usuario': username, 'contraseña': password}})
        print(f"Respuesta del servidor: {response.json().get('message', 'No se recibió mensaje')}")
    except requests.exceptions.RequestException as e:
        print(f"Ha ocurrido un error: {e}")

def login():
    """Logs in a user and returns the user_id if successful."""
    username = input("Ingrese el usuario: ")
    password = getpass.getpass("Ingrese la contraseña: ")
    try:
        response = requests.post(f"{BASE_URL}/login", json={{'usuario': username, 'contraseña': password}})
        data = response.json()
        print(f"Respuesta del servidor: {data.get('message', 'No se recibió un mensaje')}")
        
        if response.status_code == 200 and 'user_id' in data:
            return data['user_id']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ha ocurrido un error: {e}")
        return None

def view_tasks(user_id):
    """Fetches and displays tasks for the logged-in user."""
    try:
        response = requests.get(f"{BASE_URL}/tareas/{user_id}")
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                print("No existen tareas.")
            else:
                print("\n--- Tus tareas ---")
                for task in tasks:
                    print(f"  ID: {task['id']}, Status: {task['status']}")
                    print(f"  Titulo: {task['title']}")
                    if task['description']:
                        print(f"  Descripcion: {task['description']}")
                    print("-" * 20)
        else:
            print(f"Error al obtener tareas: {response.json().get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Ha ocurrido un error: {e}")

def create_task(user_id):
    """Prompts user for task details and sends them to the server."""
    print("\n--- Crear una nueva tarea ---")
    title = input("Titulo: ")
    description = input("Descripcion (opcional): ")
    if not title:
        print("El titulo no puede estar vacio.")
        return

    payload = {{
        'title': title,
        'description': description,
        'user_id': user_id
    }}
    
    try:
        response = requests.post(f"{BASE_URL}/tareas", json=payload)
        print(f"Respuesta del servidor: {response.json().get('message', 'No se recibió mensaje')}")
    except requests.exceptions.RequestException as e:
        print(f"Ha ocurrido un error: {e}")

def logged_in_menu(user_id):
    """Displays the menu for a logged-in user."""
    while True:
        print("\n--- Menú (ud está logueado) ---")
        print("1. Ver tareas")
        print("2. Crear una nueva tarea")
        print("3. Cerrar sesión")
        choice = input("Ingrese una opción: ")

        if choice == '1':
            view_tasks(user_id)
        elif choice == '2':
            create_task(user_id)
        elif choice == '3':
            print("Cerrando sesión.")
            break
        else:
            print("Opcion inválida. Por favor seleccione otra opcion.")

def main():
    """Main function to run the client."""
    while True:
        print("\n--- Menu Principal ---")
        print("1. Registro")
        print("2. Login")
        print("3. Salir")
        choice = input("Ingrese una opcion: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                logged_in_menu(user_id)
        elif choice == '3':
            break
        else:
            print("Opcion inválida. Intentelo nuevamente.")

if __name__ == '__main__':
    main()
