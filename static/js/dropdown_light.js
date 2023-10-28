const dropdownItems = document.querySelectorAll('.dropdown-item');

dropdownItems.forEach(item => {
  item.addEventListener('click', () => {
    const themeValue = item.getAttribute('data-bs-theme-value');
    document.body.setAttribute('data-bs-theme', themeValue);
  });
});