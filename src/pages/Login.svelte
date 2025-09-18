<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';

  import { carta } from '../stores/cartas';
  import { loginWithPassword, loginWithGoogle } from '../lib/api';
  import { setAuth } from '../lib/http';

  let usuario = '';
  let password = '';
  let cargando = false;
  let error = '';

  const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || 'TU_CLIENT_ID.apps.googleusercontent.com';
  let cargandoGoogle = false;

  function aplicarToken(resp: { access_token: string; token_type?: string }) {
    if (!resp?.access_token) throw new Error('Token vacio');
    const tokenType = typeof resp.token_type === 'string' ? resp.token_type : 'Bearer';
    localStorage.setItem('access_token', resp.access_token);
    localStorage.setItem('token_type', tokenType);
    setAuth(resp.access_token);
  }

  async function entrar() {
    error = '';
    if (!usuario || !password) {
      error = 'Ingresa usuario y contrasena';
      return;
    }

    cargando = true;
    try {
      const resp = await loginWithPassword(usuario, password);
      aplicarToken(resp);
      carta.update((c) => ({ ...c, aprobadorDetectado: usuario.toUpperCase() }));
      push('/control');
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Error de inicio de sesion';
      error = msg || 'No se pudo iniciar sesion';
    } finally {
      cargando = false;
    }
  }

  function decodeJwtName(idToken: string): string | null {
    try {
      const parts = idToken.split('.');
      if (parts.length < 2) return null;
      const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
      return (payload?.name || payload?.email || '').toString() || null;
    } catch {
      return null;
    }
  }

  async function handleCredentialResponse(res: any) {
    error = '';
    if (!res?.credential) {
      error = 'Token de Google no disponible';
      return;
    }

    cargandoGoogle = true;
    try {
      const apiResp = await loginWithGoogle(res.credential);
      aplicarToken(apiResp);
      const nombre = decodeJwtName(res.credential)?.toUpperCase?.() ?? 'USUARIO';
      carta.update((c) => ({ ...c, aprobadorDetectado: nombre }));
      push('/control');
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Error de Google';
      error = `Login con Google fallo: ${msg}`;
    } finally {
      cargandoGoogle = false;
    }
  }

  onMount(() => {
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      // @ts-ignore
      google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: handleCredentialResponse
      });
      // @ts-ignore
      google.accounts.id.renderButton(
        document.getElementById('google-signin'),
        { theme: 'outline', size: 'large', width: 320 }
      );
    };
    document.head.appendChild(script);
  });
</script>

<div class="min-vh-100 d-grid place-items-center bg-body-tertiary">
  <div class="card shadow" style="max-width: 520px; width: 92%;">
    <div class="card-body text-center">
      <div class="d-flex align-items-center justify-content-between mb-2 px-1 position-relative">
        <img src="/gitplus.jpg" alt="GIT+" class="logo-gitplus" />
        <img src="/whirlpool.jpg" alt="Whirlpool" class="logo-whirlpool" />
      </div>

      <h1 class="h4 mt-2">Acceso</h1>
      <p class="text-secondary mb-4">Panel de Cartas de Asignacion</p>

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

      <label for="login-password" class="form-label text-start w-100">Contrasena</label>
      <input
        id="login-password"
        type="password"
        class="form-control mb-3"
        bind:value={password}
        on:keydown={(e) => e.key === 'Enter' && entrar()}
      />

      <button class="btn btn-primary w-100 mb-3" on:click={entrar} disabled={cargando}>
        {cargando ? 'Entrando...' : 'Entrar'}
      </button>

      <div class="sep">
        <span>o</span>
      </div>

      <div id="google-signin" class="mb-2"></div>
      {#if cargandoGoogle}
        <div class="text-secondary" style="font-size:.9rem">Validando con Google...</div>
      {/if}

      <p class="text-secondary-emphasis mt-4 mb-0" style="font-size:.8rem">(c) 2025 GTIM - Demo</p>
    </div>
  </div>
</div>

<style>
  .place-items-center { place-items: center; }

  .logo-gitplus { height: 42px; width: auto; }
  .logo-whirlpool { height: 70px; width: auto; }

  .sep {
    position: relative;
    text-align: center;
    margin: 10px 0 14px;
  }
  .sep::before, .sep::after {
    content: '';
    display: inline-block;
    width: 40%;
    height: 1px;
    background: #ddd;
    vertical-align: middle;
  }
  .sep span {
    display: inline-block;
    margin: 0 8px;
    color: #888;
    font-size: .9rem;
    vertical-align: middle;
  }

  @media (max-width: 480px) {
    .logo-gitplus { height: 36px; }
    .logo-whirlpool { height: 32px; }
  }
</style>