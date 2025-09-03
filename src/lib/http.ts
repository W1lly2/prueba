// src/lib/http.ts
// Cliente HTTP (Axios) + helper opcional con fetch

import axios from 'axios';
import type { AxiosInstance } from 'axios';

const BASE =
  (import.meta as any).env?.VITE_API_BASE ||
  'http://127.0.0.1:8000/api/v1'; // <-- ajusta aquí o via .env

/** Axios preconfigurado */
export const api: AxiosInstance = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' }
});

/** Inyecta / limpia el header Authorization */
export function setAuth(token?: string | null) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
}

/* ------------------ OPCIONAL: wrapper fetch ------------------ */
type HttpOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
};

async function request<T>(path: string, opts: HttpOptions = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: opts.method ?? 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(opts.headers ?? {})
    },
    body: opts.body ? JSON.stringify(opts.body) : undefined
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return (await res.json()) as T;
}

export const http = {
  get:  <T>(p: string) => request<T>(p),
  post: <T>(p: string, body?: any) => request<T>(p, { method: 'POST', body }),
  put:  <T>(p: string, body?: any) => request<T>(p, { method: 'PUT', body }),
  del:  <T>(p: string) => request<T>(p, { method: 'DELETE' })
};