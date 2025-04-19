document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('fade-in');

    const form = document.querySelector('.auth-form');
    const notificationContainer = document.querySelector('.notification-container');

    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            ${message}
            <div class="progress-bar"></div>
        `;

        notificationContainer.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            const username = form.querySelector('[name="username"]').value.trim();
            const password = form.querySelector('[name="password"]').value.trim();

            if (!username || !password) {
                e.preventDefault();
                showNotification('Пожалуйста, заполните все поля', 'error');
            }
        });
    }
});