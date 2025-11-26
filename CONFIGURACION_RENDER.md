# 🔧 Configuración de Variables de Entorno para Render.com

## ❌ ELIMINAR estas variables (obsoletas o inseguras)

1. **TOKEN_KEY**
   - ❌ Nombre obsoleto, ahora se llama JWT_SECRET_KEY

## ⚠️ ACTUALIZAR estas variables (valores inseguros)

1. **FLASK_APP_KEY**
   - ❌ Valor actual: "any key works"
   - ✅ Nuevo valor: [Genera una clave segura]
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **DATABASE_URL**
   - ❌ Valor actual: postgres://gitpod:postgres@localhost:5432/example
   - ✅ Debe ser la URL de tu base de datos PostgreSQL en Render
   - Formato: `postgresql://usuario:password@host.render.com/nombre_db`
   - **IMPORTANTE**: Render proporciona esta URL automáticamente cuando creas la base de datos

## ➕ AÑADIR estas variables NUEVAS (requeridas)

### Seguridad - JWT
```
JWT_SECRET_KEY=<genera-una-clave-segura>
```
**Cómo generarla:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Email - Gmail
```
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password-de-gmail
```
**Cómo obtener MAIL_PASSWORD:**
1. Ve a https://myaccount.google.com/
2. Seguridad → Verificación en dos pasos (activar si no está)
3. Busca "Contraseñas de aplicaciones"
4. Genera una nueva para "Correo"
5. Usa esa contraseña de 16 caracteres

### Google Maps
```
VITE_GOOGLE_MAPS_API_KEY=tu-nueva-google-maps-api-key
```
**IMPORTANTE**: Debes generar una NUEVA API key porque la anterior está expuesta en el código
- Ve a https://console.cloud.google.com/
- Crea nueva API key
- Configura restricciones:
  - HTTP referrer: `https://tu-dominio.onrender.com/*`
  - APIs: Maps JavaScript API, Geocoding API, Places API

### Frontend
```
VITE_FRONT_URL=https://sample-service-name-1p43.onrender.com/
```
(Usa el mismo valor que VITE_FRONTEND_URL)

### CORS - Producción
```
ALLOWED_ORIGINS=https://sample-service-name-1p43.onrender.com,https://www.tu-dominio.com
```
**Formato**: Lista separada por comas, sin espacios

## ✅ MANTENER estas variables (ya están bien)

- **FLASK_APP** = src/app.py ✅
- **FLASK_DEBUG** = 1 (cambiar a 0 en producción real)
- **DEBUG** = TRUE (cambiar a FALSE en producción real)
- **VITE_BASENAME** = / ✅
- **VITE_BACKEND_URL** = https://sample-service-name-1p43.onrender.com/ ✅
- **VITE_FRONTEND_URL** = https://sample-service-name-1p43.onrender.com/ ✅

---

## 📋 Configuración Final Completa para Render

Copia esta configuración completa (reemplaza los valores):

```env
# Base de Datos (Render lo proporciona automáticamente)
DATABASE_URL=postgresql://usuario:password@host.render.com/nombre_db

# Flask
FLASK_APP=src/app.py
FLASK_DEBUG=0
DEBUG=FALSE

# Seguridad - GENERA NUEVAS CLAVES
FLASK_APP_KEY=<genera con: python -c "import secrets; print(secrets.token_hex(32))">
JWT_SECRET_KEY=<genera con: python -c "import secrets; print(secrets.token_hex(32))">

# Email Gmail
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password-16-caracteres

# Frontend
VITE_BASENAME=/
VITE_BACKEND_URL=https://tu-servicio.onrender.com
VITE_FRONTEND_URL=https://tu-servicio.onrender.com
VITE_FRONT_URL=https://tu-servicio.onrender.com

# Google Maps - GENERA NUEVA API KEY
VITE_GOOGLE_MAPS_API_KEY=tu-nueva-api-key-aqui

# CORS
ALLOWED_ORIGINS=https://tu-servicio.onrender.com
```

---

## 🚀 Pasos a Seguir en Render

### 1. Eliminar variable obsoleta
- Busca **TOKEN_KEY** y elimínala

### 2. Generar claves seguras
Ejecuta en tu terminal local:
```bash
# Para FLASK_APP_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Para JWT_SECRET_KEY (ejecuta de nuevo para obtener otra diferente)
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Actualizar FLASK_APP_KEY
- Reemplaza "any key works" con la clave generada

### 4. Añadir JWT_SECRET_KEY
- Crea nueva variable con la segunda clave generada

### 5. Configurar Email
- Añade MAIL_USERNAME con tu email
- Genera App Password en Google y añádela en MAIL_PASSWORD

### 6. Configurar Google Maps
- Genera NUEVA API key en Google Cloud Console
- Añade VITE_GOOGLE_MAPS_API_KEY

### 7. Añadir VITE_FRONT_URL
- Usa el mismo valor que VITE_FRONTEND_URL

### 8. Añadir ALLOWED_ORIGINS
- Usa tu URL de Render

### 9. Verificar DATABASE_URL
- Si está como localhost, déjala que Render la configure automáticamente
- Render la establecerá cuando conectes tu servicio con la base de datos PostgreSQL

---

## ⚠️ IMPORTANTE: Producción vs Desarrollo

Para producción real, cambia:
```env
FLASK_DEBUG=0
DEBUG=FALSE
```

---

## 🔒 Seguridad Post-Configuración

Después de configurar las variables:

1. **Rotar Google Maps API Key antigua**
   - La antigua key (AIzaSyA5_WFVBLTMfaheneobOObkt0mLJZj1EcQ) está expuesta
   - Elimínala en Google Cloud Console
   - Usa solo la nueva

2. **Verificar restricciones de API**
   - HTTP referrer solo tu dominio
   - APIs solo las necesarias

3. **Rotar contraseña de Gmail**
   - Si la antigua estaba expuesta, genera nueva App Password

---

## ✅ Checklist Final

- [ ] Eliminar TOKEN_KEY
- [ ] Generar y actualizar FLASK_APP_KEY
- [ ] Añadir JWT_SECRET_KEY
- [ ] Configurar MAIL_USERNAME y MAIL_PASSWORD
- [ ] Generar nueva Google Maps API key
- [ ] Añadir VITE_GOOGLE_MAPS_API_KEY
- [ ] Añadir VITE_FRONT_URL
- [ ] Añadir ALLOWED_ORIGINS
- [ ] Verificar DATABASE_URL (debe ser de Render, no localhost)
- [ ] Cambiar FLASK_DEBUG=0 y DEBUG=FALSE para producción
- [ ] Eliminar API key antigua de Google Cloud Console
- [ ] Hacer redeploy del servicio en Render

---

**Después de configurar todo, haz redeploy del servicio en Render para que tome las nuevas variables.**
