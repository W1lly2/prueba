// src/stores/cartas.ts
import { writable } from 'svelte/store';

export type Dispositivo = {
  descripcion: string;
  assetTag: string;
  numeroSerie: string;
  accesorio: string;
};

export type Carta = {
  // Datos del usuario (planos)
  usuario: string;
  nombreUsuario: string;
  correoUsuario: string;
  ubicacionUsuario: string;
  supervisorId: string;
  correoSupervisor: string;

  // Flujo
  tipoAsignacion: string;
  asignados: Dispositivo[];
  retirados: Dispositivo[];
  aprobadorDetectado: string;

  // ✅ nuevos (usados en CartaAceptacion.svelte)
  aceptoTerminos?: boolean;
  folio?: string;
};

const initial: Carta = {
  usuario: '',
  nombreUsuario: '',
  correoUsuario: '',
  ubicacionUsuario: '',
  supervisorId: '',
  correoSupervisor: '',
  tipoAsignacion: '',
  asignados: [],
  retirados: [],
  aprobadorDetectado: '',
  // ✅ inicializa para evitar undefined
  aceptoTerminos: false,
  folio: ''
};

export const carta = writable<Carta>(initial);