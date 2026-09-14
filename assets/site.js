'use strict';
// Progressive enhancement only: content and navigation work without JavaScript.
(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  try {
    const saved = localStorage.getItem('ma-theme');
    if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;
  } catch (_) { /* Storage can be unavailable in privacy modes. */ }
  function syncThemeButton() {
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : systemTheme.matches;
    if (toggle) {
      toggle.textContent = dark ? 'Light' : 'Dark';
      toggle.setAttribute('aria-pressed', String(dark));
    }
  }
  if (toggle) {
    toggle.hidden = false;
    syncThemeButton();
    toggle.addEventListener('click', () => {
      const dark = toggle.getAttribute('aria-pressed') === 'true';
      root.dataset.theme = dark ? 'light' : 'dark';
      try { localStorage.setItem('ma-theme', root.dataset.theme); } catch (_) {}
      syncThemeButton();
    });
    systemTheme.addEventListener('change', syncThemeButton);
  }
  document.querySelectorAll('[data-copy]').forEach(button => {
    if (!navigator.clipboard || !window.isSecureContext) return;
    button.hidden = false;
    button.addEventListener('click', async () => {
      const text = document.getElementById(button.dataset.copy);
      const status = button.parentElement.querySelector('[role="status"]');
      if (!text || !status) return;
      try {
        await navigator.clipboard.writeText(text.textContent.trim());
        status.textContent = 'Citation copied.';
      } catch (_) {
        status.textContent = 'Copy unavailable. Select the citation text above.';
      }
    });
  });
  document.querySelectorAll('[data-print]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => window.print());
  });
})();
