<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const items = ref([])
const cargando = ref(true)
const pagando = ref(false)

// 1. Función para resolver rutas de imágenes
const resolverImagen = (item) => {
  if (item.id_producto) {
    const ruta = item.producto_img
    return ruta.startsWith('http') ? ruta : `http://127.0.0.1:8000/fotos/${ruta}`
  }
  return 'https://via.placeholder.com/150?text=Personalizado'
}

// 2. Cargar la cesta
const cargarCarrito = async () => {
  try {
    cargando.value = true
    const response = await axios.get('http://127.0.0.1:8000/api/encargos/')
    
    // Ahora simplemente cogemos todo lo que nos da Django (que ya viene filtrado por el token)
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

// 3. Modificar la Cantidad (+ y -)
const cambiarCantidad = async (item, variacion) => {
  const nuevaCantidad = item.cantidad + variacion

  // Si baja de 1, le preguntamos si quiere eliminarlo de la cesta
  if (nuevaCantidad < 1) {
    if (confirm("¿Quieres quitar este artículo de la cesta?")) {
      await eliminarItemReal(item.id)
    }
    return
  }

  // Actualizamos visualmente primero para que sea instantáneo
  item.cantidad = nuevaCantidad

  // Guardamos en la base de datos
  try {
    await axios.patch(`http://127.0.0.1:8000/api/encargos/${item.id}/`, { cantidad: nuevaCantidad })
    window.dispatchEvent(new CustomEvent('carrito-actualizado'))
  } catch (error) {
    console.error("Error al cambiar cantidad", error)
    // Si falla, revertimos
    item.cantidad -= variacion
  }
}

// Función interna para borrar si llega a 0
const eliminarItemReal = async (id) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/encargos/${id}/`)
    items.value = items.value.filter(i => i.id !== id)
    window.dispatchEvent(new CustomEvent('carrito-actualizado'))
  } catch (error) {
    alert("No se pudo eliminar el producto")
  }
}

// 4. Calcular el precio total (Multiplicando por la cantidad)
const total = computed(() => {
  return items.value.reduce((acc, item) => acc + (item.precio * item.cantidad), 0)
})

// 5. Función de pago
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

<style scoped>
.container { max-width: 1100px; margin: auto; padding: 40px; }
.titulo { color: #283618; margin-bottom: 30px; font-size: 2rem; }
.msg { text-align: center; padding: 50px; color: #606c38; }

.carrito-layout { display: grid; grid-template-columns: 1fr 350px; gap: 30px; }

/* LISTA DE ARTÍCULOS */
.item-carrito { 
  display: flex; gap: 20px; background: white; padding: 20px; 
  border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  align-items: center;
}
.item-img { width: 90px; height: 90px; object-fit: cover; border-radius: 8px; border: 1px solid #eee; }
.item-info { flex: 1; }
.item-info h3 { margin: 0 0 10px 0; color: #606c38; font-size: 1.1rem; }

.detalles-personalizado { background: #fefae0; padding: 10px; border-radius: 8px; font-size: 0.85rem; border: 1px solid #e9edc9; }
.badge-personalizado { font-size: 0.7rem; background: #bc6c25; color: white; padding: 2px 8px; border-radius: 10px; display: inline-block; margin-top: 5px; }

/* PRECIO (Movido a la izquierda) */
.item-precio { 
  text-align: right; 
  margin-right: 15px; /* Separación de los botones */
  min-width: 80px;
}
.precio-unitario { display: block; font-size: 0.75rem; color: #888; margin-bottom: 2px; }
.item-precio p { font-weight: bold; font-size: 1.2rem; margin: 0; color: #283618; }

/* CONTROLES CANTIDAD VERTICALES (NUEVO) */
.item-controles {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fdfaf0;
  border-radius: 8px;
  border: 1px solid #e9edc9;
  width: 40px;
  overflow: hidden;
}

.btn-cant {
  background: none;
  border: none;
  width: 100%;
  height: 30px;
  font-size: 1.2rem;
  font-weight: bold;
  color: #606c38;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-cant:hover { background: #e9edc9; }
.btn-menos { font-size: 1.5rem; line-height: 0; padding-bottom: 5px; }

.numero-cant {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
  padding: 5px 0;
}

/* PANEL DE RESUMEN */
.resumen { background: white; padding: 25px; border-radius: 12px; height: fit-content; position: sticky; top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.resumen h2 { margin-top: 0; color: #283618; border-bottom: 1px solid #eee; padding-bottom: 10px; }
.fila-resumen { display: flex; justify-content: space-between; margin-bottom: 15px; }
.total { border-top: 2px solid #fefae0; padding-top: 15px; font-weight: bold; font-size: 1.4rem; color: #bc6c25; }

.btn-pagar { 
  width: 100%; background: #606c38; color: white; border: none; padding: 15px; 
  border-radius: 8px; font-weight: bold; font-size: 1.1rem; cursor: pointer; 
  margin-top: 10px; transition: background 0.3s;
}
.btn-pagar:hover:not(:disabled) { background: #283618; }
.btn-pagar:disabled { background-color: #ccc; cursor: not-allowed; }

.carrito-vacio { text-align: center; padding: 100px 0; background: white; border-radius: 20px; }
.btn-comprar { display: inline-block; margin-top: 20px; background: #bc6c25; color: white; padding: 10px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; }
</style>