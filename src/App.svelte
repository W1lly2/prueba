<script lang="ts">
  import Router from 'svelte-spa-router';
  import Login from './pages/Login.svelte';
  import Control from './pages/ControlAsignacion.svelte';
  import Revision from './pages/RevisionAprobacion.svelte';
  import Carta from './pages/CartaAceptacion.svelte';

  const routes = {
    '/': Login,
    '/control': Control,
    '/revision': Revision,
    '/carta': Carta
  };
</script>

<div class="min-h-screen bg-gray-50">
  <main class="pt-0">
    <Router {routes} />
  </main>
</div>