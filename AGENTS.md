# AGENTS.md - Development Guide

## Build/Test Commands
- `npm install` - Install dependencies
- `npm run dev` - Start development server (Vite)
- `npm run build` - Build production bundle
- `npm run preview` - Preview production build
- `svelte-check` - TypeScript/Svelte type checking

## Architecture
- **Frontend**: Svelte + TypeScript + Vite + SvelteKit SPA Router
- **Backend**: External FastAPI service at https://github.com/grupotimx/whr_cartas_asig_api/tree/dev
- **Styling**: Bootstrap 5 + Tailwind CSS (preflight disabled)
- **API**: RESTful with JSend response format, configured via VITE_API_BASE
- **Auth**: Google OAuth with JWT tokens

## Project Structure
- `src/pages/` - Svelte page components (Login, Control, Revision, etc.)
- `src/lib/` - Shared utilities (api.ts, http.ts)
- Routes: `/`, `/control`, `/revision`, `/carta`, `/ya-aprobado`, `/carta-firmada`

## Code Style
- TypeScript strict mode, Svelte components with `<script lang="ts">`
- Import order: Bootstrap CSS, Bootstrap JS, local CSS, then components
- API responses use JSend format with unwrap utility function
- Spanish naming for business logic, English for technical terms

## Environment Configuration
- Copy `.env.example` to `.env` and configure VITE_API_BASE with backend URL
- Backend repository: https://github.com/grupotimx/whr_cartas_asig_api/tree/dev
