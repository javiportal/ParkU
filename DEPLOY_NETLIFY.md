# Desplegar ParkU en Netlify

Guía paso a paso para desplegar el frontend de ParkU en Netlify.

## Requisitos previos

- Cuenta en [Netlify](https://netlify.com)
- Repositorio en GitHub con el código de ParkU
- Backend desplegado en Render (https://parku-9bfn.onrender.com)

---

## Paso 1: Conectar el repositorio

1. Entra a [app.netlify.com](https://app.netlify.com)
2. Clic en **"Add new site"** → **"Import an existing project"**
3. Conecta **GitHub** y autoriza Netlify
4. Selecciona el repositorio **ParkU**
5. Netlify detectará el `netlify.toml` automáticamente

---

## Paso 2: Configurar la variable de entorno (IMPORTANTE)

Antes de desplegar, agrega la variable que apunta al backend:

1. En la pantalla de configuración del sitio, expande **"Environment variables"**
2. Clic en **"Add a variable"** o **"Add environment variables"**
3. Agrega:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://parku-9bfn.onrender.com/api`
4. Marca **"Deploy"** para que se use en el próximo build

---

## Paso 3: Desplegar

1. Clic en **"Deploy site"**
2. Espera 1–2 minutos a que termine el build
3. Cuando termine, tendrás una URL como `https://algo-random.netlify.app`

---

## Paso 4: Verificar

1. Abre la URL de tu sitio
2. Inicia sesión con las credenciales del seed (revisa `app/seed.py`)
3. Si todo funciona, el frontend está conectado al backend en Render

---

## Cambiar el nombre del sitio (opcional)

1. En Netlify: **Site settings** → **Domain management** → **Options**
2. Clic en **"Change site name"**
3. Elige algo como `parku-esen` → tu URL será `https://parku-esen.netlify.app`

---

## Redeploys automáticos

Cada vez que hagas `git push` a la rama principal, Netlify desplegará automáticamente los cambios del frontend.
