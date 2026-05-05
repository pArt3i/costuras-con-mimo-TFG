# 🧵 Costuras con Mimo - Taller Artesanal & E-Commerce

Proyecto de Trabajo de Fin de Grado (TFG). Aplicación web Full-Stack para la gestión y venta de productos textiles artesanales y encargos personalizados.

## 🚀 Tecnologías Utilizadas

El proyecto está dividido en dos partes principales, utilizando una arquitectura moderna separada (Frontend/Backend):

**Frontend:**
* Vue.js 3 (Composition API)
* Vite
* Vue Router (Gestor de rutas y protección)
* Axios (Cliente HTTP)

**Backend:**
* Python & Django
* Django REST Framework (API)
* PostgreSQL (Base de datos relacional)
* SimpleJWT (Autenticación basada en tokens JWT)

**Servicios Externos / Integraciones:**
* **Stripe:** Pasarela de pago simulada para procesamiento de compras.
* **Mailtrap:** Servicio SMTP para el envío automatizado de correos transaccionales (cambios de estado de pedidos).

---

## 🛠️ Características Principales

### Para el Cliente
* **Catálogo de Productos:** Visualización de productos en stock.
* **Pedidos Personalizados:** Formulario especial para seleccionar telas y pedir bordados a medida.
* **Carrito de Compras:** Gestión dinámica de cantidades con cálculo de totales.
* **Pasarela de Pago:** Integración segura con Stripe para procesar los pedidos.
* **Área Privada (Perfil):** Historial de compras detallado con estados del pedido en tiempo real.

### Para el Administrador (Backoffice)
* **Dashboard Privado:** Acceso restringido por roles (RBAC).
* **Gestión de Catálogo:** Modificación de precios y stock en tiempo real.
* **Gestión de Pedidos:** Actualización del estado de los pedidos (Pendiente, Pagado, En Preparación, Enviado...).
* **Notificaciones Automáticas:** Envío de correos automáticos al cliente cuando su pedido cambia de estado.
* **Estadísticas Básicas:** Resumen de facturación y volumen de pedidos.

---

## ⚙️ Instalación y Despliegue Local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/costuras-con-mimo-tfg.git](https://github.com/TU_USUARIO/costuras-con-mimo-tfg.git)
cd costuras-con-mimo-tfg
