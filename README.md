# WHR Cartas Asignación - Frontend

Proyecto de Asignación de Cartas recreado en Svelte + TypeScript.

## Configuración

1. `npm install` - Instalar dependencias
2. Copiar `.env.example` a `.env` y configurar:
   - `VITE_API_BASE` - URL del backend API
   - `VITE_GOOGLE_CLIENT_ID` - Client ID de Google OAuth

## Backend

Este frontend se conecta al backend en: https://github.com/grupotimx/whr_cartas_asig_api/tree/dev

## Desarrollo

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Build de producción
- `npm run preview` - Preview del build
- `svelte-check` - Verificación de tipos