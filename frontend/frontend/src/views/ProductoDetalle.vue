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
  <div class="detalle-fondo">
    <div class="container" v-if="!cargando && producto">
      
      <div class="navegacion-superior">
        <router-link to="/" class="btn-regresar">
          <span class="flecha">←</span> Volver al catálogo
        </router-link>
      </div>

      <div class="producto-card-premium">
        <div class="galeria-seccion">
          <div class="main-img-wrapper">
            <img :src="imagenPrincipal" class="main-img-detail" alt="Producto Principal" />
          </div>
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
          <div class="header-info">
            <span class="categoria-badge">{{ producto.categoria_nombre }}</span>
            <h1>{{ producto.nombre }}</h1>
            <p class="precio-premium">{{ producto.precio.toFixed(2) }}<span>€</span></p>
          </div>
          
          <div class="separador"></div>
          
          <div class="cuerpo-info">
            <p class="descripcion-titulo">Descripción del artesano</p>
            <p class="descripcion">
              Cada pieza de "Costuras con Mimo" es única. Este producto ha sido confeccionado a mano 
              utilizando tejidos seleccionados de alta calidad, cuidando cada puntada para ofrecerte 
              un acabado impecable y duradero.
            </p>
            
            <div class="meta-info">
              <div class="stock-wrapper">
                <div class="punto-estado" :class="producto.stock > 0 ? 'bg-verde' : 'bg-rojo'"></div>
                <span :class="producto.stock > 0 ? 'texto-verde' : 'texto-rojo'">
                  {{ producto.stock > 0 ? 'Disponible en taller (' + producto.stock + ' unidades)' : 'Agotado temporalmente' }}
                </span>
              </div>
            </div>
          </div>

          <div class="acciones-compra">
            <button 
                class="btn-comprar" 
                :disabled="producto.stock <= 0 || añadiendo"
                @click="añadirAlCarrito"
            >
                <span v-if="!añadiendo">🛒 Añadir a la cesta</span>
                <span v-else>Procesando...</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="cargando" class="loading-screen">
      <div class="spinner"></div>
      <p>Buscando en el taller...</p>
    </div>
  </div>
</template>