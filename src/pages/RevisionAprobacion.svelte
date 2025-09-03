<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { carta, type Carta } from '../stores/cartas';

  // Estado global cargado desde la pantalla anterior
  $: state = $carta as Carta;

  // Helpers de presentación
  const dash = (v?: string) => (v && v.trim() ? v : '—');
  $: supervisorLinea = [dash(state.supervisorId), dash(state.correoSupervisor)]
    .filter((x) => x !== '—')
    .join(' · ') || '—';

  // Control de autorización (checkbox)
  let acepto = false;

  // Ruta a la carta final (ajústala si es diferente)
  const CARTA_ROUTE = '/carta';

  function autorizarCarta() {
    if (!acepto) return;
    push(CARTA_ROUTE);
  }
</script>

<div class="container py-4">
  <div class="card shadow-sm">
    <div class="card-body">
      <h2 class="h3 text-center mb-3">Revisión y Aprobación de Carta</h2>
      <p class="text-center text-muted mb-4">
        Verifica la siguiente información antes de autorizar la generación de la carta para el usuario.
      </p>

      <div class="d-flex justify-content-start mb-3">
        <span class="badge text-bg-light">
          Aprobador detectado: <strong>{dash(state.aprobadorDetectado) || 'ADMIN'}</strong>
        </span>
      </div>

      <!-- Datos del usuario -->
      <div class="table-responsive mb-4">
        <table class="table table-bordered align-middle">
          <tbody>
            <tr>
              <th class="head">Nombre</th>
              <td>{dash(state.nombreUsuario)}</td>
            </tr>
            <tr>
              <th class="head">User ID</th>
              <td>{dash(state.usuario)}</td>
            </tr>
            <tr>
              <th class="head">Email</th>
              <td>{dash(state.correoUsuario)}</td>
            </tr>
            <tr>
              <th class="head">Ubicación</th>
              <td>{dash(state.ubicacionUsuario)}</td>
            </tr>
            <tr>
              <th class="head">Supervisor</th>
              <td>{supervisorLinea}</td>
            </tr>
            <tr>
              <th class="kv-head">FOLIO</th>
              <td>PCR0000001</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Asignados -->
      <h5 class="mb-2">Lista de Dispositivos Asignados</h5>
      <div class="table-responsive mb-4">
        <table class="table table-sm table-bordered align-middle">
          <thead>
            <tr class="table-primary">
              <th style="width:40%">Descripción</th>
              <th style="width:15%">Asset Tag</th>
              <th style="width:20%">Número de Serie</th>
              <th style="width:25%">Accesorio</th>
            </tr>
          </thead>
          <tbody>
            {#if state.asignados.length === 0}
              <tr>
                <td colspan="4" class="text-muted">Sin dispositivos asignados.</td>
              </tr>
            {:else}
              {#each state.asignados as d}
                <tr>
                  <td>{dash(d.descripcion)}</td>
                  <td>{dash(d.assetTag)}</td>
                  <td>{dash(d.numeroSerie)}</td>
                  <td>{dash(d.accesorio) || 'N/A'}</td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>

      <!-- Retirados -->
      <h5 class="mb-2">Lista de Dispositivos Retirados</h5>
      <div class="table-responsive mb-4">
        <table class="table table-sm table-bordered align-middle">
          <thead>
            <tr class="table-primary">
              <th style="width:40%">Descripción</th>
              <th style="width:15%">Asset Tag</th>
              <th style="width:20%">Número de Serie</th>
              <th style="width:25%">Accesorio</th>
            </tr>
          </thead>
          <tbody>
            {#if state.retirados.length === 0}
              <tr>
                <td colspan="4" class="text-muted">Sin dispositivos retirados.</td>
              </tr>
            {:else}
              {#each state.retirados as d}
                <tr>
                  <td>{dash(d.descripcion)}</td>
                  <td>{dash(d.assetTag)}</td>
                  <td>{dash(d.numeroSerie)}</td>
                  <td>{dash(d.accesorio) || 'N/A'}</td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
      </div>

      <!-- Pie como en la captura: checkbox + botón centrado -->
      <div class="mt-3">
        <div class="form-check">
          <input
            id="chkAutorizo"
            class="form-check-input"
            type="checkbox"
            bind:checked={acepto} />
          <label class="form-check-label" for="chkAutorizo">
            He revisado y autorizo esta carta.
          </label>
        </div>

        <div class="d-flex justify-content-center mt-3">
          <button
            class="btn btn-success px-4"
            on:click={autorizarCarta}
            disabled={!acepto}>
            Autorizar Carta
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .head {
    width: 220px;
    background-color: #0d3b66;
    color: #fff;
  }
</style>