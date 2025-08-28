import { writable } from 'svelte/store';

export type Dispositivo = {
  descripcion: string;
  assetTag?: string;
  numeroSerie?: string;
  accesorio?: string;
};

export type DatosUsuario = {
  id: string;
  nombre: string;
  correo: string;
  ubicacion: string;
  supervisor: string;
  correoSupervisor: string;
};

export type Carta = {
  usuario: DatosUsuario;
  tecnico: string;
  tipoAsignacion: string;
  asignados: Dispositivo[];
  retirados: Dispositivo[];
  folio: string;
  aprobadorDetectado: string;
  aceptoTerminos: boolean;
};

export const carta = writable<Carta>({
  usuario: {
    id: '',
    nombre: '',
    correo: '',
    ubicacion: '',
    supervisor: '',
    correoSupervisor: ''
  },
  tecnico: '',
  tipoAsignacion: '',
  asignados: [],
  retirados: [],
  folio: '',
  aprobadorDetectado: '',
  aceptoTerminos: false
});