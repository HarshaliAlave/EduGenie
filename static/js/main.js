// EduGenie – Main JS (no JSON, no Node.js, no fetch API)

// ── Auto-hide flash messages ────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    }, 10000);
  });

  // ── Loading spinners on ALL forms ──────────────────────────
  const forms = document.querySelectorAll('form');
  forms.forEach(function (form) {
    form.addEventListener('submit', function () {
      const btns = form.querySelectorAll('button[type="submit"]');
      btns.forEach(function (btn) {
        // Don't override quiz form submit handler
        if (!form.id || form.id !== 'quizForm') {
          btn.disabled = true;
          if (!btn.dataset.noLoading) {
            const originalText = btn.textContent;
            btn.textContent = '⏳ Processing...';
            btn.dataset.originalText = originalText;
          }
        }
      });
    });
  });
});
