document.addEventListener('DOMContentLoaded', () => {

  const header = document.querySelector('.header');
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('.nav');

  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      const expanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', !expanded);
      nav.classList.toggle('is-open');
      hamburger.setAttribute('aria-label', expanded ? 'Abrir menú de navegación' : 'Cerrar menú de navegación');
    });

    document.addEventListener('click', (e) => {
      if (!header.contains(e.target) && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.setAttribute('aria-label', 'Abrir menú de navegación');
      }
    });

    document.querySelectorAll('.nav__link').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 767) {
          nav.classList.remove('is-open');
          hamburger.setAttribute('aria-expanded', 'false');
          hamburger.setAttribute('aria-label', 'Abrir menú de navegación');
        }
      });
    });
  }

  let ticking = false;
  const handleScroll = () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        if (header) {
          header.classList.toggle('is-scrolled', window.scrollY > 60);
        }
        ticking = false;
      });
      ticking = true;
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  const faqQuestions = document.querySelectorAll('.faq-question');
  faqQuestions.forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('is-open');
      item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', !isOpen);
    });
  });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});

/* ==========================================
   BRAND OVERHAUL v3 — Interactions
   ========================================== */

// Video grid click-to-play
document.querySelectorAll('.video-grid__item').forEach(function(item) {
  item.addEventListener('click', function() {
    var video = this.querySelector('.video-grid__video');
    if (this.classList.contains('video-grid__item--playing')) {
      video.pause();
      video.currentTime = 0;
      this.classList.remove('video-grid__item--playing');
    } else {
      document.querySelectorAll('.video-grid__item--playing').forEach(function(p) {
        p.querySelector('.video-grid__video').pause();
        p.querySelector('.video-grid__video').currentTime = 0;
        p.classList.remove('video-grid__item--playing');
      });
      video.play();
      this.classList.add('video-grid__item--playing');
    }
  });
});

// Comparison slider drag-to-compare
document.querySelectorAll('.comparison-slider').forEach(function(slider) {
  var beforeImg = slider.querySelector('.comparison-slider__img--before');
  var afterImg = slider.querySelector('.comparison-slider__img--after');
  var handle = slider.querySelector('.comparison-slider__handle');

  function setPosition(x) {
    var rect = slider.getBoundingClientRect();
    var pos = Math.max(0, Math.min(1, (x - rect.left) / rect.width));
    var pct = pos * 100;
    afterImg.style.clipPath = 'inset(0 ' + (100 - pct) + '% 0 0)';
    beforeImg.style.clipPath = 'inset(0 0 0 ' + pct + '%)';
    if (handle) {
      handle.style.left = pct + '%';
    }
  }

  function onMove(e) {
    var clientX = e.touches ? e.touches[0].clientX : e.clientX;
    setPosition(clientX);
  }

  slider.addEventListener('mousedown', function(e) {
    onMove(e);
    function onMouseMove(ev) { onMove(ev); }
    function onMouseUp() {
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    }
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  });

  slider.addEventListener('touchstart', function(e) {
    onMove(e);
    function onTouchMove(ev) { onMove(ev); }
    function onTouchEnd() {
      slider.removeEventListener('touchmove', onTouchMove);
      slider.removeEventListener('touchend', onTouchEnd);
    }
    slider.addEventListener('touchmove', onTouchMove);
    slider.addEventListener('touchend', onTouchEnd);
  });
});

// Urgency timer countdown (48h from page load)
document.querySelectorAll('.urgency-timer').forEach(function(timer) {
  var hoursSpan = timer.querySelector('.urgency-timer__hours');
  var minsSpan = timer.querySelector('.urgency-timer__mins');
  var secsSpan = timer.querySelector('.urgency-timer__secs');
  if (!hoursSpan || !minsSpan || !secsSpan) return;

  var end = new Date();
  end.setHours(end.getHours() + 48);

  function update() {
    var diff = end - new Date();
    if (diff <= 0) { timer.textContent = 'Oferta finalizada'; return; }
    var h = Math.floor(diff / 3600000);
    var m = Math.floor((diff % 3600000) / 60000);
    var s = Math.floor((diff % 60000) / 1000);
    hoursSpan.textContent = String(h).padStart(2, '0');
    minsSpan.textContent = String(m).padStart(2, '0');
    secsSpan.textContent = String(s).padStart(2, '0');
  }
  update();
  setInterval(update, 1000);
});
