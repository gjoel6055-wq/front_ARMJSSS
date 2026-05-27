document.addEventListener('DOMContentLoaded', () => {
    console.log('Estructura base del Gestor Universitario lista.');

    // ==========================================
    // 1. LÓGICA DE INTERFAZ (MENÚS Y NAVBAR)
    // ==========================================

    resaltarEnlaceActivo();

    const rutaActual = window.location.pathname;
    const btnslogin = document.getElementsByClassName("btn-navbar-login");
    for (let i = 0; i < btnslogin.length; i++) {
        if (rutaActual === '/') {
       btnslogin[i].style.display  = 'block'; // Mostrar en inicio
    } else {
        btnslogin[i].style.display = 'none';  // Ocultar en el resto
    }
    }

    // ==========================================
    // 2. LÓGICA DEL FORMULARIO DE LOGIN
    // ==========================================
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const mensajeError = document.getElementById('mensaje-error');

            try {
                const response = await fetch('http://localhost:5000/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    window.location.href = '/';
                } else {
                    mensajeError.textContent = data.error || 'Error al iniciar sesión';
                    mensajeError.style.display = 'block';
                }
            } catch (error) {
                mensajeError.textContent = 'Error de conexión con el servidor.';
                mensajeError.style.display = 'block';
                console.error('Error de red:', error);
            }
        });
    }

    // ==========================================
    // 3. LÓGICA DEL FORMULARIO DE REGISTRO
    // ==========================================
    const registroForm = document.getElementById('registroForm');

    if (registroForm) {
        registroForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const nombre = document.getElementById('nombre').value;
            const apellido = document.getElementById('apellido').value;
            const padron = document.getElementById('padron').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const passwordConfirm = document.getElementById('password-confirm').value;
            const mensajeRegistro = document.getElementById('mensaje-registro');

            if (password !== passwordConfirm) {
                mensajeRegistro.textContent = 'Las contraseñas no coinciden.';
                mensajeRegistro.style.color = '#dc3545';
                mensajeRegistro.style.display = 'block';
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/auth/registro', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre, apellido, padron, email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    mensajeRegistro.textContent = '¡Cuenta creada con éxito! Redirigiendo...';
                    mensajeRegistro.style.color = '#28a745';
                    mensajeRegistro.style.display = 'block';
                    setTimeout(() => { window.location.href = '/auth/login'; }, 2000);
                } else {
                    mensajeRegistro.textContent = data.error || 'Error al crear la cuenta.';
                    mensajeRegistro.style.color = '#dc3545';
                    mensajeRegistro.style.display = 'block';
                }
            } catch (error) {
                mensajeRegistro.textContent = 'Error de conexión con el servidor.';
                mensajeRegistro.style.color = '#dc3545';
                mensajeRegistro.style.display = 'block';
                console.error('Error de red:', error);
            }
        });
    }

    // ==========================================
    // 4. LÓGICA DE AUDITORÍA (LOGS DINÁMICOS)
    // ==========================================
    const tablaLogs = document.getElementById('tabla-logs-body');
    const filtroForm = document.getElementById('filtroLogsForm');

    if (tablaLogs) {
        async function cargarLogs(filtros = {}) {
            try {
                const queryParams = new URLSearchParams(filtros).toString();
                const token = localStorage.getItem('token');

                const response = await fetch(`http://localhost:5000/log?${queryParams}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) throw new Error('Error al obtener los logs');

                const logs = await response.json();
                tablaLogs.innerHTML = '';

                if (logs.length === 0) {
                    tablaLogs.innerHTML = `<tr><td colspan="5" class="td-mensaje-vacio">No se encontraron registros.</td></tr>`;
                    return;
                }

                logs.forEach(log => {
                    let claseBadge = "badge-gris";
                    if (log.accion === 'LOGIN') claseBadge = "badge-verde";
                    if (log.accion === 'QR_GEN') claseBadge = "badge-azul";
                    if (log.accion === 'LOGIN_FAIL') claseBadge = "badge-rojo";

                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${log.fecha_hora}</td>
                        <td class="td-usuario">${log.usuario}</td>
                        <td><span class="badge ${claseBadge}">${log.accion}</span></td>
                        <td class="td-detalle">${log.detalle}</td>
                        <td class="td-ip">${log.ip}</td>
                    `;
                    tablaLogs.appendChild(fila);
                });
            } catch (error) {
                tablaLogs.innerHTML = `<tr><td colspan="5" class="td-mensaje-error">Error al conectar con el servidor de auditoría.</td></tr>`;
                console.error(error);
            }
        }

        // Carga inicial
        cargarLogs();

        // Aplicar filtros
        if (filtroForm) {
            filtroForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const filtros = {
                    usuario: document.getElementById('buscar_usuario').value,
                    accion: document.getElementById('filtro_accion').value,
                    fecha: document.getElementById('fecha_log').value
                };
                cargarLogs(filtros);
            });
        }
    }
});

// ==========================================
// FUNCIONES GLOBALES (FUERA DEL DOMContentLoaded)
// ==========================================

/**
 * Función que analiza la URL actual y agrega un estilo visual
 * al enlace del menú de navegación que coincide con la página activa.
 */
function resaltarEnlaceActivo() {
    const rutaActual = window.location.pathname;
    const enlacesMenu = document.querySelectorAll('.navbar ul li a');

    enlacesMenu.forEach(enlace => {
        if (enlace.getAttribute('href') === rutaActual) {
            enlace.style.backgroundColor = 'rgba(255, 255, 255, 0.25)';
            enlace.style.fontWeight = 'bold';
        }
    });
}