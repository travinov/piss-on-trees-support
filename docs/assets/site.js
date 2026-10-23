'use strict';
document.querySelectorAll('[data-copy-email]').forEach(button => {
  button.addEventListener('click', async () => {
    const status = document.getElementById(button.getAttribute('aria-describedby'));
    try {
      await navigator.clipboard.writeText(button.dataset.copyEmail);
      status.textContent = button.dataset.success;
    } catch {
      status.textContent = button.dataset.fallback;
    }
  });
});
