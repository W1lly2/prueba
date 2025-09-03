// src/lib/api.ts
import type { AxiosResponse } from 'axios';
import { api } from './http';

type JSend<T> = { status: 'success' | 'fail' | 'error'; data: T };

// ---------------- Utils ----------------
function unwrap<T>(resp: AxiosResponse<JSend<T>>): T {
  const payload = resp?.data;
  if (!payload) throw new Error('Sin respuesta');
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
  // Swagger: /api/v1/users/{USER_ID}
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
      // ⬇️ Fallback robusto: traer todo y filtrar por asset_id
      `/assets`,
    ],
    (o: any) => (o && (o.asset_id || o.id)) ? (
      (o.asset_id?.toLowerCase?.() === id.toLowerCase()) ||
      (o.id?.toLowerCase?.() === id.toLowerCase())
    ) : false
  );
}

// Busca por SERIAL NUMBER. Filtra por coincidencia exacta.
// src/lib/api.ts
export async function getAssetBySerial(serial: string) {
  const sn = serial.trim();
  const enc = encodeURIComponent(sn);

  const r = await api.get<JSend<any[]>>(`/assets?asset_serial_number=${enc}`);
  const data = unwrap<any[]>(r);
  return data.find(o =>
    (o?.asset_serial_number ?? '').toLowerCase() === sn.toLowerCase()
  ) ?? null;
}