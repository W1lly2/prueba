<script lang="ts">
  import { get } from 'svelte/store';
  import { push } from 'svelte-spa-router';
  import { carta, type Carta } from '../stores/cartas';

  let state: Carta = get(carta);
  let acepta = false;

  function autorizar() {
    if (!acepta) return;
    push('/carta');
  }
</script>

<div class="min-h-screen bg-page">
  <div class="container-ideal py-3">
    <div class="card shadow-sm">
      <div class="card-body">
        <!-- TÍTULO EN AZUL -->
        <h1 class="h3 text-center mb-3 text-navy">Revisión y Aprobación de Carta</h1>

        <!-- Badge aprobador -->
        <div class="mb-2 d-flex">
          <span class="badge bg-primary-subtle text-primary border">
            Aprobador detectado:
            <strong class="ms-1">{state.aprobadorDetectado || '—'}</strong>
          </span>
        </div>

        <!-- TEXTO CENTRADO -->
        <p class="intro text-muted small">
          Verifica la siguiente información antes de autorizar la generación de la carta para el usuario.
        </p>

        <!-- TABLA DE INFORMACIÓN PRINCIPAL (cuadros azules en primera columna) -->
        <div class="table-responsive mb-3">
          <table class="table table-bordered align-middle small mb-0">
            <tbody>
              <tr><th class="kv-head">Nombre</th><td>{state.usuario.nombre || '—'}</td></tr>
              <tr><th class="kv-head">User ID</th><td>{state.usuario.id || '—'}</td></tr>
              <tr><th class="kv-head">Email</th><td>{state.usuario.correo || '—'}</td></tr>
              <tr><th class="kv-head">Ubicación</th><td>{state.usuario.ubicacion || '—'}</td></tr>
              <tr><th class="kv-head">Supervisor</th><td>{state.usuario.supervisor || '—'}</td></tr>
              <tr><th class="kv-head">FOLIO</th><td>{state.folio || '—'}</td></tr>
            </tbody>
          </table>
        </div>

        <!-- ASIGNADOS -->
        <div class="mb-3">
          <h2 class="section-title">Lista de Dispositivos Asignados</h2>

          {#if state.asignados.length > 0}
            {#each state.asignados as d, i}
              <div class="small text-muted mb-1">Dispositivo #{i + 1}</div>
              <div class="table-responsive mb-3">
                <table class="table table-sm table-bordered align-middle table-navy mb-0">
                  <thead>
                    <tr>
                      <th>Descripción</th>
                      <th>Asset Tag</th>
                      <th>Número de Serie</th>
                      <th>Accesorio</th>
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

        <!-- RETIRADOS -->
        <div class="mb-3">
          <h2 class="section-title">Lista de Dispositivos Retirados</h2>

          {#if state.retirados.length > 0}
            {#each state.retirados as d, i}
              <div class="small text-muted mb-1">Dispositivo Retirado #{i + 1}</div>
              <div class="table-responsive mb-3">
                <table class="table table-sm table-bordered align-middle table-navy mb-0">
                  <thead>
                    <tr>
                      <th>Descripción</th>
                      <th>Asset Tag</th>
                      <th>Número de Serie</th>
                      <th>Accesorio</th>
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

        <!-- CHECK + BOTÓN -->
        <div class="form-check mb-3">
          <input id="chk-ok" class="form-check-input" type="checkbox" bind:checked={acepta} />
          <label for="chk-ok" class="form-check-label small">
            He revisado y autorizo esta carta.
          </label>
        </div>

        <div class="mt-3">
          <button class="btn btn-success w-100 py-2" disabled={!acepta} on:click={autorizar}>
            Autorizar Carta
          </button>
        </div>
      </div>
    </div>
  </div>
</div>