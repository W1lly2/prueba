<script lang="ts">
  import { get } from 'svelte/store';
  import { push } from 'svelte-spa-router';
  import { carta, type Carta } from '../stores/cartas';

  let state: Carta = get(carta);
  let acepta = state.aceptoTerminos ?? false;

  const fechaUTC = new Date().toUTCString();

  // Estado del pop-up
  let showModal = false;

  function enviar() {
    if (!acepta) return;
    carta.update((c) => ({ ...c, aceptoTerminos: true }));
    showModal = true; // abre el pop-up
  }
  function cerrarModal() { showModal = false; }
  function irInicio() { showModal = false; push('/'); }

  // Evita scroll del fondo cuando el modal está abierto
  $: document?.body && (document.body.style.overflow = showModal ? 'hidden' : '');
</script>

<div class="min-h-screen bg-page" inert={showModal}>
  <div class="container-ideal py-3">
    <div class="card shadow-sm">
      <div class="card-body">

        <!-- Encabezado: fecha arriba/derecha y título centrado -->
        <div class="position-relative pt-1 mb-3">
          <div class="small text-muted position-absolute top-0 end-0">
            {fechaUTC}
          </div>
          <h1 class="h3 text-navy text-center mt-4 mb-0">
            Carta de Asignación de Equipo
          </h1>
        </div>

        <!-- Aviso amarillo -->
        <div class="note-banner mb-3">
          <strong>Leer detenidamente</strong> - <em>Política de uso de dispositivos tecnológicos.</em>
        </div>

        <!-- Datos del usuario -->
        <div class="table-responsive mb-3">
          <table class="table table-bordered align-middle small mb-0">
            <tbody>
              <tr>
                <th class="kv-head">NOMBRE</th>
                <td>{state.nombreUsuario || '—'}</td>
              </tr>
              <tr>
                <th class="kv-head">USER ID</th>
                <td>{state.usuario || '—'}</td>
              </tr>
              <tr>
                <th class="kv-head">EMAIL</th>
                <td>{state.correoUsuario || '—'}</td>
              </tr>
              <tr>
                <th class="kv-head">UBICACIÓN</th>
                <td>{state.ubicacionUsuario || '—'}</td>
              </tr>
              <tr>
                <th class="kv-head">SUPERVISOR</th>
                <td>
                  {#if state.supervisorId || state.correoSupervisor}
                    {state.supervisorId || '—'}{state.correoSupervisor ? ` · ${state.correoSupervisor}` : ''}
                  {:else}
                    —
                  {/if}
                </td>
              </tr>
              <tr>
                <th class="kv-head">FOLIO</th>
                <td>PCR0000001</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Asignados -->
        <div class="mb-3">
          <h2 class="section-title-lg">Lista de Dispositivos Asignados</h2>
          {#if state.asignados.length > 0}
            {#each state.asignados as d, i}
              <div class="small text-muted mb-1">Dispositivo #{i + 1}</div>
              <div class="table-responsive mb-3">
                <table class="table table-sm table-bordered align-middle table-navy mb-0">
                  <thead>
                    <tr>
                      <th>DESCRIPCIÓN</th>
                      <th>ASSET TAG</th>
                      <th>NÚMERO DE SERIE</th>
                      <th>ACCESORIO</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{d.descripcion || '—'}</td>
                      <td>{d.assetTag || 'N/A'}</td>
                      <td>{d.numeroSerie || '—'}</td>
                      <td>{d.accesorio || 'N/A'}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            {/each}
          {:else}
            <div class="text-muted small">Sin dispositivos asignados.</div>
          {/if}
        </div>

        <!-- Retirados -->
        <div class="mb-3">
          <h2 class="section-title-lg">Lista de Dispositivos Retirados</h2>
          {#if state.retirados.length > 0}
            {#each state.retirados as d, i}
              <div class="small text-muted mb-1">Dispositivo Retirado #{i + 1}</div>
              <div class="table-responsive mb-3">
                <table class="table table-sm table-bordered align-middle table-navy mb-0">
                  <thead>
                    <tr>
                      <th>DESCRIPCIÓN</th>
                      <th>ASSET TAG</th>
                      <th>NÚMERO DE SERIE</th>
                      <th>ACCESORIO</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>{d.descripcion || '—'}</td>
                      <td>{d.assetTag || 'N/A'}</td>
                      <td>{d.numeroSerie || '—'}</td>
                      <td>{d.accesorio || 'N/A'}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            {/each}
          {:else}
            <div class="text-muted small">Sin dispositivos retirados.</div>
          {/if}
        </div>

        <!-- Texto legal + checkbox -->
        <p class="small text-muted">
          Por medio de la presente declaro que he recibido los dispositivos tecnológicos antes mencionados.
          Asumo la responsabilidad de su guarda y cuidado, y me comprometo a cumplir con la
          <a href="#/politica-uso" class="link-primary">Política de uso de Dispositivos Tecnológicos</a>
          definida por la empresa.
        </p>

        <div class="form-check mb-3">
          <input id="chk-acepta" class="form-check-input" type="checkbox" bind:checked={acepta} />
          <label for="chk-acepta" class="form-check-label small">
            Acepto los términos y condiciones
          </label>
        </div>

        <!-- Botón ancho completo -->
        <div class="mt-3">
          <button class="btn btn-navy w-100 py-2" disabled={!acepta} on:click={enviar}>
            Enviar Aceptación
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Pop-up (modal) -->
{#if showModal}
  <div
    class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center"
    style="background: rgba(0,0,0,.5); z-index: 1055;"
  >
    <div class="card shadow" style="max-width: 480px; width: 92%;">
      <div class="card-body text-center">
        <h5 class="mb-2 text-navy">¡Aceptación registrada!</h5>
        <p class="text-muted small mb-3">
          Esta es una demo: aún no se envía correo ni se guarda en servidor.
        </p>
        <button class="btn btn-navy w-100" on:click={irInicio}>Ir al inicio</button>
      </div>
    </div>
  </div>
{/if}
