<script lang="ts">
  import { carta } from '../stores/cartas';
  import { push } from 'svelte-spa-router';

  let usuario = '';
  let password = '';

  function entrar() {
    if (!usuario || !password) return;
    carta.update(c => ({ ...c, aprobadorDetectado: usuario.toUpperCase() }));
    push('/control');
  }
</script>

<div class="min-h-screen grid place-items-center">
  <div class="bg-white w-full max-w-md rounded-2xl shadow p-8">
    <!-- Logos CENTRADOS y GRANDES -->
    <div class="mb-6 flex justify-center">
      <div class="flex items-center gap-10">
        <img src="/gitplus.jpg" alt="GIT+" class="h-10 md:h-12 w-auto object-contain" />
        <img src="/whirlpool.jpg" alt="Whirlpool" class="h-14 md:h-16 w-auto object-contain" />
      </div>
    </div>

    <h1 class="text-center text-xl font-semibold">Acceso</h1>
    <p class="text-center text-gray-500 mb-6">Panel de Cartas de Asignación</p>

    <label for="login-usuario" class="block text-sm font-medium mb-1">Usuario</label>
    <input id="login-usuario" class="w-full border rounded-lg px-3 py-2 mb-4"
           placeholder="Ej. LICONJ3" bind:value={usuario} />

    <label for="login-password" class="block text-sm font-medium mb-1">Contraseña</label>
    <input id="login-password" class="w-full border rounded-lg px-3 py-2 mb-6"
           type="password" bind:value={password} />

    <button class="w-full rounded-lg bg-blue-600 text-white font-medium py-2.5 hover:bg-blue-700"
            on:click={entrar}>
      Entrar
    </button>

    <p class="text-center text-xs text-gray-500 mt-6">© 2025 GTIM — Demo</p>
  </div>
</div>