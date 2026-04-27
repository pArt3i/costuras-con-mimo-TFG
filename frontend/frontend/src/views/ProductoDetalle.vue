<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const producto = ref(null)
const imagenPrincipal = ref('')
const cargando = ref(true)
const añadiendo = ref(false)

// Función para resolver la ruta de la imagen (la misma que usamos en la tienda)
const resolverRutaImagen = (ruta) => {
  if (!ruta) return 'https://via.placeholder.com/400'
  if (ruta.startsWith('http')) return ruta
  return `http://127.0.0.1:8000/fotos/${ruta}`
}

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/productos/${route.params.id}/`)
    producto.value = response.data
    imagenPrincipal.value = resolverRutaImagen(response.data.img)
    cargando.value = false
  } catch (error) {
    console.error("Error al cargar los detalles:", error)
    cargando.value = false
  }
})

const seleccionarImagen = (url) => {
  imagenPrincipal.value = resolverRutaImagen(url)
}

// --- FUNCIÓN ACTUALIZADA PARA LA CESTA MIXTA ---
const añadirAlCarrito = async () => {
  añadiendo.value = true
  try {
    // 1. Obtenemos el ID del usuario del localStorage (o usamos 1 por defecto para pruebas)
    // Lo ideal es tener un sistema de perfil, pero para que funcione ahora:
    const userId = 1 

    const payload = {
      id_usuario: userId,
      id_producto: producto.value.id, // 👈 ENVIAMOS EL ID DEL PRODUCTO (CATÁLOGO)
      id_tejido: null,               // No es personalizado
      producto_type: producto.value.nombre,
      precio: producto.value.precio,
      bordado: '',
      estado: 'CARRITO'
    }

    await axios.post('http://127.0.0.1:8000/api/encargos/', payload)

    // Emitimos el evento para actualizar el contador de la Navbar
    window.dispatchEvent(new CustomEvent('carrito-actualizado'))

    alert("¡Añadido a la cesta correctamente!")
    router.push('/carrito')

  } catch (error) {
    console.error("Error al añadir al carrito:", error)
    alert("No se pudo añadir el producto.")
  } finally {
    añadiendo.value = false
  }
}
</script>

<template>
<div class="container" v-if="!cargando && producto">
    <div class="producto-detalle">
    
    <div class="galeria-seccion">
        <img :src="imagenPrincipal" class="main-img" alt="Producto Principal" />
        <div class="thumbnails">
            <img 
              :src="resolverRutaImagen(producto.img)" 
              @click="seleccionarImagen(producto.img)" 
              class="thumb" 
              :class="{ activa: imagenPrincipal === resolverRutaImagen(producto.img) }"
            />
            <img 
              v-for="(foto, index) in producto.imagenes_extra" 
              :key="index" 
              :src="resolverRutaImagen(foto.img_url)" 
              @click="seleccionarImagen(foto.img_url)" 
              class="thumb" 
              :class="{ activa: imagenPrincipal === resolverRutaImagen(foto.img_url) }"
            />
        </div>
    </div>

    <div class="info-seccion">
        <span class="categoria-tag">{{ producto.categoria_nombre }}</span>
        <h1>{{ producto.nombre }}</h1>
        <p class="precio">{{ producto.precio.toFixed(2) }}€</p>
        <hr />
        <p class="descripcion">Producto artesanal confeccionado con materiales de alta calidad.</p>
        
        <div class="stock-info">
            <span>Disponibilidad: </span>
            <strong :class="producto.stock > 0 ? 'in-stock' : 'no-stock'">
                {{ producto.stock > 0 ? 'En Stock (' + producto.stock + ')' : 'Agotado' }}
            </strong>
        </div>

        <div class="acciones">
            <button 
                class="btn-carrito" 
                :disabled="producto.stock <= 0 || añadiendo"
                @click="añadirAlCarrito"
            >
                {{ añadiendo ? 'Añadiendo...' : 'Añadir a la cesta' }}
            </button>
            <router-link to="/" class="btn-volver">Volver al catálogo</router-link>
        </div>
    </div>
    </div>
</div>
<div v-else-if="cargando" class="loading">Cargando producto...</div>
</template>

<style scoped>
.producto-detalle { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 20px; }
.main-img { width: 100%; height: 450px; object-fit: cover; border-radius: 15px; }
.thumbnails { display: flex; gap: 10px; margin-top: 15px; }
.thumb { width: 80px; height: 80px; object-fit: cover; cursor: pointer; border: 2px solid transparent; border-radius: 8px; }
.thumb.activa { border-color: #606c38; }
.precio { font-size: 2rem; color: #bc6c25; font-weight: bold; }
.btn-carrito { background: #606c38; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; font-size: 1.1rem; }
.btn-carrito:disabled { background: #a3ad8d; }
.in-stock { color: #2a9d8f; }
.no-stock { color: #e76f51; }
</style>