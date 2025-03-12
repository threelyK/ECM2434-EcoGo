
function glowCards() {
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('glow');
    });
}

function shakeCards() {
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('shake');
        setTimeout(() => card.classList.remove('shake'), 500);
    });
}

function openPack() {
    shakeCards();
    setTimeout(glowCards, 500);
}

openPack();