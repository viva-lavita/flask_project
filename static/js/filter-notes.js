const filterInput = document.getElementById('filterInput');
const cards = document.querySelectorAll('.card');

filterInput.addEventListener('input', function () {
  const filterValue = this.value.toLowerCase();

  cards.forEach(function (card) {
    const title = card.querySelector('.card-title').innerText.toLowerCase();
    const intro = card.querySelector('.card-text').innerText.toLowerCase();
    const author = card.querySelector('.card-author').innerText.toLowerCase();

    if (title.includes(filterValue) || intro.includes(filterValue) || author.includes(filterValue)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
});