(() => {
  const consentKey = 'pulsewatch_analytics_consent_v1';
  const measurementId = window.PULSEWATCH_GA4_ID;
  const banner = document.querySelector('.consent-banner');
  const acceptButton = document.querySelector('.js-consent-accept');
  const rejectButton = document.querySelector('.js-consent-reject');
  const settingsButtons = document.querySelectorAll('.js-cookie-settings');
  let analyticsLoaded = false;

  const readConsent = () => {
    try {
      return window.localStorage.getItem(consentKey);
    } catch (_error) {
      return null;
    }
  };

  const writeConsent = (value) => {
    try {
      window.localStorage.setItem(consentKey, value);
    } catch (_error) {
      // The choice applies to this page even when storage is unavailable.
    }
  };

  const updateConsent = (analyticsStorage) => {
    if (typeof window.gtag !== 'function') return;
    window.gtag('consent', 'update', {
      analytics_storage: analyticsStorage,
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  };

  const loadAnalytics = () => {
    if (analyticsLoaded || !measurementId || readConsent() !== 'granted') return;
    analyticsLoaded = true;
    updateConsent('granted');
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      send_page_view: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
    script.dataset.pulsewatchAnalytics = 'true';
    document.head.appendChild(script);
  };

  const showBanner = (focusChoice = false) => {
    if (!banner) return;
    banner.hidden = false;
    if (focusChoice) rejectButton?.focus({preventScroll: true});
  };

  const hideBanner = () => {
    if (banner) banner.hidden = true;
  };

  acceptButton?.addEventListener('click', () => {
    writeConsent('granted');
    loadAnalytics();
    hideBanner();
  });

  rejectButton?.addEventListener('click', () => {
    const hadAnalytics = analyticsLoaded || readConsent() === 'granted';
    writeConsent('denied');
    updateConsent('denied');
    hideBanner();
    if (hadAnalytics) window.location.reload();
  });

  settingsButtons.forEach((button) => button.addEventListener('click', () => showBanner(true)));

  const storedConsent = readConsent();
  if (storedConsent === 'granted') {
    loadAnalytics();
  } else if (storedConsent !== 'denied') {
    showBanner();
  }

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
        if (readConsent() === 'granted' && typeof window.gtag === 'function') {
          window.gtag('event', 'generate_lead', {method: 'pilot_enquiry'});
        }
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
