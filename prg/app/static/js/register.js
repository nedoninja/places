document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('fade-in');

    function initDatePicker() {
        const dateInput = document.querySelector('[name="birth_date"]');
        const calendarIcon = document.querySelector('.calendar-icon');
        const datepicker = document.querySelector('.custom-datepicker');
        const currentMonthYear = document.querySelector('.current-month-year');
        const daysGrid = document.querySelector('.days-grid');
        const prevMonthBtn = document.querySelector('.prev-month');
        const nextMonthBtn = document.querySelector('.next-month');
        const prevYearBtn = document.querySelector('.prev-year');
        const nextYearBtn = document.querySelector('.next-year');
        const todayBtn = document.querySelector('.today-btn');
        const clearBtn = document.querySelector('.clear-btn');
        const yearsContainer = document.querySelector('.datepicker-years');

        let currentDate = new Date();
        let selectedDate = null;
        const minYear = 1950;
        const maxYear = 2024;

        function formatDate(date) {
            if (!date) return '';
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            return `${day}.${month}.${year}`;
        }

        function parseDate(dateStr, showErrors = true) {
            if (!dateStr) return null;
            const parts = dateStr.split('.');
            if (parts.length !== 3) {
                if (showErrors) showError('Введите дату в формате дд.мм.гггг');
                return null;
            }

            const day = parseInt(parts[0], 10);
            const month = parseInt(parts[1], 10) - 1;
            const year = parseInt(parts[2], 10);

            if (year < minYear || year > maxYear) {
                if (showErrors) showError(`Год должен быть между ${minYear} и ${maxYear}`);
                return null;
            }

            const date = new Date(year, month, day);
            if (isNaN(date.getTime())) {
                if (showErrors) showError('Введите корректную дату');
                return null;
            }
            return date;
        }

        function updateCalendar(suppressErrors = false) {
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();

            const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
            currentMonthYear.textContent = `${monthNames[month]} ${year}`;

            daysGrid.innerHTML = '';

            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const firstDayOfWeek = (firstDay.getDay() + 6) % 7;

            for (let i = 0; i < firstDayOfWeek; i++) {
                const emptyDay = document.createElement('div');
                emptyDay.classList.add('day', 'other-month');
                daysGrid.appendChild(emptyDay);
            }

            for (let day = 1; day <= lastDay.getDate(); day++) {
                const date = new Date(year, month, day);
                const dayElement = document.createElement('div');
                dayElement.classList.add('day');
                dayElement.textContent = day;

                if (selectedDate &&
                    selectedDate.getDate() === day &&
                    selectedDate.getMonth() === month &&
                    selectedDate.getFullYear() === year) {
                    dayElement.classList.add('selected');
                }

                if (year < minYear || year > maxYear) {
                    dayElement.classList.add('disabled');
                } else {
                    dayElement.addEventListener('click', () => {
                        selectedDate = date;
                        dateInput.value = formatDate(selectedDate);
                        updateCalendar(true);
                        datepicker.classList.remove('active');
                    });
                }

                daysGrid.appendChild(dayElement);
            }

            const totalCells = firstDayOfWeek + lastDay.getDate();
            const remainingCells = 7 - (totalCells % 7);
            if (remainingCells < 7) {
                for (let i = 1; i <= remainingCells; i++) {
                    const emptyDay = document.createElement('div');
                    emptyDay.classList.add('day', 'other-month');
                    daysGrid.appendChild(emptyDay);
                }
            }
        }

        function updateYears() {
            yearsContainer.innerHTML = '';
            for (let year = maxYear; year >= minYear; year--) {
                const yearElement = document.createElement('div');
                yearElement.textContent = year;

                if (currentDate.getFullYear() === year) {
                    yearElement.classList.add('selected');
                }

                yearElement.addEventListener('click', () => {
                    currentDate.setFullYear(year);
                    yearsContainer.classList.remove('active');
                    updateCalendar(true);
                });

                yearsContainer.appendChild(yearElement);
            }
        }

        function ensureDatepickerVisible() {
            const rect = datepicker.getBoundingClientRect();
            const viewportHeight = window.innerHeight;

            if (rect.bottom > viewportHeight) {
                datepicker.style.bottom = 'auto';
                datepicker.style.top = 'calc(100% + 5px)';
            } else {
                datepicker.style.bottom = 'calc(100% + 5px)';
                datepicker.style.top = 'auto';
            }
        }

        function init() {
            if (dateInput.value) {
                selectedDate = parseDate(dateInput.value, false);
                if (selectedDate) {
                    currentDate = new Date(selectedDate);
                }
            }

            updateCalendar();
            updateYears();

            calendarIcon.addEventListener('click', (e) => {
                e.stopPropagation();
                datepicker.classList.toggle('active');
                yearsContainer.classList.remove('active');

                if (datepicker.classList.contains('active')) {
                    ensureDatepickerVisible();
                }
            });

            prevMonthBtn.addEventListener('click', () => {
                currentDate.setMonth(currentDate.getMonth() - 1);
                updateCalendar(true);
            });

            nextMonthBtn.addEventListener('click', () => {
                currentDate.setMonth(currentDate.getMonth() + 1);
                updateCalendar(true);
            });

            prevYearBtn.addEventListener('click', () => {
                const newYear = currentDate.getFullYear() - 1;
                if (newYear >= minYear) {
                    currentDate.setFullYear(newYear);
                    updateCalendar(true);
                }
            });

            nextYearBtn.addEventListener('click', () => {
                const newYear = currentDate.getFullYear() + 1;
                if (newYear <= maxYear) {
                    currentDate.setFullYear(newYear);
                    updateCalendar(true);
                }
            });

            currentMonthYear.addEventListener('click', () => {
                yearsContainer.classList.toggle('active');
                if (yearsContainer.classList.contains('active')) {
                    ensureDatepickerVisible();
                }
            });

            todayBtn.addEventListener('click', () => {
                const today = new Date();
                if (today.getFullYear() > maxYear) {
                    currentDate = new Date(maxYear, today.getMonth(), today.getDate());
                } else if (today.getFullYear() < minYear) {
                    currentDate = new Date(minYear, today.getMonth(), today.getDate());
                } else {
                    currentDate = new Date();
                }
                selectedDate = new Date(currentDate);
                dateInput.value = formatDate(selectedDate);
                updateCalendar(true);
                datepicker.classList.remove('active');
            });

            clearBtn.addEventListener('click', () => {
                selectedDate = null;
                dateInput.value = '';
                datepicker.classList.remove('active');
            });

            document.addEventListener('click', (e) => {
                if (!datepicker.contains(e.target) && e.target !== calendarIcon && !calendarIcon.contains(e.target)) {
                    datepicker.classList.remove('active');
                    yearsContainer.classList.remove('active');
                }
            });

            dateInput.addEventListener('change', () => {
                if (dateInput.value) {
                    const date = parseDate(dateInput.value, true);
                    if (date) {
                        selectedDate = date;
                        currentDate = new Date(date);
                        updateCalendar(true);
                    } else {
                        dateInput.value = '';
                    }
                }
            });
        }

        init();
    }

    initDatePicker();

    const form = document.querySelector('.auth-form');
    const errorContainer = document.querySelector('.error-container');

    function showError(message) {
        while (errorContainer.firstChild) {
            errorContainer.removeChild(errorContainer.firstChild);
        }

        const error = document.createElement('div');
        error.className = 'field-error';
        error.innerHTML = `
            <div class="error-message">${message}</div>
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

    function getFieldName(input) {
        const nameMap = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'username': 'Логин',
            'email': 'Email',
            'password': 'Пароль',
            'password_confirm': 'Подтверждение пароля',
            'phone': 'Номер телефона',
            'city': 'Город',
            'birth_date': 'Дата рождения',
            'role': 'Роль'
        };

        return nameMap[input.name] || input.placeholder || input.name;
    }

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = {
                email: form.querySelector('[name="email"]').value.trim(),
                phone: form.querySelector('[name="phone"]').value.trim(),
                password: form.querySelector('[name="password"]').value.trim(),
                passwordConfirm: form.querySelector('[name="password_confirm"]').value.trim(),
                birthDate: form.querySelector('[name="birth_date"]').value.trim()
            };

            let isValid = true;
            form.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    showError(`Пожалуйста, заполните поле "${getFieldName(input)}"`);
                    input.focus();
                    isValid = false;
                    return;
                }
            });

            if (!isValid) return;

            if (!validateEmail(formData.email)) {
                showError('Пожалуйста, введите корректный email (например, user@example.com)');
                form.querySelector('[name="email"]').focus();
                return;
            }

            if (!validatePhone(formData.phone)) {
                showError('Пожалуйста, введите корректный номер телефона (начинается с +, например +79123456789)');
                form.querySelector('[name="phone"]').focus();
                return;
            }

            if (!validatePassword(formData.password)) {
                showError('Пароль должен содержать минимум 8 символов');
                form.querySelector('[name="password"]').focus();
                return;
            }

            if (!validatePasswordMatch(formData.password, formData.passwordConfirm)) {
                showError('Пароли не совпадают');
                form.querySelector('[name="password_confirm"]').focus();
                return;
            }

            if (formData.birthDate) {
                const date = parseDate(formData.birthDate, true);
                if (!date || date.getFullYear() < 1950 || date.getFullYear() > 2024) {
                    showError(`Год рождения должен быть между 1950 и 2024`);
                    form.querySelector('[name="birth_date"]').focus();
                    return;
                }
            }

            form.submit();
        });
    }

    window.parseDate = function(dateStr, showErrors = true) {
        if (!dateStr) return null;
        const parts = dateStr.split('.');
        if (parts.length !== 3) {
            if (showErrors) showError('Введите дату в формате дд.мм.гггг');
            return null;
        }

        const day = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10) - 1;
        const year = parseInt(parts[2], 10);

        const date = new Date(year, month, day);
        if (isNaN(date.getTime())) {
            if (showErrors) showError('Введите корректную дату');
            return null;
        }
        return date;
    };
});