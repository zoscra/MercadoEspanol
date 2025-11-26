# 🌾 Mercado Español

**Mercado Español** es una plataforma web de marketplace agrícola que conecta directamente a productores del campo con compradores, eliminando intermediarios. Los usuarios pueden publicar y comprar productos agrícolas (cosechas, cultivos) con integración de geolocalización para mostrar ubicaciones de fincas y calcular distancias.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![Flask](https://img.shields.io/badge/flask-latest-lightgrey.svg)

---

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Despliegue](#-despliegue)
- [Problemas Conocidos](#-problemas-conocidos)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

- 🔐 **Autenticación JWT**: Registro e inicio de sesión seguro con tokens JWT
- 🗺️ **Integración con Google Maps**: Geolocalización de fincas y productos
- 📍 **Cálculo de Distancias**: Distancia automática entre compradores y vendedores
- 🌾 **Gestión de Ofertas**: Crear, editar, eliminar y comprar ofertas de productos agrícolas
- 📧 **Recuperación de Contraseña**: Sistema de reseteo de contraseña por email
- 🔍 **Búsqueda Avanzada**: Filtros por precio, tipo de producto, disponibilidad y proximidad
- 📱 **Responsive Design**: Interfaz adaptable a dispositivos móviles
- 👨‍🌾 **Perfiles de Usuario**: Información de vehículos y coordenadas de fincas
- 🖼️ **Subida de Imágenes**: Integración con Cloudinary para fotos de productos

---

## 🛠️ Tecnologías

### Backend
- **Python 3.10+** - Lenguaje de programación
- **Flask** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **PostgreSQL** - Base de datos relacional
- **Flask-JWT-Extended** - Autenticación JWT
- **Flask-Mail** - Envío de emails
- **Bcrypt** - Hash de contraseñas
- **Cloudinary** - Almacenamiento de imágenes
- **Gunicorn** - Servidor WSGI de producción

### Frontend
- **React 18.2** - Biblioteca UI
- **Vite 4.4** - Build tool y dev server
- **React Router 6** - Enrutamiento
- **@vis.gl/react-google-maps** - Componentes de Google Maps
- **ESLint** - Linting de código

### DevOps
- **Pipenv** - Gestión de dependencias Python
- **npm** - Gestión de paquetes JavaScript
- **Render.com** - Plataforma de despliegue
- **GitHub** - Control de versiones

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10+** ([Descargar](https://www.python.org/downloads/))
- **Node.js 20+** ([Descargar](https://nodejs.org/))
- **PostgreSQL 12+** ([Descargar](https://www.postgresql.org/download/))
- **Pipenv** (`pip install pipenv`)
- **Git** ([Descargar](https://git-scm.com/))

### APIs Necesarias
- **Google Maps API Key** ([Obtener aquí](https://developers.google.com/maps/documentation/javascript/get-api-key))
- **Cloudinary Account** ([Registrarse](https://cloudinary.com/users/register/free))

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/MercadoEspanol.git
cd MercadoEspanol
```

### 2. Configurar el Backend

```bash
# Instalar dependencias de Python
pipenv install

# Crear archivo de variables de entorno
cp .env.example .env
```

### 3. Configurar Base de Datos

**Crear base de datos PostgreSQL:**

```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE mercadoespanol;

# Salir
\q
```

**Actualizar .env con la URL de tu base de datos:**

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/mercadoespanol
```

### 4. Ejecutar Migraciones

```bash
# Crear migraciones (si modificaste models.py)
pipenv run migrate

# Aplicar migraciones
pipenv run upgrade
```

### 5. Configurar el Frontend

```bash
# Instalar dependencias de Node
npm install
```

### 6. Iniciar la Aplicación

**Terminal 1 - Backend:**
```bash
pipenv run start
```
El backend estará disponible en `http://localhost:3001`

**Terminal 2 - Frontend:**
```bash
npm run start
```
El frontend estará disponible en `http://localhost:3000`

---

## ⚙️ Configuración

### Variables de Entorno (.env)

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/mercadoespanol

# Flask
FLASK_APP=src/app.py
FLASK_APP_KEY=tu-clave-secreta-muy-segura-aqui
FLASK_DEBUG=1
DEBUG=TRUE

# JWT
JWT_SECRET_KEY=tu-jwt-secret-key-muy-segura

# Email (Gmail)
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password-de-gmail

# Frontend
VITE_BASENAME=/
VITE_BACKEND_URL=http://localhost:3001

# Google Maps
VITE_GOOGLE_MAPS_API_KEY=tu-google-maps-api-key

# Cloudinary (opcional)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### ⚠️ Configuración Importante de Gmail

Para usar Gmail con Flask-Mail, necesitas crear una **App Password**:

1. Ve a tu [cuenta de Google](https://myaccount.google.com/)
2. Seguridad → Verificación en dos pasos (debe estar activada)
3. Busca "Contraseñas de aplicaciones"
4. Genera una nueva contraseña para "Correo"
5. Usa esa contraseña en `MAIL_PASSWORD`

### 🗺️ Configuración de Google Maps API

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs:
   - Maps JavaScript API
   - Geocoding API
   - Places API
4. Crea credenciales → Clave de API
5. **Restricciones recomendadas:**
   - Restricción de HTTP referrer: `http://localhost:3000/*`
   - Restricción de API: Solo las APIs mencionadas

---

## 💻 Uso

### Crear Usuarios de Prueba

```bash
flask insert-test-users 5
```

Esto creará 5 usuarios de prueba con las credenciales:
- Email: `test_user1@test.com` a `test_user5@test.com`
- Contraseña: `123456`

### Flujo de Usuario

1. **Registro**: Los usuarios se registran con email, nombre, información de vehículo y coordenadas de su finca
2. **Login**: Inicio de sesión con JWT que se almacena en localStorage
3. **Crear Oferta**: Los productores publican productos con título, descripción, precio, unidad e imagen
4. **Buscar Ofertas**: Los compradores buscan y filtran ofertas por múltiples criterios
5. **Comprar**: Los compradores pueden reclamar/comprar ofertas disponibles
6. **Gestionar**: Los vendedores pueden eliminar sus propias ofertas

---

## 📁 Estructura del Proyecto

```
MercadoEspanol/
├── src/
│   ├── api/                          # Backend Flask
│   │   ├── __init__.py
│   │   ├── admin.py                  # Panel de administración
│   │   ├── commands.py               # Comandos CLI
│   │   ├── models.py                 # Modelos SQLAlchemy (User, Oferta)
│   │   ├── routes.py                 # Endpoints de la API
│   │   └── utils.py                  # Utilidades y excepciones
│   ├── front/                        # Frontend React
│   │   ├── assets/                   # Imágenes y recursos estáticos
│   │   ├── components/               # Componentes reutilizables
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── GoogleMapWithCustomControl.jsx
│   │   │   ├── BorrarOfertasBoton.jsx
│   │   │   └── ComprarOfertasBoton.jsx
│   │   ├── pages/                    # Páginas de la aplicación
│   │   │   ├── Home.jsx              # Página principal con ofertas
│   │   │   ├── Login.jsx             # Inicio de sesión
│   │   │   ├── Registro.jsx          # Registro con mapa
│   │   │   ├── BusquedaOfertas.jsx   # Búsqueda avanzada
│   │   │   ├── OfertaId.jsx          # Detalle de oferta
│   │   │   └── ResetPassword.jsx     # Recuperación de contraseña
│   │   ├── hooks/
│   │   │   └── useGlobalReducer.jsx  # Hook de estado global
│   │   ├── styles/
│   │   │   └── beautifulStyles.jsx   # Estilos CSS
│   │   ├── main.jsx                  # Punto de entrada React
│   │   ├── routes.jsx                # Configuración de rutas
│   │   └── store.js                  # Reducer de estado global
│   ├── app.py                        # Configuración Flask
│   ├── extension.py                  # Extensiones Flask
│   └── wsgi.py                       # Punto de entrada WSGI
├── migrations/                       # Migraciones Alembic
├── dist/                             # Build de producción (generado)
├── public/                           # Archivos públicos estáticos
├── docs/                             # Documentación adicional
├── .env.example                      # Plantilla de variables de entorno
├── Pipfile                           # Dependencias Python
├── package.json                      # Dependencias JavaScript
├── vite.config.js                    # Configuración Vite
├── render.yaml                       # Configuración de despliegue
└── README.md                         # Este archivo
```

---

## 🔌 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/user/register` | Registrar nuevo usuario | No |
| POST | `/api/user/login` | Iniciar sesión | No |
| GET | `/api/user` | Obtener usuario actual | JWT |
| POST | `/api/resetPassword` | Solicitar reset de contraseña | No |
| PUT | `/api/user/resetPassword` | Actualizar contraseña con token | No |

### Ofertas

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/user/ofertas` | Listar todas las ofertas | No |
| POST | `/api/user/ofertas` | Crear nueva oferta | JWT |
| GET | `/api/user/oferta/info/<id>` | Obtener oferta específica | No |
| PUT | `/api/user/oferta/comprar/<id>` | Comprar/reclamar oferta | JWT |
| DELETE | `/api/user/oferta/vendedor/borrar/<id>` | Eliminar oferta propia | JWT |

### Ejemplo de Request

**Registro de Usuario:**
```bash
curl -X POST http://localhost:3001/api/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "agricultor@example.com",
    "password": "miPassword123",
    "name": "Juan Pérez",
    "vehiculo": "Camioneta Toyota",
    "coordenadas": "40.416775,-3.703790"
  }'
```

**Crear Oferta (requiere JWT):**
```bash
curl -X POST http://localhost:3001/api/user/ofertas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_JWT_TOKEN" \
  -d '{
    "titulo": "Tomates Orgánicos",
    "descripcion": "Tomates frescos de cultivo propio",
    "precio_ud": 2.5,
    "unidad_tipo": "kg",
    "image_url": "https://example.com/tomates.jpg",
    "coordenadas": "40.416775,-3.703790"
  }'
```

---

## 🚢 Despliegue

### Despliegue en Render.com

Este proyecto está configurado para desplegarse fácilmente en Render.com:

1. **Fork el repositorio** a tu cuenta de GitHub

2. **Crea una cuenta en [Render.com](https://render.com)**

3. **Nuevo Web Service:**
   - Conecta tu repositorio de GitHub
   - Render detectará automáticamente `render.yaml`
   - Se crearán:
     - Web Service (Flask + React)
     - PostgreSQL Database

4. **Configurar Variables de Entorno** en Render Dashboard:
   - `FLASK_APP_KEY`
   - `JWT_SECRET_KEY`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `VITE_GOOGLE_MAPS_API_KEY`
   - (Cloudinary si lo usas)

5. **Deploy:**
   - Render ejecutará automáticamente `./render_build.sh`
   - Build del frontend con Vite
   - Instalación de dependencias Python
   - Migraciones de base de datos

6. **Actualizar Google Maps API:**
   - Añade el dominio de Render a las restricciones de HTTP referrer

### Build Manual

```bash
# Build del frontend
npm run build

# El output estará en /dist
# Flask sirve estos archivos estáticos automáticamente
```

---

## ⚠️ Problemas Conocidos

### 🔴 CRÍTICO - Seguridad

1. **Credenciales Hardcodeadas**
   - **Problema**: Email y contraseña de Gmail están hardcodeados en `src/app.py`
   - **Solución**:
     ```python
     # Reemplazar en src/app.py líneas 56-61:
     app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
     app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
     ```
   - **URGENTE**: Rotar la contraseña expuesta inmediatamente

2. **Google Maps API Key Expuesta**
   - **Problema**: API key hardcodeada en componentes React
   - **Solución**: Mover a variable de entorno `VITE_GOOGLE_MAPS_API_KEY`
   - Usar: `import.meta.env.VITE_GOOGLE_MAPS_API_KEY`

### 🟡 Advertencias

1. **Inconsistencia de Versión Python**
   - `Pipfile` requiere Python 3.13
   - `render.yaml` usa Python 3.10.6
   - **Solución**: Actualizar Pipfile a Python 3.10

2. **Mensajes de Error Inapropiados**
   - Algunos mensajes en `routes.py` contienen lenguaje informal/inapropiado
   - **Solución**: Revisar líneas 71, 77, 84, 89, 93 y reemplazar con mensajes profesionales

3. **Validación de Entrada Faltante**
   - No hay validación de formato de email
   - No hay requisitos de fuerza de contraseña
   - Los precios pueden ser negativos
   - **Solución**: Implementar validación con Flask-WTForms o Marshmallow

4. **Sin Tests**
   - No hay tests unitarios ni de integración
   - **Solución**: Implementar pytest para backend y Jest para frontend

### 🟢 Mejoras Recomendadas

- Implementar rate limiting en endpoints de API
- Añadir documentación Swagger/OpenAPI
- Configurar logging estructurado
- Implementar sistema de cola para emails
- Añadir error boundaries en React
- Implementar PropTypes en todos los componentes
- Añadir restricciones CORS específicas por dominio

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica increíble'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Convenciones de Código

- **Python**: Sigue PEP 8
- **JavaScript**: Usa ESLint configurado en el proyecto
- **Commits**: Usa prefijos (Add:, Fix:, Update:, Remove:, Refactor:)
- **Tests**: Escribe tests para nuevas funcionalidades

---

## 📄 Licencia

Este proyecto fue construido como parte del [Coding Bootcamp](https://4geeksacademy.com/us/coding-bootcamp) de 4Geeks Academy.

Basado en el template de [4Geeks Academy](https://github.com/4geeksacademy/).

---

## 👥 Autores

Desarrollado por estudiantes de 4Geeks Academy como proyecto final de bootcamp.

---

## 📞 Soporte

¿Necesitas ayuda?

- 📧 Email: soporte@example.com
- 📚 [Documentación de 4Geeks](https://4geeks.com/docs/start/react-flask-template)
- 🐛 [Reportar un bug](https://github.com/tu-usuario/MercadoEspanol/issues)

---

## 🙏 Agradecimientos

- [4Geeks Academy](https://4geeksacademy.com/) por el template base
- [Alejandro Sanchez](https://twitter.com/alesanchezr) y contribuidores del template
- Comunidad de desarrolladores open source

---

<div align="center">

**[⬆ Volver arriba](#-mercado-español)**

Hecho con ❤️ por estudiantes de 4Geeks Academy

</div>
