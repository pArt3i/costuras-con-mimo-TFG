<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const items = ref([])
const cargando = ref(true)
const pagando = ref(false)

const resolverImagen = (item) => {
  if (item.id_producto) {
    const ruta = item.producto_img
    return ruta.startsWith('http') ? ruta : `http://127.0.0.1:8000/fotos/${ruta}`
  }
  return 'https://via.placeholder.com/150?text=Personalizado'
}

const cargarCarrito = async () => {
  try {
    cargando.value = true
    const response = await axios.get('http://127.0.0.1:8000/api/encargos/')
    
    let cestaBruta = response.data.filter(i => i.estado === 'CARRITO')
    
    items.value = cestaBruta.map(item => ({
      ...item,
      cantidad: item.cantidad || 1 
    }))

  } catch (error) {
    console.error("Error al cargar el carrito:", error)
  } finally {
    cargando.value = false
  }
}

const cambiarCantidad = async (item, variacion) => {
  const nuevaCantidad = item.cantidad + variacion

  if (nuevaCantidad < 1) {
    if (confirm("¿Quieres quitar este artículo de la cesta?")) {
      await eliminarItemReal(item.id)
    }
    return
  }

  item.cantidad = nuevaCantidad

  try {
    await axios.patch(`http://127.0.0.1:8000/api/encargos/${item.id}/`, { cantidad: nuevaCantidad })
    window.dispatchEvent(new CustomEvent('carrito-actualizado'))
  } catch (error) {
    console.error("Error al cambiar cantidad", error)
    item.cantidad -= variacion
  }
}

const eliminarItemReal = async (id) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/encargos/${id}/`)
    items.value = items.value.filter(i => i.id !== id)
    window.dispatchEvent(new CustomEvent('carrito-actualizado'))
  } catch (error) {
    alert("No se pudo eliminar el producto")
  }
}

const total = computed(() => {
  return items.value.reduce((acc, item) => acc + (item.precio * item.cantidad), 0)
})

const irAPagar = async () => {
  pagando.value = true
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/encargos/finalizar_pedido/')
    if (response.data.url) {
      window.location.href = response.data.url
    }
  } catch (error) {
    alert("Error al conectar con la pasarela.")
  } finally {
    pagando.value = false
  }
}

onMounted(cargarCarrito)
</script>

<template>
  <div class="container">
    <h1 class="titulo">Tu Cesta de Compra</h1>

    <div v-if="cargando" class="msg">Cargando tu pedido...</div>
    
    <div v-else-if="items.length === 0" class="carrito-vacio">
      <p>No tienes nada en la cesta todavía.</p>
      <router-link to="/" class="btn-comprar">Ir al catálogo</router-link>
    </div>

    <div v-else class="carrito-layout">
      <div class="productos-lista">
        <div v-for="item in items" :key="item.id" class="item-carrito">
          <img :src="resolverImagen(item)" class="item-img" />
          
          <div class="item-info">
            <h3>{{ item.producto_type }}</h3>
            <div v-if="!item.id_producto" class="detalles-personalizado">
              <p><strong>Tela:</strong> {{ item.tejido_nombre }}</p>
              <p><strong>Bordado:</strong> "{{ item.bordado }}"</p>
              <span class="badge-personalizado">✨ Diseño Único</span>
            </div>
          </div>

          <div class="item-precio">
            <span class="precio-unitario" v-if="item.cantidad > 1">{{ item.precio.toFixed(2) }}€ / ud</span>
            <p>{{ (item.precio * item.cantidad).toFixed(2) }}€</p>
          </div>

          <div class="item-controles">
            <button @click="cambiarCantidad(item, 1)" class="btn-cant btn-mas">+</button>
            <span class="numero-cant">{{ item.cantidad }}</span>
            <button @click="cambiarCantidad(item, -1)" class="btn-cant btn-menos">-</button>
          </div>
        </div>
      </div>

      <div class="resumen">
        <h2>Resumen</h2>
        <div class="fila-resumen">
          <span>Artículos:</span>
          <span>{{ total.toFixed(2) }}€</span>
        </div>
        <div class="fila-resumen total">
          <span>Total:</span>
          <span>{{ total.toFixed(2) }}€</span>
        </div>
        
        <button @click="irAPagar" class="btn-pagar" :disabled="pagando">
          {{ pagando ? 'Conectando...' : 'Pagar Pedido' }}
        </button>
      </div>
    </div>
  </div>
</template>
