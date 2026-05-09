<script setup>
// No necesitamos mucha lógica aquí, solo visual
</script>

<template>
  <div class="not-found-container">
    <div class="content">
      <h1 class="error-code">404</h1>
      <div class="icon">🧶✂️</div>
      <h2>¡Ups! Nos hemos quedado sin hilo...</h2>
      <p>La página que intentas buscar se ha descosido o no existe en nuestro taller.</p>
      
      <router-link to="/" class="btn-home">
        🔙 Volver a la Tienda
      </router-link>
    </div>
  </div>
</template>
