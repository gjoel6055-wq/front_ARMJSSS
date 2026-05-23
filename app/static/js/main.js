// Espera a que todo el árbol del documento (DOM) esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    console.log('Estructura base del Gestor Universitario lista.');

    // Ejecutar lógica del menú de navegación activo
    resaltarEnlaceActivo();
});

/**
 * Función que analiza la URL actual y agrega un estilo visual
 * al enlace del menú de navegación que coincide con la página activa.
 */
function resaltarEnlaceActivo() {
    // Obtiene la ruta actual del navegador (ej: '/alumnos' o '/docentes')
    const rutaActual = window.location.pathname;

    // Selecciona todos los enlaces que están dentro de la lista de la navbar
    const enlacesMenu = document.querySelectorAll('.navbar ul li a');

    enlacesMenu.forEach(enlace => {
        // Compara el atributo href del enlace con la ruta actual
        if (enlace.getAttribute('href') === rutaActual) {
            // Aplica estilos específicos para identificar la página activa
            enlace.style.backgroundColor = 'rgba(255, 255, 255, 0.25)';
            enlace.style.fontWeight = 'bold';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {

    // Obtenemos la ruta actual del navegador
    const rutaActual = window.location.pathname;

    // Buscamos el botón de ingresar
    const btnIngresar = document.getElementById('nav-item-ingresar');
    const tituloNav = document.getElementById('titulo-navbar');

    // 3. Lógica para el botón "Ingresar"
    if (btnIngresar) {
        if (rutaActual === '/') {
            btnIngresar.style.display = 'block'; // Mostrar en inicio
        } else {
            btnIngresar.style.display = 'none';  // Ocultar en el resto
        }
    }
    // 4. Lógica INVERSA para el Título
    if (tituloNav) {
        if (rutaActual === '/') {
            tituloNav.style.display = 'block';    // Ocultar en inicio
        } else {
            tituloNav.style.display = 'none';   // Mostrar en el resto (ej. /login)
        }
    }
});