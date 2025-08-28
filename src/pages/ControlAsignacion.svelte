<script lang="ts">
  import { get } from 'svelte/store';
  import { push } from 'svelte-spa-router';
  import { carta, type Carta, type Dispositivo } from '../stores/cartas';

  let state: Carta = get(carta);
  const setCarta = (s: Carta) => { state = s; carta.set(state); };

  let descripcionAsignar = '';
  let numeroSerieAsignar = '';
  let numeroSerieRetirar = '';

  function onTecnicoChange(e: Event) {
    setCarta({ ...state, tecnico: (e.target as HTMLSelectElement).value });
  }
  function onTipoAsignacionChange(e: Event) {
    setCarta({ ...state, tipoAsignacion: (e.target as HTMLSelectElement).value });
  }

  function updateAsignado(index: number, field: 'assetTag' | 'accesorio') {
    return (e: Event) => {
      const value = (e.target as HTMLInputElement).value;
      const nuevos = state.asignados.map((d, i) => (i === index ? { ...d, [field]: value } : d));
      setCarta({ ...state, asignados: nuevos });
    };
  }

  function updateRetirado(index: number, field: 'assetTag' | 'accesorio') {
  return (e: Event) => {
    const value = (e.target as HTMLInputElement).value;
    const nuevos = state.retirados.map((d, i) =>
      i === index ? { ...d, [field]: value } : d
    );
    setCarta({ ...state, retirados: nuevos });
  };
}

  function asignar() {
    if (!numeroSerieAsignar) return;
    const d: Dispositivo = {
      descripcion: descripcionAsignar || '',
      numeroSerie: numeroSerieAsignar || '',
      assetTag: '',
      accesorio: ''
    };
    setCarta({ ...state, asignados: [...state.asignados, d] });
    descripcionAsignar = '';
    numeroSerieAsignar = '';
  }

  function retirar() {
    if (!numeroSerieRetirar) return;
    const d: Dispositivo = {
      descripcion: '',
      numeroSerie: numeroSerieRetirar,
      assetTag: '',
      accesorio: ''
    };
    setCarta({ ...state, retirados: [...state.retirados, d] });
    numeroSerieRetirar = '';
  }

  const generarCarta = () => push('/revision');
  const logout = () => push('/');
</script>

<div class="min-h-screen bg-light">
  <!-- Topbar -->
  <header class="bg-white border-bottom sticky-top">
  <div class="container-fluid py-1 px-3 overflow-hidden">
    <div class="row align-items-center gx-2">
      <!-- Izquierda -->
      <div class="col-3 d-flex align-items-center ps-0">
        <img src="/gtim.jpg" alt="gtim" class="logo-left" />
      </div>

      <!-- Centro -->
      <div class="col-6 d-flex justify-content-center">
        <div class="d-flex gap-2 align-items-center">
          <span class="badge text-bg-light border">
            Hola{state.aprobadorDetectado ? `, ${state.aprobadorDetectado}` : ''}
          </span>
          <button class="btn btn-sm btn-outline-danger" on:click={logout}>Cerrar sesión</button>
        </div>
      </div>

      <!-- Derecha -->
      <div class="col-3 d-flex justify-content-end align-items-center pe-2">
        <img src="/whirlpool-corp.jpg" alt="Whirlpool Corporation" class="logo-right" />
      </div>
    </div>
  </div>
</header>


  <!-- Card -->
  <div class="container-ideal py-2">
    <div class="card shadow-sm">
      <div class="card-body compact">
        <h2 class="h4 text-center mb-3">Control de Asignación de Equipos</h2>

        <!-- Cabecera (bloqueados y grises: Nombre, Correo, Ubicación, Supervisor ID, Correo de Supervisor) -->
        <div class="row g-2">
          <div class="col-12 col-md-6 col-lg-2">
            <label for="uid" class="form-label mb-1 fw-bold">User ID</label>
            <input id="uid" class="form-control form-control-sm" bind:value={state.usuario.id} />
          </div>

          <div class="col-12 col-md-6 col-lg-2">
            <label for="uname" class="form-label mb-1">Nombre de Usuario</label>
            <input id="uname" class="form-control form-control-sm bg-light" bind:value={state.usuario.nombre} disabled />
          </div>

          <div class="col-12 col-md-6 col-lg-2">
            <label for="uemail" class="form-label mb-1">Correo</label>
            <input id="uemail" type="email" class="form-control form-control-sm bg-light"
                   bind:value={state.usuario.correo} disabled />
          </div>

          <div class="col-12 col-md-6 col-lg-2">
            <label for="uloc" class="form-label mb-1">Ubicación</label>
            <input id="uloc" class="form-control form-control-sm bg-light"
                   bind:value={state.usuario.ubicacion} disabled />
          </div>

          <div class="col-12 col-md-6 col-lg-2">
            <label for="usup" class="form-label mb-1">Supervisor ID</label>
            <input id="usup" class="form-control form-control-sm bg-light"
                   bind:value={state.usuario.supervisor} disabled />
          </div>

          <div class="col-12 col-md-6 col-lg-2">
            <label for="usupmail" class="form-label mb-1">Correo de Supervisor</label>
            <input id="usupmail" type="email" class="form-control form-control-sm bg-light"
                   bind:value={state.usuario.correoSupervisor} disabled />
          </div>
        </div>

        <!-- Técnico -->
        <div class="mt-2">
          <label for="tecnico" class="form-label mb-1 fw-bold">Técnico</label>
          <select id="tecnico" class="form-select form-select-sm"
                  bind:value={state.tecnico} on:change={onTecnicoChange}>
            <option value="">Selecciona técnico…</option>
            <option>SANCHG27 - Gaston Sanchez (Monterrey IT)</option>
            <option>LICONJ3 - Juan Pérez (Monterrey IT)</option>
            <option>FOOBR1 - Foo Bar (CDMX IT)</option>
          </select>
        </div>

        <!-- Dispositivo -->
        <div class="mt-2">
          <label class="form-label mb-1 fw-bold">Dispositivo</label>
          <div class="row g-2">
            <div class="col-12 col-md">
              <input class="form-control form-control-sm" placeholder="Descripción (opcional)"
                     bind:value={descripcionAsignar} />
            </div>
            <div class="col-12 col-md-4">
              <input class="form-control form-control-sm" placeholder="Número de serie"
                     bind:value={numeroSerieAsignar} />
            </div>
            <div class="col-12 col-md-auto d-grid">
              <button class="btn btn-primary btn-sm" on:click={asignar}>Asignar Dispositivo</button>
            </div>
          </div>
        </div>

        <!-- Tipo de Asignación -->
        <div class="mt-2">
          <label for="tipo" class="form-label mb-1 fw-bold">Tipo de Asignación</label>
          <select id="tipo" class="form-select form-select-sm"
                  bind:value={state.tipoAsignacion} on:change={onTipoAsignacionChange}>
            <option value="">Selecciona…</option>
            <option>PC Refresh</option>
            <option>Alta</option>
            <option>Cambio</option>
            <option>Baja</option>
          </select>
        </div>

        <!-- Asignados -->
        <div class="mt-3">
          <div class="fw-bold mb-2">Lista de Dispositivos Asignados</div>
          <div class="table-responsive border rounded">
            <table class="table table-sm align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Descripción Dispositivo</th>
                  <th>Asset Tag</th>
                  <th>Número de Serie</th>
                  <th>Accesorio</th>
                </tr>
              </thead>
              <tbody>
                {#each state.asignados as d, i}
                  <tr>
                    <td>{d.descripcion}</td>
                    <td><input class="form-control form-control-sm" value={d.assetTag} on:input={updateAsignado(i,'assetTag')} /></td>
                    <td>{d.numeroSerie}</td>
                    <td><input class="form-control form-control-sm" value={d.accesorio} on:input={updateAsignado(i,'accesorio')} /></td>
                  </tr>
                {/each}
                {#if state.asignados.length === 0}
                  <tr><td colspan="4" class="text-muted">Sin dispositivos asignados.</td></tr>
                {/if}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Retirar -->
        <div class="mt-3">
          <div class="form-label mb-1 fw-bold">Retirar Dispositivo</div>
          <div class="row g-2">
            <div class="col-12 col-md">
              <input class="form-control form-control-sm" placeholder="Ej: SN987654321"
                     bind:value={numeroSerieRetirar} />
            </div>
            <div class="col-12 col-md-auto d-grid">
              <button class="btn btn-warning btn-sm text-white" on:click={retirar}>Retirar Dispositivo</button>
            </div>
          </div>
        </div>

        <!-- Retirados -->
        <div class="mt-3">
          <div class="fw-bold mb-2">Lista de Dispositivos Retirados</div>
          <div class="table-responsive border rounded">
            <table class="table table-sm align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Descripción Dispositivo</th>
                  <th>Asset Tag</th>
                  <th>Número de Serie</th>
                  <th>Accesorio</th>
                </tr>
              </thead>
              <tbody>
                {#each state.retirados as d, i}
                  <tr>
                    <td>{d.descripcion}</td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        value={d.assetTag}
                        on:input={updateRetirado(i, 'assetTag')}
                      />
                    </td>
                    <td>{d.numeroSerie}</td>
                    <td>
                      <input
                        class="form-control form-control-sm"
                        value={d.accesorio}
                        on:input={updateRetirado(i, 'accesorio')}
                      />
                    </td>
                  </tr>
                {/each}
                {#if state.retirados.length === 0}
                  <tr>
                    <td colspan="4" class="text-muted">Sin dispositivos retirados.</td>
                  </tr>
                {/if}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Botón final -->
        <div class="mt-3 d-flex justify-content-center">
          <button class="btn btn-success" on:click={generarCarta}>Generar carta de asignación</button>
        </div>
      </div>
    </div>
  </div>
</div>