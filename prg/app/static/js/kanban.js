let cardIdCounter = 0;

function addCard(columnId) {
    const column = document.getElementById(columnId);
    const card = document.createElement('div');
    card.classList.add('card');
    card.draggable = true;
    card.id = 'card-' + cardIdCounter++;

    // Color picker
    const colorPicker = document.createElement('input');
    colorPicker.type = 'color';
    colorPicker.value = '#f9f9f9'; // Default card color
    colorPicker.style.marginRight = '5px';
    colorPicker.addEventListener('change', function(event) {
        card.style.backgroundColor = event.target.value;
    });
    card.appendChild(colorPicker);

    // Card title input
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.placeholder = 'Title';
    titleInput.style.width = '100%';
    titleInput.style.marginBottom = '5px';
    card.appendChild(titleInput);

    // Card description input
    const descriptionInput = document.createElement('textarea');
    descriptionInput.placeholder = 'Description';
    descriptionInput.style.width = '100%';
    descriptionInput.style.height = '50px';
    card.appendChild(descriptionInput);

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button');
    deleteButton.textContent = 'Delete';
    deleteButton.onclick = function() {
        card.remove();
    };
    card.appendChild(deleteButton);

    card.addEventListener('dragstart', dragStart);
    column.appendChild(card);
}

function allowDrop(event) {
    event.preventDefault();
}

function dragStart(event) {
    event.dataTransfer.setData('text/plain', event.target.id);
}

function drop(event) {
    event.preventDefault();
    const cardId = event.dataTransfer.getData('text/plain');
    const card = document.getElementById(cardId);
    const column = event.target;

    if (column.classList.contains('column')) {
        column.appendChild(card);
    }
}

document.getElementById('theme-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
});
