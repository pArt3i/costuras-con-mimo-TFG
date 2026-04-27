<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const productos = ref([])
const errorMsg = ref('')

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/productos/')
    productos.value = response.data
    console.log("Productos cargados:", productos.value)
  } catch (error) {
    errorMsg.value = "Error al conectar con el servidor"
    console.error(error)
  }
})

const resolverRutaImagen = (ruta) => {
  if (!ruta) return 'https://via.placeholder.com/200'
  
  if (ruta.startsWith('http')) return ruta
  
  return `http://127.0.0.1:8000/fotos/${ruta}`
}
</script>

<template>
  <main class="catalogo-main">
    <h1 class="catalogo-titulo">🧵 Catálogo de Productos</h1>
    
    <div v-if="errorMsg" class="alerta-error">
      {{ errorMsg }}
    </div>

    <div v-if="productos.length > 0" class="productos-grid">
      <div v-for="p in productos" :key="p.id" class="producto-card">
        
        <img 
          :src="resolverRutaImagen(p.img)" 
          :alt="p.nombre" 
          @error="(e) => console.error('Error cargando imagen:', e.target.src)"
          class="producto-img"
        />

        <h3 class="producto-titulo">{{ p.nombre }}</h3>
        <p class="producto-precio-etiqueta"><strong>{{ p.precio }}€</strong></p>
        
        <router-link :to="'/producto/' + p.id" class="btn-ver-detalles">
          Ver detalles
        </router-link>
      </div>
    </div>
    <div v-else-if="!errorMsg" style="text-align: center; color: #606c38; padding: 40px; font-size: 1.2rem;">
      Cargando catálogo...
    </div>
  </main>
</template>