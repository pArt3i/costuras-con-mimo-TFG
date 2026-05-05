<script setup>
// No necesita lógica extra, solo redirigir si el usuario quiere volver
</script>

<template>
  <div class="error-container">
    <div class="error-card">
      <div class="error-header">
        <h1 class="code">403</h1>
      </div>
      <div class="error-body">
        <div class="icon">🚫🔒</div>
        <h2>Entrada restringida</h2>
        <p>
          Lo sentimos, pero no tienes los permisos necesarios para acceder a esta sección del taller. 
          Esta zona está reservada exclusivamente para administradores.
        </p>
        
        <div class="actions">
          <router-link to="/" class="btn-primary">
            🏠 Ir a la Tienda
          </router-link>
          <button @click="$router.go(-1)" class="btn-secondary">
            ⬅️ Volver atrás
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #fefae0; /* Tu color crema de fondo */
  padding: 20px;
}

.error-card {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  overflow: hidden;
  text-align: center;
}

.error-header {
  background: #606c38; /* Tu verde militar */
  padding: 30px;
  color: #fefae0;
}

.code {
  font-size: 5rem;
  margin: 0;
  letter-spacing: 5px;
}

.error-body {
  padding: 40px 30px;
}

.icon {
  font-size: 3.5rem;
  margin-bottom: 20px;
}

h2 {
  color: #283618;
  margin-bottom: 15px;
  font-size: 1.8rem;
}

p {
  color: #606c38;
  line-height: 1.6;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  background-color: #bc6c25; /* Tu naranja tierra */
  color: white;
  text-decoration: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: bold;
  transition: background 0.3s;
}

.btn-primary:hover {
  background-color: #dda15e;
}

.btn-secondary {
  background-color: #f4f5f0;
  color: #283618;
  border: 1px solid #ccd5ae;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary:hover {
  background-color: #e9edc9;
}
</style>