<script lang="ts">
  import { carta } from '../stores/cartas';
  import { push } from 'svelte-spa-router';

  let usuario = '';
  let password = '';
  let cargando = false;
  let error = '';

  async function entrar() {
    error = '';
    if (!usuario || !password) return;

    cargando = true;
    try {
      // aquí podrías llamar al endpoint de login (cuando exista)
      // por ahora solo guardamos el aprobador y navegamos
      carta.update(c => ({ ...c, aprobadorDetectado: usuario.toUpperCase() }));
      push('/control');
    } catch (e) {
      error = 'No se pudo iniciar sesión';
    } finally {
      cargando = false;
    }
  }
</script>

<div class="min-vh-100 d-grid place-items-center bg-body-tertiary">
  <div class="card shadow" style="max-width: 520px; width: 92%;">
    <div class="card-body text-center">
      <!-- Logos arriba del título -->
      <div class="d-flex align-items-center justify-content-between mb-2 px-1 position-relative">
        <img src="/gitplus.jpg" alt="GIT+" class="logo-gitplus" />
        <img src="/whirlpool.jpg" alt="Whirlpool" class="logo-whirlpool" />
      </div>

      <h1 class="h4 mt-2">Acceso</h1>
      <p class="text-secondary mb-4">Panel de Cartas de Asignación</p>

      {#if error}
        <div class="alert alert-danger py-2">{error}</div>
      {/if}

      <label for="login-usuario" class="form-label text-start w-100">Usuario</label>
      <input
        id="login-usuario"
        class="form-control mb-3"
        placeholder="Ej. LICONJ3"
        bind:value={usuario}
      />

      <label for="login-password" class="form-label text-start w-100">Contraseña</label>
      <input
        id="login-password"
        type="password"
        class="form-control mb-4"
        bind:value={password}
      />

      <button class="btn btn-primary w-100" on:click={entrar} disabled={cargando}>
        {cargando ? 'Entrando…' : 'Entrar'}
      </button>

      <p class="text-secondary-emphasis mt-4 mb-0" style="font-size:.8rem">© 2025 GTIM — Demo</p>
    </div>
  </div>
</div>

<style>
  .place-items-center { place-items: center; }

  /* Tamaños más grandes, responsivos */
  .logo-gitplus { height: 42px; width: auto; }
  .logo-whirlpool { height: 70px; width: auto; }

  @media (max-width: 480px) {
    .logo-gitplus { height: 36px; }
    .logo-whirlpool { height: 32px; }
  }
</style>