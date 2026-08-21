(() => {
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.nav-links');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  }

  document.querySelectorAll('.js-lead-form').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const emailInput = form.querySelector('input[name="email"]');
      const button = form.querySelector('button[type="submit"]');
      const message = form.querySelector('.form-message');
      if (!emailInput || !button || !message || !emailInput.value.trim()) return;
      button.disabled = true;
      button.textContent = 'Sending…';
      message.textContent = '';
      try {
        const response = await fetch('/subscribe.php', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({email: emailInput.value.trim()})
        });
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.message || 'Unable to submit the enquiry.');
        message.style.color = '#138a64';
        message.textContent = "Thanks. We'll review fit and send the pilot qualification steps.";
        emailInput.value = '';
      } catch (error) {
        message.style.color = '#b93838';
        message.textContent = error.message || 'Unable to submit. Please try again later.';
      } finally {
        button.disabled = false;
        button.textContent = 'Request pilot assessment';
      }
    });
  });
})();
