document.addEventListener('DOMContentLoaded', function() {
    const notificationButton = document.getElementById('notification-button');
    const notificationPanel = document.getElementById('notification-panel');

    // Función para mostrar u ocultar el panel de notificaciones
    function toggleNotificationsPanel() {
        if (notificationPanel.style.display === 'block') {
            notificationPanel.style.display = 'none'; // Si el panel está visible, ocúltalo
        } else {
            notificationPanel.style.display = 'block'; // Si el panel está oculto, muéstralo
        }
    }

    // Función para crear una nueva notificación
    function createNotification() {
        const notificationMessage = "Recuerda actualizar tu cocina, así podrás crear deliciosas recetas!";
        
        // Crear un nuevo elemento div para la notificación
        const div = document.createElement('div');
        div.className = 'notification-item unread';
        div.textContent = notificationMessage;
        div.onclick = function() {
            // Cuando se hace clic en la notificación, redirigir a kitchen:list
            const kitchenListUrl = notificationButton.dataset.url;
            window.location.href = kitchenListUrl;
            // Ocultar el panel de notificaciones
            notificationPanel.style.display = 'none';
        };
        
        // Agregar la notificación al panel
        notificationPanel.appendChild(div);
    }

    // Función para programar las notificaciones
    function scheduleNotifications() {
        setInterval(createNotification, 5000); // 5000 milisegundos = 5 segundos
    }

    // Llamar a la función para programar las notificaciones
    scheduleNotifications();

    // Agregar evento de clic al botón de notificaciones
    notificationButton.addEventListener('click', function() {
        toggleNotificationsPanel();
    });
});
