// src/lib/api.ts
import type { AxiosResponse } from 'axios';
import { api, apiOrigin } from './http';
import type { Carta } from '../stores/cartas';

type JSend<T> = { status: 'success' | 'fail' | 'error'; data: T };

// ---------------- Utils ----------------
function unwrap<T>(resp: AxiosResponse<JSend<T>>): T {
  const payload = resp?.data;
  if (!payload) throw new Error('Respuesta vacia');
  if (payload.status !== 'success') {
    throw new Error(`API ${payload.status}`);
  }
  return payload.data as T;
}

const eq = (a?: string, b?: string) =>
  (a ?? '').toLowerCase() === (b ?? '').toLowerCase();

// Intenta varias rutas y devuelve el elemento que cumpla el predicado.
// Si la respuesta es un array -> busca dentro; si es un objeto -> valida el predicado.
async function tryGetMatch<T>(
  paths: string[],
  predicate: (x: any) => boolean
): Promise<T> {
  let lastErr: unknown;
  for (const p of paths) {
    try {
      const r = await api.get<JSend<any>>(p);
      const data = unwrap<any>(r);

      if (Array.isArray(data)) {
        const hit = data.find(predicate);
        if (hit) return hit as T;
      } else if (data && predicate(data)) {
        return data as T;
      }
    } catch (e) {
      lastErr = e;
    }
  }
  throw lastErr ?? new Error('No encontrado');
}

// ---------------- Users ----------------
export async function getUserById(userId: string) {
  const enc = encodeURIComponent(userId.trim());
  const r = await api.get<JSend<any>>(`/users/${enc}`);
  return unwrap<any>(r);
}

// ---------------- Assets ----------------
// Busca por ASSET ID (UUID o 32 chars). Filtra por coincidencia exacta.
export async function getAssetById(assetId: string) {
  const id = assetId.trim();
  const enc = encodeURIComponent(id);

  return await tryGetMatch<any>(
    [
      `/assets/${enc}`,
      `/assets/by-id/${enc}`,
      `/assets/id/${enc}`,
      `/assets?asset_id=${enc}`,
      `/assets`,
    ],
    (o: any) => (o && (o.asset_id || o.id)) ? (
      (o.asset_id?.toLowerCase?.() === id.toLowerCase()) ||
      (o.id?.toLowerCase?.() === id.toLowerCase())
    ) : false
  );
}

// Busca por SERIAL NUMBER. Filtra por coincidencia exacta.
export async function getAssetBySerial(serial: string) {
  const sn = serial.trim();
  const enc = encodeURIComponent(sn);

  const r = await api.get<JSend<any[]>>(`/assets?asset_serial_number=${enc}`);
  const data = unwrap<any[]>(r);
  return data.find(o =>
    (o?.asset_serial_number ?? '').toLowerCase() === sn.toLowerCase()
  ) ?? null;
}

// ---------------- Auth ----------------
type TokenResponse = {
  access_token: string;
  token_type: string;
  [key: string]: unknown;
};

async function postForm(url: string, params: URLSearchParams) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString()
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

async function postJson(url: string, body: unknown) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body ?? {})
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function loginWithPassword(username: string, password: string): Promise<TokenResponse> {
  const params = new URLSearchParams();
  params.set('username', username);
  params.set('password', password);
  params.set('grant_type', 'password');
  params.set('scope', '');
  return await postForm(`${apiOrigin}/auth/token`, params) as TokenResponse;
}

export async function loginWithGoogle(idToken: string): Promise<TokenResponse> {
  return await postJson(`${apiOrigin}/auth/google`, { id_token: idToken }) as TokenResponse;
}

// ---------------- Cartas ----------------
const defaultCartasBase = '/cartas';
const rawCartasBase = (import.meta as any).env?.VITE_API_CARTAS_BASE ?? defaultCartasBase;
const CARTAS_BASE = normaliseBasePath(rawCartasBase);

function normaliseBasePath(path: string): string {
  const trimmed = (path || '').trim();
  if (!trimmed) return defaultCartasBase;
  return trimmed.startsWith('/') ? trimmed : `/${trimmed}`;
}

function joinCartaPath(segment = ''): string {
  if (!segment) return CARTAS_BASE;
  const clean = segment.startsWith('/') ? segment.slice(1) : segment;
  return `${CARTAS_BASE}/${clean}`;
}

type CartaResponse = {
  folio?: string;
  status?: string;
  message?: string;
  carta?: Partial<Carta>;
  [key: string]: unknown;
};

function buildCartaPayload(state: Carta) {
  return {
    folio: state.folio,
    usuario: state.usuario,
    nombreUsuario: state.nombreUsuario,
    correoUsuario: state.correoUsuario,
    ubicacionUsuario: state.ubicacionUsuario,
    supervisorId: state.supervisorId,
    correoSupervisor: state.correoSupervisor,
    tipoAsignacion: state.tipoAsignacion,
    asignados: state.asignados,
    retirados: state.retirados,
    aprobadorDetectado: state.aprobadorDetectado,
    aceptoTerminos: state.aceptoTerminos ?? false
  };
}

export async function crearCarta(state: Carta): Promise<CartaResponse> {
  const payload = buildCartaPayload(state);
  const resp = await api.post<JSend<CartaResponse>>(joinCartaPath(), payload);
  return unwrap<CartaResponse>(resp);
}

export async function firmarCarta(folio: string, extras: Record<string, unknown> = {}): Promise<CartaResponse> {
  const enc = encodeURIComponent(folio);
  const resp = await api.post<JSend<CartaResponse>>(joinCartaPath(`${enc}/firmar`), extras);
  return unwrap<CartaResponse>(resp);
}

export async function obtenerCarta(folio: string): Promise<CartaResponse> {
  const enc = encodeURIComponent(folio);
  const resp = await api.get<JSend<CartaResponse>>(joinCartaPath(enc));
  return unwrap<CartaResponse>(resp);
}