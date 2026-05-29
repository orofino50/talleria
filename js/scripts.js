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
