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

/**
 * Esta función es la CLAVE. 
 * Si el campo 'img' de la DB es "perro.webp", 
 * lo convierte en "http://127.0.0.1:8000/fotos/perro.webp"
 */
const resolverRutaImagen = (ruta) => {
  if (!ruta) return 'https://via.placeholder.com/200'
  
  // Si ya empieza por http (como el placeholder), no tocamos nada
  if (ruta.startsWith('http')) return ruta
  
  // Si es solo el nombre del archivo, le pegamos la ruta de tu Django
  return `http://127.0.0.1:8000/fotos/${ruta}`
}
</script>

<template>
  <main style="padding: 20px;">
    <h1 style="color: #d4a373;">🧵 Catálogo de Productos</h1>
    
    <div v-if="errorMsg" style="color: #d9534f; background: #f8d7da; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
      {{ errorMsg }}
    </div>

    <div v-if="productos.length > 0" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">
      <div v-for="p in productos" :key="p.id" style="border: 1px solid #e9edc9; padding: 15px; border-radius: 10px; background: #fefae0; display: flex; flex-direction: column;">
        
        <img 
          :src="resolverRutaImagen(p.img)" 
          :alt="p.nombre" 
          @error="(e) => console.error('Error cargando imagen:', e.target.src)"
          style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px;" 
        />

        <h3 style="margin: 0 0 10px 0; color: #283618;">{{ p.nombre }}</h3>
        <p style="margin: 0 0 15px 0; color: #bc6c25; font-size: 1.2rem;"><strong>{{ p.precio }}€</strong></p>
        
        <router-link :to="'/producto/' + p.id" style="background: #606c38; color: white; text-align: center; padding: 10px; border-radius: 6px; font-weight: bold; margin-top: auto; text-decoration: none;">
          Ver detalles
        </router-link>
      </div>
    </div>
    <div v-else-if="!errorMsg" style="text-align: center; color: #606c38; padding: 40px; font-size: 1.2rem;">
      Cargando catálogo...
    </div>
  </main>
</template>