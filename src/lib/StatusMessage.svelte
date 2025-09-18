<script lang="ts">
  export let title: string;
  export let subtitle: string;
  export let maxWidth: string = '720px';
  export let onClose: () => void = () => {
    if (window.close) window.close();
    else history.back();
  };
</script>

<div class="status-page">
  <main class="status-card" role="dialog" aria-labelledby="titulo" aria-describedby="desc" style="--max-width: {maxWidth}">
    <div class="status-icon">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="12" cy="12" r="12" class="status-bg" />
        <path d="M7 12.5l3 3 7-7" class="status-tick" />
      </svg>
    </div>

    <h1 id="titulo" class="status-title">{title}</h1>
    <p id="desc" class="status-subtitle">{subtitle}</p>

    <button class="status-btn" on:click={onClose} aria-label="Cerrar mensaje">Cerrar</button>
  </main>
</div>
