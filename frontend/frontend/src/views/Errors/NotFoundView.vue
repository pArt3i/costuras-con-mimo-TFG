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

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f4f5f0; /* Fondo clarito */
  text-align: center;
  padding: 20px;
}

.content {
  background: white;
  padding: 50px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  max-width: 500px;
}

.error-code {
  font-size: 6rem;
  margin: 0;
  color: #ccd5ae; /* Verde muy clarito para que no sea agresivo */
  line-height: 1;
}

.icon {
  font-size: 4rem;
  margin: 20px 0;
}

h2 {
  color: #283618; /* Verde oscuro */
  margin-bottom: 15px;
}

p {
  color: #606c38;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.btn-home {
  display: inline-block;
  background-color: #bc6c25;
  color: #fefae0;
  text-decoration: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1.1rem;
  transition: background-color 0.3s;
}

.btn-home:hover {
  background-color: #a05a1d;
}
</style>