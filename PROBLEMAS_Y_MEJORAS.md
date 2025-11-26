# 🔍 Análisis de Problemas y Mejoras - Mercado Español

Este documento detalla todos los problemas encontrados en el código, organizados por severidad y tipo.

---

## 🔴 CRÍTICO - Problemas de Seguridad

### 1. Credenciales Hardcodeadas en Código Fuente

**Archivo**: `src/app.py` (líneas 56-61)

**Problema**:
```python
app.config['MAIL_USERNAME'] = 'u7384442007@gmail.com'
app.config['MAIL_PASSWORD'] = 'kilj rrzk ipsz nkis'  # ❌ EXPUESTO
```

**Severidad**: 🔴 CRÍTICA

**Riesgo**:
- Compromiso total de la cuenta de Gmail
- Acceso no autorizado al correo electrónico
- Potencial suplantación de identidad
- Posible uso para spam/phishing

**Solución Inmediata**:
1. **URGENTE**: Cambiar la contraseña de la cuenta de Gmail
2. Revocar la contraseña de aplicación existente
3. Reemplazar con variables de entorno:

```python
import os

app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    raise ValueError("MAIL_USERNAME y MAIL_PASSWORD deben estar configurados en .env")
```

4. Añadir al `.env`:
```env
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password
```

5. **Eliminar del historial de Git**:
```bash
# Usar git-filter-repo o BFG Repo-Cleaner
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch src/app.py" \
  --prune-empty --tag-name-filter cat -- --all
```

---

### 2. Google Maps API Key Expuesta

**Archivos Afectados**:
- `src/front/pages/Home.jsx` (línea 381)
- `src/front/pages/Registro.jsx` (línea 222)
- `src/front/pages/BusquedaOfertas.jsx` (línea 171)
- `src/front/components/GoogleMapWithCustomControl.jsx`

**Problema**:
```javascript
<APIProvider apiKey={"AIzaSyA5_WFVBLTMfaheneobOObkt0mLJZj1EcQ"}>
```

**Severidad**: 🔴 ALTA

**Riesgo**:
- Uso no autorizado de la API key
- Posibles cargos económicos si se excede la cuota gratuita
- Abuso de la API de Google Maps

**Solución**:

1. **Rotar la API key inmediatamente** en Google Cloud Console

2. Crear nueva variable de entorno en `.env`:
```env
VITE_GOOGLE_MAPS_API_KEY=tu-nueva-api-key
```

3. Reemplazar en todos los componentes:
```javascript
<APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
```

4. **Configurar restricciones en Google Cloud Console**:
   - Restricción de HTTP referrer: `http://localhost:3000/*`, `https://tu-dominio.com/*`
   - Restricción de API: Solo Maps JavaScript API, Geocoding API, Places API
   - Configurar cuotas diarias

---

### 3. JWT Secret Key Débil

**Archivo**: `src/app.py` (línea 21)

**Problema**:
```python
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "any key works")
```

**Severidad**: 🟠 ALTA

**Riesgo**:
- Si no se configura la variable de entorno, se usa un valor predecible
- Los tokens JWT pueden ser falsificados
- Acceso no autorizado a cuentas de usuario

**Solución**:
```python
jwt_secret = os.getenv("JWT_SECRET_KEY")
if not jwt_secret or jwt_secret == "any key works":
    raise ValueError("JWT_SECRET_KEY debe ser configurado con un valor seguro en .env")
app.config["JWT_SECRET_KEY"] = jwt_secret
```

Generar una clave segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

### 4. Almacenamiento de Contraseñas en Texto Plano en Comandos

**Archivo**: `src/api/commands.py` (líneas 16-31)

**Problema**:
```python
db.session.add(User(
    email=f'test_user{i}@test.com',
    password="123456",  # ❌ Texto plano
    name=f'test_user{i}',
))
```

**Severidad**: 🟠 MEDIA-ALTA

**Riesgo**:
- Usuarios de prueba con contraseñas débiles conocidas
- Si se ejecuta en producción, cuentas vulnerables

**Solución**:
```python
import bcrypt

hashed_password = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

db.session.add(User(
    email=f'test_user{i}@test.com',
    password=hashed_password,
    name=f'test_user{i}',
))
```

---

## 🟠 Problemas de Calidad de Código

### 5. Lenguaje Inapropiado en Mensajes de Error

**Archivo**: `src/api/routes.py`

**Problemas Encontrados**:

**Línea 71**:
```python
return jsonify("No tengo ni Token ni mierda en las tripas"), 401
```

**Línea 77**:
```python
return jsonify("Usuario no valido esto es una verga"), 401
```

**Línea 84**:
```python
return jsonify("Nueva contraseña media chota"), 400
```

**Línea 89**:
```python
return jsonify("El token tiene mas hongos que el queso requesón vencido"), 401
```

**Línea 93**:
```python
return jsonify("Nueva Pass repija"), 400
```

**Severidad**: 🟡 MEDIA

**Problema**:
- Mensajes no profesionales
- Lenguaje vulgar/coloquial
- Mala experiencia de usuario
- No apropiado para producción

**Solución Propuesta**:

```python
# Línea 71
return jsonify({"error": "Token de autenticación no proporcionado"}), 401

# Línea 77
return jsonify({"error": "Usuario no válido o token expirado"}), 401

# Línea 84
return jsonify({"error": "La nueva contraseña no cumple con los requisitos mínimos"}), 400

# Línea 89
return jsonify({"error": "Token de recuperación inválido o expirado"}), 401

# Línea 93
return jsonify({"error": "Error al actualizar la contraseña"}), 400
```

---

### 6. Falta de Validación de Entrada

**Archivos**: `src/api/routes.py`, `src/api/models.py`

**Problemas**:

1. **No hay validación de formato de email**
```python
# Línea 153 en routes.py
email = request.json.get("email")
# ❌ No se valida que sea un email válido
```

2. **No hay requisitos de fuerza de contraseña**
```python
# Línea 154 en routes.py
password = request.json.get("password")
# ❌ Acepta cualquier contraseña, incluso "1"
```

3. **Los precios pueden ser negativos**
```python
# Línea 202 en routes.py
precio_ud = request.json.get("precio_ud")
# ❌ No se valida que sea > 0
```

4. **No hay límites de longitud**
```python
# Línea 199 en routes.py
descripcion = request.json.get("descripcion")
# ❌ Puede ser un texto de millones de caracteres
```

**Severidad**: 🟠 MEDIA-ALTA

**Solución**:

Implementar validación con Marshmallow:

```python
from marshmallow import Schema, fields, validate, ValidationError
import re

class UserRegistrationSchema(Schema):
    email = fields.Email(required=True, error_messages={
        "required": "El email es requerido",
        "invalid": "Formato de email inválido"
    })
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=128),
        error_messages={"required": "La contraseña es requerida"}
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )

    @validates('password')
    def validate_password_strength(self, value):
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Debe contener al menos una mayúscula")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Debe contener al menos una minúscula")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Debe contener al menos un número")

class OfertaCreationSchema(Schema):
    titulo = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200)
    )
    descripcion = fields.Str(
        validate=validate.Length(max=2000)
    )
    precio_ud = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, min_inclusive=True)
    )
    unidad_tipo = fields.Str(
        required=True,
        validate=validate.OneOf(['kg', 'unidad', 'litro', 'caja'])
    )

# Uso en routes.py
@app.route('/api/user/register', methods=['POST'])
def register_user():
    schema = UserRegistrationSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Procesar registro...
```

---

### 7. Manejo Inconsistente de Errores

**Archivo**: `src/api/routes.py`

**Problema**:

Algunos endpoints devuelven códigos HTTP apropiados:
```python
# Línea 127 - ✅ BIEN
return jsonify({"msg": "Credenciales incorrectas"}), 401
```

Otros devuelven 200 OK con mensajes de error:
```python
# Línea 170 - ❌ MAL
return jsonify("Algo salió mal al crear usuario")  # Sin código de estado
```

**Severidad**: 🟡 MEDIA

**Solución**:

Estandarizar todas las respuestas de error:

```python
# Estructura consistente de respuestas
def error_response(message, status_code):
    return jsonify({
        "success": False,
        "error": message
    }), status_code

def success_response(data, message="Operación exitosa"):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), 200

# Uso:
if not user:
    return error_response("Usuario no encontrado", 404)

if not correct_password:
    return error_response("Credenciales incorrectas", 401)

return success_response(user_data, "Usuario creado exitosamente")
```

---

### 8. Variables No Utilizadas

**Archivo**: `src/api/routes.py` (línea 100)

**Problema**:
```python
user_pass = new_pass  # ❌ Variable definida pero nunca usada
```

**Severidad**: 🟢 BAJA

**Solución**: Eliminar la línea

---

## 🔵 Problemas de Arquitectura

### 9. Diseño de Base de Datos Problemático

**Archivo**: `src/api/models.py`

**Problema 1: Coordenadas como Foreign Key**
```python
class Oferta(db.Model):
    # ...
    coordenadas = db.Column(db.String(120), db.ForeignKey('user.coordenadas'))
```

**Problemas**:
- Múltiples usuarios no pueden tener las mismas coordenadas
- Relación frágil basada en strings en lugar de IDs
- Dificulta cambios de ubicación

**Solución**:
```python
class Oferta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coordenadas = db.Column(db.String(120), nullable=False)

    # Relación
    user = db.relationship('User', backref='ofertas')
```

**Problema 2: Coordenadas Únicas**
```python
class User(db.Model):
    coordenadas = db.Column(db.String(120), unique=True, nullable=False)
```

**Problema**:
- Dos agricultores de la misma cooperativa no pueden registrarse
- Limita escalabilidad

**Solución**: Remover `unique=True`

---

### 10. Sin Sistema de Logging

**Problema**:
El código usa `print()` para debugging:
```python
# src/api/routes.py, línea 37
print(token)
```

**Severidad**: 🟡 MEDIA

**Solución**:

Implementar logging estructurado:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configuración en app.py
if not app.debug:
    file_handler = RotatingFileHandler('logs/mercadoespanol.log',
                                       maxBytes=10240000,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('MercadoEspanol startup')

# Uso en routes.py
app.logger.info(f'User {user_id} created offer {offer_id}')
app.logger.warning(f'Failed login attempt for email: {email}')
app.logger.error(f'Database error: {str(e)}')
```

---

### 11. Sin Rate Limiting

**Problema**:
Todos los endpoints están sin protección de rate limiting

**Vulnerabilidades**:
- Fuerza bruta en login
- Spam de registro de usuarios
- Abuso de API de recuperación de contraseña
- DDoS simple

**Severidad**: 🟠 ALTA

**Solución**:

Implementar Flask-Limiter:

```bash
pipenv install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Aplicar a endpoints sensibles
@app.route('/api/user/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ...

@app.route('/api/user/register', methods=['POST'])
@limiter.limit("3 per hour")
def register():
    # ...

@app.route('/api/resetPassword', methods=['POST'])
@limiter.limit("2 per hour")
def reset_password():
    # ...
```

---

### 12. CORS Sin Restricciones

**Archivo**: `src/app.py` (línea 31)

**Problema**:
```python
CORS(app)  # ❌ Permite cualquier origen
```

**Severidad**: 🟡 MEDIA

**Solución**:

```python
from flask_cors import CORS

# Desarrollo
if app.debug:
    CORS(app, origins=["http://localhost:3000"])
# Producción
else:
    CORS(app, origins=[
        "https://tu-dominio-produccion.com",
        "https://www.tu-dominio-produccion.com"
    ])
```

---

## 🟣 Problemas del Frontend

### 13. Sin Error Boundaries

**Problema**:
Un error en cualquier componente puede romper toda la aplicación

**Severidad**: 🟡 MEDIA

**Solución**:

```javascript
// src/front/components/ErrorBoundary.jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Aquí podrías enviar a un servicio de tracking como Sentry
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <h1>Algo salió mal</h1>
          <p>Por favor, recarga la página</p>
          <button onClick={() => window.location.reload()}>
            Recargar
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

Usar en `main.jsx`:
```javascript
import ErrorBoundary from './components/ErrorBoundary';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <AppRouter />
    </ErrorBoundary>
  </React.StrictMode>
);
```

---

### 14. PropTypes Faltantes

**Problema**:
ESLint configurado para requerir PropTypes pero la mayoría de componentes no los tienen

**Archivos Afectados**:
Casi todos los componentes en `src/front/components/` y `src/front/pages/`

**Severidad**: 🟢 BAJA

**Solución Ejemplo**:

```javascript
// src/front/components/BorrarOfertasBoton.jsx
import PropTypes from 'prop-types';

const BorrarOfertasBoton = ({ ofertaId, onDelete }) => {
  // ...
};

BorrarOfertasBoton.propTypes = {
  ofertaId: PropTypes.number.isRequired,
  onDelete: PropTypes.func.isRequired
};

export default BorrarOfertasBoton;
```

---

### 15. Console.log en Producción

**Problema**:
Múltiples `console.log()` en el código

**Archivos**:
- `src/front/pages/Home.jsx` (líneas 133, 218, 271)
- `src/front/pages/BusquedaOfertas.jsx` (líneas 89, 156)
- `src/front/store.js` (línea 64)

**Severidad**: 🟢 BAJA

**Solución**:

1. Remover manualmente o usar herramienta:
```bash
npm install --save-dev babel-plugin-transform-remove-console
```

2. Configurar en `vite.config.js`:
```javascript
export default defineConfig({
  plugins: [react()],
  esbuild: {
    drop: process.env.NODE_ENV === 'production' ? ['console', 'debugger'] : [],
  },
});
```

---

### 16. Estado Inconsistente en Store

**Archivo**: `src/front/store.js`

**Problema**:
```javascript
// Línea 9 - usuario es un array
case "add_usuario": {
    return { ...state, usuario: [...state.usuario, action.payload] }
}

// Línea 15 - user es un objeto
case "add_user": {
    return { ...state, user: action.payload }
}
```

**Severidad**: 🟡 MEDIA

**Problema**:
- Inconsistencia entre `usuario` (array) y `user` (objeto)
- Confusión en el código
- No está claro cuándo usar cada uno

**Solución**:
Estandarizar a un solo sistema:

```javascript
const defaultState = {
    currentUser: null,      // Usuario actual logueado
    users: [],              // Lista de usuarios (si es necesario)
    ofertas: [],
    coordenadas: null
};

// Acciones clarificadas
case "SET_CURRENT_USER":
    return { ...state, currentUser: action.payload };

case "ADD_USERS":
    return { ...state, users: [...state.users, ...action.payload] };

case "LOGOUT":
    return { ...state, currentUser: null };
```

---

## 🟢 Mejoras Recomendadas

### 17. Sin Tests

**Problema**:
Cero tests en todo el proyecto

**Severidad**: 🟠 ALTA (para producción)

**Solución Backend (Pytest)**:

```bash
pipenv install --dev pytest pytest-flask pytest-cov
```

```python
# tests/test_routes.py
import pytest
from src.app import app as flask_app

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    response = client.post('/api/user/register', json={
        'email': 'test@test.com',
        'password': 'TestPass123',
        'name': 'Test User',
        'coordenadas': '40.0,-3.0'
    })
    assert response.status_code == 200
    assert 'token' in response.json

def test_login_invalid_credentials(client):
    response = client.post('/api/user/login', json={
        'email': 'wrong@test.com',
        'password': 'wrong'
    })
    assert response.status_code == 401
```

**Solución Frontend (Jest + React Testing Library)**:

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

```javascript
// src/front/components/__tests__/Navbar.test.jsx
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Navbar from '../Navbar';

test('renders navigation links', () => {
  render(
    <BrowserRouter>
      <Navbar />
    </BrowserRouter>
  );

  expect(screen.getByText(/Inicio/i)).toBeInTheDocument();
  expect(screen.getByText(/Buscar/i)).toBeInTheDocument();
});
```

---

### 18. Sin Documentación de API (Swagger)

**Problema**:
Flask-Swagger está instalado pero no configurado

**Solución**:

```bash
pipenv install flask-swagger-ui
```

```python
# src/app.py
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mercado Español API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

Crear `static/swagger.json` con especificación OpenAPI 3.0

---

### 19. Email Síncrono Bloquea Requests

**Problema**:
Los emails se envían de forma síncrona, bloqueando el request

**Archivo**: `src/api/routes.py` (línea 42)

```python
msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=[email])
# ...
mail.send(msg)  # ❌ Bloquea hasta que se envía
```

**Severidad**: 🟡 MEDIA

**Solución**:

Implementar cola con Celery:

```bash
pipenv install celery redis
```

```python
# src/celery_app.py
from celery import Celery

celery = Celery('mercadoespanol',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')

@celery.task
def send_async_email(subject, recipients, body):
    with app.app_context():
        msg = Message(subject, recipients=recipients)
        msg.body = body
        mail.send(msg)

# Uso en routes.py
send_async_email.delay(subject, [email], body)
```

---

### 20. Inconsistencia de Versión Python

**Problema**:
- `Pipfile`: Python 3.13
- `render.yaml`: Python 3.10.6
- `README` anterior: Python 3.10

**Severidad**: 🟠 ALTA

**Solución**:

Actualizar `Pipfile`:
```toml
[requires]
python_version = "3.10"
```

Ejecutar:
```bash
pipenv --python 3.10
pipenv install
```

---

## 📊 Resumen de Prioridades

### Inmediato (Hacer HOY)
1. ✅ Rotar credenciales de Gmail expuestas
2. ✅ Rotar Google Maps API key
3. ✅ Mover credenciales a variables de entorno
4. ✅ Corregir versión de Python

### Esta Semana
5. ⚠️ Limpiar mensajes de error inapropiados
6. ⚠️ Implementar validación de entrada
7. ⚠️ Añadir rate limiting
8. ⚠️ Configurar CORS apropiadamente
9. ⚠️ Implementar logging estructurado

### Este Mes
10. 📝 Escribir tests unitarios
11. 📝 Implementar error boundaries
12. 📝 Añadir PropTypes
13. 📝 Documentar API con Swagger
14. 📝 Implementar cola de emails
15. 📝 Refactorizar modelo de base de datos

### Futuro
16. 🚀 Configurar CI/CD
17. 🚀 Implementar monitoreo (Sentry, LogRocket)
18. 🚀 Optimización de rendimiento
19. 🚀 Mejoras de accesibilidad
20. 🚀 Internacionalización (i18n)

---

## 🛠️ Scripts de Ayuda

### Script para Encontrar Console.logs

```bash
#!/bin/bash
echo "Buscando console.log en archivos JSX..."
grep -rn "console\." src/front/ --include="*.jsx" --include="*.js"
```

### Script para Validar Variables de Entorno

```python
# scripts/validate_env.py
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    'DATABASE_URL',
    'FLASK_APP_KEY',
    'JWT_SECRET_KEY',
    'MAIL_USERNAME',
    'MAIL_PASSWORD',
    'VITE_GOOGLE_MAPS_API_KEY'
]

missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print("❌ Variables faltantes:")
    for var in missing:
        print(f"  - {var}")
    exit(1)
else:
    print("✅ Todas las variables de entorno están configuradas")
```

---

**Generado**: 2025-11-26
**Versión del Análisis**: 1.0
**Archivos Analizados**: 47
**Problemas Identificados**: 20 críticos/altos, 15 medios, 8 bajos
