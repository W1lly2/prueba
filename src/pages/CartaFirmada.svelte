<script lang="ts">
  function cerrar() {
    if (window.close) window.close();
    else history.back();
  }
</script>

<div class="page">
  <main class="card" role="dialog" aria-labelledby="titulo" aria-describedby="desc">
    <div class="icon">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="12" cy="12" r="12" class="bg" />
        <path d="M7 12.5l3 3 7-7" class="tick" />
      </svg>
    </div>

    <h1 id="titulo" class="title">
      La carta fue firmada correctamente y se envió una copia a su correo.
    </h1>
    <p id="desc" class="subtitle">Puede cerrar la pestaña.</p>

    <button class="btn" on:click={cerrar} aria-label="Cerrar mensaje">Cerrar</button>
  </main>
</div>

<style>
  .page {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 2rem;
    background: radial-gradient(1200px 600px at 50% -20%, #eef6f0, transparent),
                linear-gradient(180deg, #f7f9fb, #edf1f5);
  }
  .card {
    width: min(980px, 92vw);
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 20px 50px rgba(16, 24, 40, .08);
    padding: clamp(1.5rem, 3vw, 2.5rem) clamp(1.25rem, 3.5vw, 2.5rem);
    text-align: center;
  }
  .icon {
    display: grid;
    place-items: center;
    margin-bottom: 1rem;
  }
  svg { width: 72px; height: 72px; }
  .bg { fill: #e9f7ee; }
  .tick { fill: none; stroke: #197d4b; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }

  .title {
    margin: .25rem 0 .75rem;
    font-size: clamp(1.75rem, 3.2vw, 3rem);
    line-height: 1.15;
    color: #101828;
    font-weight: 800;
    letter-spacing: -.02em;
  }
  .subtitle {
    margin: 0 0 1.5rem;
    color: #475467;
    font-size: clamp(1rem, 1.2vw, 1.125rem);
  }
  .btn {
    display: inline-block;
    margin-top: .5rem;
    padding: 1rem 1.6rem;
    border: 1px solid #d0d5dd;
    border-radius: 10px;
    background: #fff;
    color: #101828;
    font-weight: 700;
    cursor: pointer;
    transition: box-shadow .2s, transform .02s;
  }
  .btn:hover { box-shadow: 0 6px 16px rgba(16, 24, 40, .08); }
  .btn:active { transform: translateY(1px); }
</style>