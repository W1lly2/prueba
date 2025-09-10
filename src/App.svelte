<script lang="ts">
  import Router from 'svelte-spa-router';

  import Login   from './pages/Login.svelte';
  import Control from './pages/ControlAsignacion.svelte';
  import Revision from './pages/RevisionAprobacion.svelte';
  import Carta   from './pages/CartaAceptacion.svelte';

  // NUEVO
  import YaAprobado   from './pages/YaAprobado.svelte';
  import CartaFirmada from './pages/CartaFirmada.svelte';

  const routes = {
    '/':        Login,
    '/control': Control,
    '/revision': Revision,
    '/carta':   Carta,

    // NUEVO
    '/ya-aprobado':   YaAprobado,
    '/carta-firmada': CartaFirmada,
  };
</script>

<main class="pt-0">
  <Router {routes} />
</main>