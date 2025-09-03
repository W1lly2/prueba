<script lang="ts">
  import { get } from 'svelte/store';
  import { push } from 'svelte-spa-router';

  import { carta, type Carta, type Dispositivo } from '../stores/cartas';
  import { getUserById, getAssetBySerial } from '../lib/api';

  // Estado reactivo del store
  $: state = $carta as Carta;

  // Auxiliares del form (inputs temporales)
  let tecnicoSeleccionado = '';
  let descripcionTmp = '';
  let serieTmp = '';
  let serieRetirarTmp = '';

  function setCarta(next: Carta) {
    carta.set(next);
  }

  /** Resetea el store y vuelve al login */
  function cerrarSesion() {
    const limpio: Carta = {
      usuario: '',
      nombreUsuario: '',
      correoUsuario: '',
      ubicacionUsuario: '',
      supervisorId: '',
      correoSupervisor: '',
      tipoAsignacion: '',
      asignados: [],
      retirados: [],
      aprobadorDetectado: ''
    };
    carta.set(limpio);
    push('/'); // ir a login
  }

  // Helpers
  function valueOf(e: Event): string {
    const el = e.target as HTMLInputElement;
    return el?.value ?? '';
  }

  function cleanLabel(s?: string): string {
    if (!s) return '';
    // Quita "Nombre " o "Ubicación " al inicio (con o sin acento)
    return s.replace(/^(nombre|ubicaci[oó]n)\s+/i, '').trim();
  }

  function updateAsignado(i: number, campo: keyof Dispositivo, val: string) {
    const cur = get(carta);
    const arr = cur.asignados.map((x, idx) => (idx === i ? { ...x, [campo]: val } : x));
    setCarta({ ...cur, asignados: arr });
  }

  function updateRetirado(i: number, campo: keyof Dispositivo, val: string) {
    const cur = get(carta);
    const arr = cur.retirados.map((x, idx) => (idx === i ? { ...x, [campo]: val } : x));
    setCarta({ ...cur, retirados: arr });
  }

  // ------- Carga datos de usuario por ID (blur o Enter) -------
  async function buscarUsuario() {
  const userId = (state.usuario || '').trim();
  if (!userId) return;

  try {
    const u: any = await getUserById(userId);
    setCarta({
      ...state,
      usuario: userId,
      nombreUsuario: cleanLabel(u?.user_name),
      correoUsuario: u?.user_email ?? '',
      ubicacionUsuario: cleanLabel(u?.user_location),   // <-- aquí estaba el typo
      supervisorId: u?.supervisor_user_id ?? '',
      correoSupervisor: u?.supervisor_email ?? ''
    });
  } catch (err) {
    console.error('Error cargando usuario:', err);
    setCarta({
      ...state,
      nombreUsuario: '',
      correoUsuario: '',
      ubicacionUsuario: '',
      supervisorId: '',
      correoSupervisor: ''
    });
  }
}

  // Autocompletar asset tag / descripción si teclean serial en la tabla (ASIGNADOS)
  async function onSerialAsignadoBlur(i: number) {
    const sn = state.asignados[i]?.numeroSerie?.trim();
    if (!sn) return;
    try {
      const a = await getAssetBySerial(sn);
      if (a?.asset_tag) updateAsignado(i, 'assetTag', a.asset_tag);
      if (a?.asset_description && !state.asignados[i]?.descripcion) {
        updateAsignado(i, 'descripcion', a.asset_description);
      }
    } catch {
      /* noop */
    }
  }

  // Autocompletar si teclean serial en la tabla (RETIRADOS)
  async function onSerialRetiradoBlur(i: number) {
    const sn = state.retirados[i]?.numeroSerie?.trim();
    if (!sn) return;
    try {
      const a = await getAssetBySerial(sn);
      if (a?.asset_tag) updateRetirado(i, 'assetTag', a.asset_tag);
      if (a?.asset_description && !state.retirados[i]?.descripcion) {
        updateRetirado(i, 'descripcion', a.asset_description);
      }
    } catch {
      /* noop */
    }
  }

  // -------- Asignar Dispositivo SOLO por Número de Serie ----------
  async function asignarDispositivo() {
    const serial = (serieTmp || '').trim();
    if (!descripcionTmp && !serial) return;

    let nuevo: Dispositivo = {
      descripcion: descripcionTmp ?? '',
      assetTag: '',
      numeroSerie: serial ?? '',
      accesorio: ''
    };

    try {
      if (serial) {
        const a = await getAssetBySerial(serial);
        if (a) {
          nuevo.descripcion = a.asset_description ?? nuevo.descripcion;
          nuevo.assetTag = a.asset_tag ?? '';
          nuevo.numeroSerie = a.asset_serial_number ?? serial;
        }
      }
    } catch (err) {
      console.warn('No se pudo autocompletar activo por número de serie:', err);
    }

    setCarta({ ...state, asignados: [...state.asignados, nuevo] });
    descripcionTmp = '';
    serieTmp = '';
  }

  // -------- Retirar Dispositivo (misma lógica de autocompletar) ----------
  async function retirarDispositivo() {
    const serial = (serieRetirarTmp || '').trim();
    if (!serial) return;

    let nuevo: Dispositivo = {
      descripcion: '',
      assetTag: '',
      numeroSerie: serial,
      accesorio: ''
    };

    try {
      const a = await getAssetBySerial(serial);
      if (a) {
        nuevo.descripcion = a.asset_description ?? nuevo.descripcion;
        nuevo.assetTag = a.asset_tag ?? '';
        nuevo.numeroSerie = a.asset_serial_number ?? serial;
      }
    } catch (err) {
      console.warn('No se pudo autocompletar activo (retirar) por número de serie:', err);
    }

    setCarta({ ...state, retirados: [...state.retirados, nuevo] });
    serieRetirarTmp = '';
  }

  function eliminarAsignado(i: number) {
    setCarta({ ...state, asignados: state.asignados.filter((_, idx) => idx !== i) });
  }
  function eliminarRetirado(i: number) {
    setCarta({ ...state, retirados: state.retirados.filter((_, idx) => idx !== i) });
  }

  function generarCarta() {
    push('/revision');
  }
</script>

<div class="min-vh-100 py-4" style="background:#f3f4f6;">
  <div class="container">

    <!-- Header con logos y sesión -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <img src="/gtim.jpg" alt="GTIM" class="logo-left" />
      <div class="d-flex align-items-center gap-2">
        <span class="badge text-bg-light rounded-pill px-3 py-2">
          Hola, <strong>{state.aprobadorDetectado || 'ADMIN'}</strong>
        </span>
        <button class="btn btn-outline-danger btn-sm" on:click={cerrarSesion}>Cerrar sesión</button>
      </div>
      <img src="/whirlpool-corp.jpg" alt="Whirlpool Corporation" class="logo-right" />
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <h2 class="h4 text-center mb-4">Control de Asignación de Equipos</h2>

        <!-- Datos usuario -->
        <div class="row g-3">
          <div class="col-md-2">
            <label class="form-label fw-bold">User ID</label>
            <input
              class="form-control"
              placeholder="USUARIO1"
              bind:value={state.usuario}
              on:blur={buscarUsuario}
              on:keydown={(e) => (e.key === 'Enter') && buscarUsuario()} />
          </div>

          <div class="col-md-3">
            <label class="form-label">Nombre de Usuario</label>
            <input class="form-control" bind:value={state.nombreUsuario} disabled />
          </div>

          <div class="col-md-3">
            <label class="form-label">Correo</label>
            <input class="form-control" bind:value={state.correoUsuario} disabled />
          </div>

          <div class="col-md-2">
            <label class="form-label">Ubicación</label>
            <input class="form-control" bind:value={state.ubicacionUsuario} disabled />
          </div>

          <div class="col-md-2">
            <label class="form-label">Supervisor ID</label>
            <input class="form-control" bind:value={state.supervisorId} disabled />
          </div>

          <div class="col-md-4">
            <label class="form-label">Correo de Supervisor</label>
            <input class="form-control" bind:value={state.correoSupervisor} disabled />
          </div>
        </div>

        <hr class="my-4" />

        <!-- Técnico -->
        <div class="mb-3">
          <label class="form-label fw-bold">Técnico</label>
          <div class="input-group">
            <select class="form-select" bind:value={tecnicoSeleccionado}>
              <option value="" selected>Selecciona técnico…</option>
              <option value="SANCHG27">SANCHG27 - Gaston Sanchez (Monterrey IT)</option>
            </select>
          </div>
        </div>

        <!-- Asignar dispositivo -->
        <div class="mb-3">
          <label class="form-label fw-bold">Dispositivo</label>
          <div class="row g-2">
            <div class="col-md">
              <input
                class="form-control"
                placeholder="Descripción (opcional)"
                bind:value={descripcionTmp} />
            </div>
            <div class="col-md-3">
              <input
                class="form-control"
                placeholder="Número de serie"
                bind:value={serieTmp} />
            </div>
            <div class="col-auto">
              <button class="btn btn-primary" on:click={asignarDispositivo}>
                Asignar Dispositivo
              </button>
            </div>
          </div>
        </div>

        <!-- Tipo de asignación -->
        <div class="mb-4">
          <label class="form-label fw-bold">Tipo de Asignación</label>
          <select class="form-select" bind:value={state.tipoAsignacion}>
            <option value="" selected>Selecciona…</option>
            <option value="PC Refresh">PC Refresh</option>
            <option value="Alta">Alta</option>
            <option value="Cambio">Cambio</option>
          </select>
        </div>

        <!-- Asignados -->
        <h6 class="fw-bold mb-2">Lista de Dispositivos Asignados</h6>
        <div class="table-responsive">
          <table class="table table-sm align-middle">
            <thead>
              <tr class="table-secondary">
                <th style="width:40%">Descripción Dispositivo</th>
                <th style="width:15%">Asset Tag</th>
                <th style="width:20%">Número de Serie</th>
                <th style="width:15%">Accesorio</th>
                <th style="width:10%"></th>
              </tr>
            </thead>
            <tbody>
              {#if state.asignados.length === 0}
                <tr><td colspan="5" class="text-muted">Sin dispositivos asignados.</td></tr>
              {:else}
                {#each state.asignados as d, i}
                  <tr>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.descripcion}
                        on:input={(e) => updateAsignado(i, 'descripcion', valueOf(e))} />
                    </td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.assetTag}
                        on:input={(e) => updateAsignado(i, 'assetTag', valueOf(e))} />
                    </td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.numeroSerie}
                        on:blur={() => onSerialAsignadoBlur(i)}
                        on:input={(e) => updateAsignado(i, 'numeroSerie', valueOf(e))} />
                    </td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.accesorio}
                        on:input={(e) => updateAsignado(i, 'accesorio', valueOf(e))} />
                    </td>
                    <td class="text-end">
                      <button
                        class="btn btn-outline-secondary btn-sm icon-btn"
                        title="Quitar"
                        aria-label="Quitar"
                        on:click={() => eliminarAsignado(i)}>
                        <img src="/trash.jpg" alt="" class="icon-trash" draggable="false" aria-hidden="true" />
                      </button>
                    </td>
                  </tr>
                {/each}
              {/if}
            </tbody>
          </table>
        </div>

        <!-- Retirar -->
        <div class="mt-4">
          <label class="form-label fw-bold">Retirar Dispositivo</label>
          <div class="row g-2">
            <div class="col">
              <input
                class="form-control"
                placeholder="Ej: SN987654321"
                bind:value={serieRetirarTmp} />
            </div>
            <div class="col-auto">
              <button class="btn btn-warning" on:click={retirarDispositivo}>
                Retirar Dispositivo
              </button>
            </div>
          </div>
        </div>

        <!-- Retirados -->
        <h6 class="fw-bold mt-4 mb-2">Lista de Dispositivos Retirados</h6>
        <div class="table-responsive">
          <table class="table table-sm align-middle">
            <thead>
              <tr class="table-secondary">
                <th style="width:40%">Descripción Dispositivo</th>
                <th style="width:15%">Asset Tag</th>
                <th style="width:20%">Número de Serie</th>
                <th style="width:15%">Accesorio</th>
                <th style="width:10%"></th>
              </tr>
            </thead>
            <tbody>
              {#if state.retirados.length === 0}
                <tr><td colspan="5" class="text-muted">Sin dispositivos retirados.</td></tr>
              {:else}
                {#each state.retirados as d, i}
                  <tr>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.descripcion}
                        on:input={(e) => updateRetirado(i, 'descripcion', valueOf(e))} />
                    </td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.assetTag}
                        on:input={(e) => updateRetirado(i, 'assetTag', valueOf(e))} />
                    </td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.numeroSerie}
                        on:blur={() => onSerialRetiradoBlur(i)}
                        on:input={(e) => updateRetirado(i, 'numeroSerie', valueOf(e))} />
                    </td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        bind:value={d.accesorio}
                        on:input={(e) => updateRetirado(i, 'accesorio', valueOf(e))} />
                    </td>
                    <td class="text-end">
                      <button
                        class="btn btn-outline-secondary btn-sm icon-btn"
                        title="Quitar"
                        aria-label="Quitar"
                        on:click={() => eliminarRetirado(i)}>
                        <img src="/trash.jpg" alt="" class="icon-trash" draggable="false" aria-hidden="true" />
                      </button>
                    </td>
                  </tr>
                {/each}
              {/if}
            </tbody>
          </table>
        </div>

        <div class="d-flex justify-content-end mt-4">
          <button class="btn btn-success" on:click={generarCarta}>
            Generar carta de asignación
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  input:disabled { cursor: not-allowed; }
  .logo-left  { height: 44px; width: auto; object-fit: contain; }
  .logo-right { height: 40px; width: auto; object-fit: contain; }

  .icon-btn { padding: .25rem .5rem; line-height: 1; display: inline-flex; align-items: center; justify-content: center; }
  .icon-trash { width: 16px; height: 16px; object-fit: contain; pointer-events: none; }
</style>