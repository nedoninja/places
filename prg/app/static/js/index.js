document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const servicesContainer = document.querySelector('.services-container');
    let services = Array.from(document.querySelectorAll('.service')); // Initial list of services
    let noResultsMessage = null;

    function displayNoResultsMessage() {
        if (!noResultsMessage) {
            noResultsMessage = document.createElement('p');
            noResultsMessage.textContent = 'Нет результатов.';
            noResultsMessage.classList.add('no-results-message'); // Add a class for styling
            servicesContainer.appendChild(noResultsMessage);
        }
    }

    function clearNoResultsMessage() {
        if (noResultsMessage) {
            noResultsMessage.remove();
            noResultsMessage = null;
        }
    }

    window.searchServices = function() {
        const searchTerm = searchInput.value.toLowerCase();
        let resultsFound = false;

        clearNoResultsMessage(); // Clear any previous "no results" message

        services.forEach(service => {
            const title = service.querySelector('h3').textContent.toLowerCase();
            const description = service.querySelector('p').textContent.toLowerCase();
            const price = service.querySelector('p').textContent.toLowerCase();

            if (title.includes(searchTerm) || description.includes(searchTerm) || price.includes(searchTerm)) {
                service.style.display = 'block';
                resultsFound = true;
            } else {
                service.style.display = 'none';
            }
        });

        if (!resultsFound) {
            displayNoResultsMessage();
        }
    };

    // Optional: Add event listener for Enter key press
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            searchServices();
        }
    });
});
