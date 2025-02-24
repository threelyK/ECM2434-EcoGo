/*
This script fetches card data from the backend and creates card elements to display on the inventory page.
*/

document.addEventListener('DOMContentLoaded', () => {
    const inventoryGrid = document.getElementById('inventory-grid');

    // Function to fetch card data from the backend
    async function fetchCardData() {
        const response = await fetch('/user/cards/');
        const cards = await response.json();
        return cards;
    }

    // Function to create a card element - replace with backend
    function createCardElement(card) {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card col-md-3';
        cardDiv.innerHTML = `
            <img src="${card.image}" alt="${card.name}">
            <h2>${card.name}</h2>
            <p>${card.description}</p>
            <p>Count: ${card.count}</p>
        `;
        return cardDiv;
    }

    // Fetch card data and add cards to the grid
    fetchCardData().then(cards => {
        cards.forEach(card => {
            const cardElement = createCardElement(card);
            inventoryGrid.appendChild(cardElement);
        });
    });
});