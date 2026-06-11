# Gestor Universitario FIUBA — Frontend

Interfaz gráfica de usuario (Web) desarrollada con Flask y Jinja2 para la gestión de cursos universitarios.
Proyecto final de Introducción al Desarrollo de Software — Curso Lanzillota 2026.

> **⚙️ Backend:** Esta aplicación depende de la API REST del Backend. Asegurate de tener el [repositorio del Backend] corriendo en el puerto `8080` antes de iniciar el Frontend.

---

## Tecnologías

- **Python 3.12**
- **Flask** — web framework para el ruteo del frontend
- **Jinja2** — motor de plantillas (templates HTML)
- **HTML5 & CSS3** — maquetado y estilos (sin frameworks externos pesados)
- **Requests** — cliente HTTP para consumir la API del backend
- **python-dotenv** — gestión de variables de entorno

---

## Estructura del proyecto

```
front_ARMJSSS/
├── app/
│   ├── constants.py                        # Constantes globales (ej. URLs)
│   ├── routes/                             # Controladores de las vistas
│   │   ├── alumnos.py                      # Interfaz de gestión de alumnos
│   │   ├── asistencias.py                  # Generación y validación QR
│   │   ├── auth.py                         # Vistas de Login y Registro
│   │   ├── cursos.py                       # Interfaz de cursos 
│   │   ├── dashboard.py                    # Vista principal y estadísticas
│   │   ├── docentes.py                     # Interfaz de gestión de docentes
│   │   ├── equipos.py                      # Vistas de equipos y asignaciones
│   │   ├── evaluaciones.py                 # Vistas de evaluaciones y tipos
│   │   └── log.py                          # Interfaz de auditoría
│   ├── services/                           # Clientes que consumen la API REST
│   │   ├── auth_service.py                 # Llama a /login y /registro
│   │   ├── alumno_service.py               # Llama a endpoints de /alumnos
│   │   ├── curso_service.py                # Llama a endpoints de /cursos
│   │   └── ... (servicios por entidad)
│   ├── templates/                          # Archivos HTML (Jinja2)
│   │   ├── base.html                       # Plantilla maestra y navegación
│   │   ├── auth/                           # Pantallas de login/registro
│   │   ├── dashboard/                      # Pantallas del panel central
│   │   └── ... (carpetas por entidad)
│   └── static/                             # Archivos estáticos
│       └── css/
│           └── styles.css                  # Hoja de estilos global
├── app.py                                  # Punto de entrada de la app Flask Front
├── init.sh                                 # Script de inicialización
├── requirements.txt
├── .env
└── .env.example
```

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/gjoel6055-wq/front_ARMJSSS
cd front_ARMJSSS
```

### 2. Crear el entorno virtual e instalar dependencias

**En Linux / macOS:**
```bash
bash init.sh
source venv/bin/activate
```

**En Windows (sin WSL):**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar las variables de entorno

Copiá el archivo de ejemplo para crear tu propio `.env`:
```bash
cp .env.example .env
```

Editá el archivo `.env`. Acá lo más importante es asegurarte de que apunte a la URL correcta donde está corriendo tu Backend (por defecto, puerto 5000):

```env
API_URL=http://127.0.0.1:8080
SECRET_KEY=tu_clave_secreta_frontend
```

### 4. Correr la aplicación

Asegurate de que el **Backend esté corriendo** en otra terminal. Luego ejecutá:

```bash
python app.py
```
*(Nota: Opcionalmente podés correrlo con `flask run --port=5001` para evitar conflictos de puerto con el backend)*

La interfaz gráfica quedará disponible ingresando desde tu navegador a `http://localhost:8080`.

---

## Arquitectura y Convenciones

**Consumo de la API:**
El Frontend no se conecta directamente a la base de datos. Utiliza una arquitectura de dos capas:
```
Route (Vista) → Service (Cliente HTTP) → API Backend
```

- `routes/` — Captura la interacción del usuario en la web, procesa formularios y renderiza los templates HTML (`render_template`). Emite mensajes Flash en caso de error.
- `services/` — Utilizan la librería `requests` para armar los JSON y enviar las peticiones HTTP (GET, POST, PUT, DELETE) hacia el Backend, inyectando el token JWT cuando es necesario.

**Autenticación y Sesiones:**
- Al hacer login exitoso, el Backend devuelve un token JWT.
- El Frontend guarda este token (y los datos básicos del usuario como rol y email) en la **sesión encriptada de Flask** (`session['token']`).
- En cada nueva vista que requiere permisos, se rescata el token de la sesión y se adjunta a los Headers para consumir la API.

**Estilos y UX:**
- Se utilizó **CSS puro** (`styles.css`) con variables personalizadas y un sistema de tarjetas y modales moderno.
- Se implementaron **Mensajes Flash** centralizados en `base.html` para dar *feedback* visual inmediato al usuario tras cada acción (creación, edición, borrado o errores del servidor).

---

## Equipo y Reparto de Módulos (Front)

| Integrante | Vistas y Servicios |
|---|---|
| Ariana | Tipos evaluación, Evaluaciones, Notas |
| Joel | Auth (UI), Asistencias (Generador y Validador QR), Log de Auditoría |
| Rafael | Listado de Alumnos, Dashboard |
| Shirley | Gestión de Docentes, Cursos, Equipos |
