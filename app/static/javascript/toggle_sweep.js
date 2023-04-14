document.addEventListener('DOMContentLoaded', function() {
  const toggleButtons = document.querySelectorAll('[id$="_button"]');
  const toggleForm = document.querySelectorAll('[id$="_form"]');
  const toggleSplit = document.querySelectorAll('[id$="_split"]');

  toggleButtons.forEach((button, index) => {
    const split = toggleSplit[index];
    const form = toggleForm[index];

    button.addEventListener('click', () => {
      if (split.style.display === 'none') {
        split.style.display = 'block';
        form.style.display = 'none';
      } else {
        split.style.display = 'none';
        form.style.display = 'block';
      }
    });
  });
});
