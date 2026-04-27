import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'


// Configuración del Interceptor de Axios
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // Inyectamos el token en la cabecera automáticamente
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Manejo de errores globales (ej: token caducado)
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Si el servidor dice que el token no vale, limpiamos y fuera
      localStorage.clear();
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

const app = createApp(App)
app.use(router)
app.mount('#app')