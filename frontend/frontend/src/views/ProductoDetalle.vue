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

const añadirAlCarrito = async () => {
  añadiendo.value = true
  try {
    const userId = 1 

    const payload = {
      id_usuario: userId,
      id_producto: producto.value.id,
      id_tejido: null,
      producto_type: producto.value.nombre,
      precio: producto.value.precio,
      bordado: '',
      estado: 'CARRITO'
    }

    await axios.post('http://127.0.0.1:8000/api/encargos/', payload)

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

