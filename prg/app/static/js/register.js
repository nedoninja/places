document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('fade-in');

    const form = document.querySelector('.auth-form');
    const errorContainer = document.querySelector('.error-container');
    const notificationContainer = document.querySelector('.notification-container');

    function showError(message) {
        errorContainer.innerHTML = '';
        const error = document.createElement('div');
        error.className = 'field-error';
        error.innerHTML = `
            ${message}
            <div class="progress-bar"></div>
        `;
        errorContainer.appendChild(error);

        setTimeout(() => {
            error.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => error.remove(), 300);
        }, 3000);
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePhone(phone) {
        return /^\+?[0-9\s\-\(\)]{10,}$/.test(phone);
    }

    function validatePassword(password) {
        return password.length >= 8;
    }

    function validatePasswordMatch(password, confirmPassword) {
        return password === confirmPassword;
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = form.querySelector('[name="email"]').value.trim();
            const phone = form.querySelector('[name="phone"]').value.trim();
            const password = form.querySelector('[name="password"]').value.trim();
            const passwordConfirm = form.querySelector('[name="password_confirm"]').value.trim();

            let isValid = true;
            form.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    showError(`Пожалуйста, заполните поле "${input.placeholder}"`);
                    input.focus();
                    isValid = false;
                    return false;
                }
            });

            if (!isValid) return;

            if (!validateEmail(email)) {
                showError('Пожалуйста, введите корректный email');
                form.querySelector('[name="email"]').focus();
                return;
            }

            if (!validatePhone(phone)) {
                showError('Пожалуйста, введите корректный номер телефона (начинается с +)');
                form.querySelector('[name="phone"]').focus();
                return;
            }

            if (!validatePassword(password)) {
                showError('Пароль должен содержать минимум 8 символов');
                form.querySelector('[name="password"]').focus();
                return;
            }

            if (!validatePasswordMatch(password, passwordConfirm)) {
                showError('Пароли не совпадают');
                form.querySelector('[name="password_confirm"]').focus();
                return;
            }

            form.submit();
        });
    }
});

