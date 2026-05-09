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