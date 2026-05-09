<script setup>
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="footer-container">
    <div class="footer-content">
      
      <!-- SECCIÓN IZQUIERDA: Descripción -->
      <div class="footer-info">
        <h3 class="footer-brand">🧶 Costuras con Mimo</h3>
        <p class="footer-desc">
          Taller artesanal de costura creativa. Creamos accesorios textiles y personalizados 
          con mucho amor, cuidando cada detalle para ti.
        </p>
      </div>

      <!-- SECCIÓN DERECHA: Redes Sociales -->
      <div class="footer-social">
        <h4>¡Síguenos en redes!</h4>
        <div class="social-icons">
          <a href="https://www.instagram.com/costurasconmimo/" target="_blank" rel="noopener noreferrer" class="social-link" title="Visítanos en Instagram">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-instagram">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
              <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
              <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
            <span class="social-text">@costurasconmimo</span>
          </a>
        </div>
      </div>
      
    </div>

    <!-- SECCIÓN INFERIOR: Copyright -->
    <div class="footer-bottom">
      <p>&copy; {{ currentYear }} Costuras con Mimo. Todos los derechos reservados.</p>
    </div>
  </footer>
</template>
