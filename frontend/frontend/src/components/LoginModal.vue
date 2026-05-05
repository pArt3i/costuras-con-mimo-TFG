<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

// Recibimos la prop 'mostrar' para saber si abrir el modal
const props = defineProps(['mostrar'])
const emit = defineEmits(['cerrar', 'loginExitoso'])

const esLogin = ref(true) 
const mensaje = ref({ texto: '', tipo: '' })
const cargando = ref(false)

const formulario = ref({
  username: '',
  email: '',
  password: '',
  direccion: '' 
})

// --- VALIDACIONES DE FRONTEND ---
const passwordValida = computed(() => formulario.value.password.length >= 8)
const emailValido = computed(() => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(formulario.value.email)
})

const procesarFormulario = async () => {
  mensaje.value = { texto: '', tipo: '' }
  
  if (!passwordValida.value) {
    mensaje.value = { texto: 'La contraseña debe tener al menos 8 caracteres', tipo: 'error' }
    return
  }

  cargando.value = true
  try {
    if (esLogin.value) {
      // --- 1. LÓGICA DE INICIO DE SESIÓN ---
      const res = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: formulario.value.username,
        password: formulario.value.password
      })
      
      const tokenAcceso = res.data.access
      localStorage.setItem('token', tokenAcceso)
      localStorage.setItem('username', formulario.value.username) 

      // --- 2. COMPROBACIÓN DE ADMINISTRADOR ---
      try {
        const userRes = await axios.get('http://127.0.0.1:8000/api/usuarios/', {
          headers: { Authorization: `Bearer ${tokenAcceso}` }
        })
        
        const listaUsuarios = Array.isArray(userRes.data) ? userRes.data : (userRes.data.results || [])
        const miUsuario = listaUsuarios.find(u => u.username === formulario.value.username)
        
        if (miUsuario && miUsuario.is_superuser) {
          localStorage.setItem('isAdmin', 'true')
        } else {
          localStorage.removeItem('isAdmin')
        }
      } catch (adminError) {
        console.error("No se pudo verificar si es administrador", adminError)
        localStorage.removeItem('isAdmin')
      }
      
      mensaje.value = { texto: '¡Acceso concedido! Entrando...', tipo: 'exito' }
      
      // --- 3. REDIRECCIÓN DIRECTA ---
      setTimeout(() => {
        emit('loginExitoso')
        emit('cerrar')
        
        if (localStorage.getItem('isAdmin') === 'true') {
          // Si es admin, obligamos al navegador a viajar al panel de control
          window.location.href = '/admin'
        } else {
          // Si es un usuario normal, recargamos la página donde estaba
          window.location.reload()
        }
      }, 1200)

    } else {
      // --- LÓGICA DE REGISTRO ---
      await axios.post('http://127.0.0.1:8000/api/usuarios/', formulario.value)
      
      mensaje.value = { texto: 'Cuenta creada. Ahora puedes iniciar sesión.', tipo: 'exito' }
      setTimeout(() => {
        esLogin.value = true
        mensaje.value = { texto: '', tipo: '' }
      }, 2000)
    }
  } catch (error) {
    if (error.response && error.response.data) {
      const data = error.response.data
      if (data.email) {
        mensaje.value = { texto: 'Este correo electrónico ya está registrado', tipo: 'error' }
      } else if (data.username) {
        mensaje.value = { texto: 'Este nombre de usuario ya existe', tipo: 'error' }
      } else {
        mensaje.value = { texto: 'Error: Revisa los datos introducidos', tipo: 'error' }
      }
    } else {
      mensaje.value = { texto: 'No se pudo conectar con el servidor', tipo: 'error' }
    }
  } finally {
    cargando.value = false
  }
}

// Limpiar formulario al cerrar
const cerrarYLimpiar = () => {
  mensaje.value = { texto: '', tipo: '' }
  formulario.value = { username: '', email: '', password: '', direccion: '' }
  emit('cerrar')
}
</script>
<template>
  <div v-if="mostrar" class="modal-overlay" @click.self="cerrarYLimpiar">
    <div class="modal-content">
      <button class="close-btn" @click="cerrarYLimpiar">×</button>
      
      <h2 class="titulo-modal">{{ esLogin ? '🧵 Iniciar Sesión' : '📝 Crear Cuenta' }}</h2>
      
      <div v-if="mensaje.texto" :class="['alerta', mensaje.tipo]">
        {{ mensaje.texto }}
      </div>

      <form @submit.prevent="procesarFormulario" class="form-estilo">
        <div class="campo">
          <label>Nombre de Usuario:</label>
          <input type="text" v-model="formulario.username" required placeholder="Tu usuario">
        </div>

        <div v-if="!esLogin" class="campo">
          <label>Correo Electrónico:</label>
          <input type="email" v-model="formulario.email" required placeholder="ejemplo@correo.com">
          <span v-if="formulario.email && !emailValido" class="error-msg">Email no válido</span>
        </div>

        <!-- NUEVO CAMPO DIRECCIÓN -->
        <div v-if="!esLogin" class="campo">
          <label>Dirección de envío:</label>
          <input type="text" v-model="formulario.direccion" required placeholder="Calle, número, código postal...">
        </div>

        <div class="campo">
          <label>Contraseña:</label>
          <input type="password" v-model="formulario.password" required placeholder="Mínimo 8 caracteres">
          <span v-if="formulario.password && !passwordValida" class="error-msg">Mínimo 8 caracteres</span>
        </div>

        <button type="submit" class="btn-submit" :disabled="cargando">
          {{ cargando ? 'Cargando...' : (esLogin ? 'Entrar' : 'Registrarme') }}
        </button>
      </form>

      <div class="footer-modal">
        <p>{{ esLogin ? '¿Aún no tienes cuenta?' : '¿Ya eres de la familia?' }}</p>
        <button @click="esLogin = !esLogin" class="btn-toggle">
          {{ esLogin ? 'Regístrate aquí' : 'Inicia sesión ahora' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos para el efecto emergente */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background: #fdfaf0;
  padding: 2rem;
  border-radius: 15px;
  width: 90%;
  max-width: 400px;
  position: relative;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #606c38;
}

.titulo-modal {
  text-align: center;
  color: #283618;
  margin-bottom: 1.5rem;
}

.form-estilo {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.campo label {
  font-weight: bold;
  color: #606c38;
  font-size: 0.9rem;
}

.campo input {
  padding: 10px;
  border: 1px solid #ccd5ae;
  border-radius: 8px;
}

.error-msg {
  color: #bc6c25;
  font-size: 0.75rem;
  font-weight: bold;
}

.btn-submit {
  background: #606c38;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

.btn-submit:disabled {
  background: #a3ad8d;
}

.alerta {
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.exito { background: #e9edc9; color: #606c38; border: 1px solid #606c38; }
.error { background: #f8d7da; color: #721c24; border: 1px solid #721c24; }

.footer-modal {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.85rem;
  border-top: 1px solid #ccd5ae;
  padding-top: 1rem;
}

.btn-toggle {
  background: none;
  border: none;
  color: #bc6c25;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
}
</style>