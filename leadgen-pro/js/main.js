/* LeadGen Pro — main.js
   Vanilla JS for nav, scroll reveal, drawer, FAQ, smooth scroll.
   No dependencies. */
(function () {
  'use strict';

  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('navToggle');
  const navDrawer = document.getElementById('navDrawer');
  const navLinks = document.querySelectorAll('.nav__links a, .nav__drawer a[href^="#"]');

  /* ---- 1. Nav scroll state ---------------------------------- */
  let lastScroll = 0;
  function onScroll() {
    const y = window.scrollY;
    nav.classList.toggle('is-scrolled', y > 50);
    lastScroll = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- 2. Mobile drawer ------------------------------------- */
  if (navToggle && navDrawer) {
    navToggle.addEventListener('click', function () {
      const isOpen = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!isOpen));
      navToggle.setAttribute('aria-label', isOpen ? 'Abrir menu' : 'Fechar menu');
      navDrawer.classList.toggle('is-open', !isOpen);
      navDrawer.hidden = isOpen;
      document.body.style.overflow = isOpen ? '' : 'hidden';
    });
    navDrawer.addEventListener('click', function (e) {
      if (e.target.matches('a')) {
        navToggle.click();
      }
    });
  }

  /* ---- 3. Smooth scroll for in-page anchors ----------------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const id = link.getAttribute('href');
      if (id === '#' || id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const navHeight = nav ? nav.offsetHeight : 0;
      const y = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
      window.scrollTo({ top: y, behavior: 'smooth' });
      history.pushState(null, '', id);
    });
  });

  /* ---- 4. Scroll reveal (IntersectionObserver) -------------- */
  const revealTargets = document.querySelectorAll(
    '.section__title, .section__lead, .section-label, .module-card, .mock-search, .timeline__step, .extension-card, .ia-card, .kanban__col, .dash-card, .price-card, .faq__item, .split__bullets li, .features-grid li, .feature-row, .hero__proof, .hero__ctas, .hero__sub, .proof__stats, .proof__card, .proof__disclaimer'
  );
  revealTargets.forEach(function (el) { el.setAttribute('data-reveal', ''); });

  if ('IntersectionObserver' in window) {
    document.body.classList.add('has-reveals');
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revealTargets.forEach(function (el) { io.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---- 5. FAQ: close others when one opens ----------------- */
  const faqItems = document.querySelectorAll('.faq__item');
  faqItems.forEach(function (item) {
    item.addEventListener('toggle', function () {
      if (item.open) {
        faqItems.forEach(function (other) {
          if (other !== item) other.open = false;
        });
      }
    });
  });

  /* ---- 6. Active section highlight in nav ------------------- */
  if ('IntersectionObserver' in window) {
    const sections = document.querySelectorAll('main section[id]');
    const navMap = new Map();
    navLinks.forEach(function (a) {
      const href = a.getAttribute('href');
      if (href && href.startsWith('#')) navMap.set(href.slice(1), a);
    });
    const activeIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          navMap.forEach(function (a) { a.classList.remove('is-active'); });
          const active = navMap.get(id);
          if (active) active.classList.add('is-active');
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { activeIO.observe(s); });
  }

  /* ---- 7. Animate hero proof on load ----------------------- */
  const heroProof = document.querySelector('.hero__proof');
  if (heroProof) {
    setTimeout(function () { heroProof.classList.add('is-visible'); }, 100);
  }

  /* ---- 8. Animate bars on dashboard cards ------------------- */
  const barCards = document.querySelectorAll('.bars');
  if ('IntersectionObserver' in window && barCards.length) {
    const barIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          barIO.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    barCards.forEach(function (b) { barIO.observe(b); });
  }

  /* ---- 9. Mobile sticky CTA: hide when pricing is in view --- */
  const mobileCta = document.querySelector('.mobile-cta');
  const precosSection = document.getElementById('precos');
  if (mobileCta && precosSection && 'IntersectionObserver' in window) {
    document.body.classList.add('has-mobile-cta');
    const ctaIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        mobileCta.classList.toggle('is-hidden', entry.isIntersecting);
      });
    }, { rootMargin: '-20% 0px -20% 0px' });
    ctaIO.observe(precosSection);
  }

  /* ---- 10. Kanban drag and drop ---------------------------- */
  var kanbanCards = document.querySelectorAll('.kanban__card');
  var kanbanCols = document.querySelectorAll('.kanban__col');

  function updateKanbanCounts() {
    kanbanCols.forEach(function (col) {
      var cards = col.querySelectorAll('.kanban__card');
      var count = col.querySelector('.kanban__count');
      if (count) count.textContent = cards.length;
    });
  }

  kanbanCards.forEach(function (card) {
    card.addEventListener('dragstart', function (e) {
      card.classList.add('is-dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', '');
    });
    card.addEventListener('dragend', function () {
      card.classList.remove('is-dragging');
      kanbanCols.forEach(function (col) { col.classList.remove('drag-over'); });
    });
  });

  kanbanCols.forEach(function (col) {
    var cardsContainer = col.querySelector('.kanban__cards');
    if (!cardsContainer) return;

    col.addEventListener('dragover', function (e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      col.classList.add('drag-over');
    });

    col.addEventListener('dragleave', function (e) {
      if (!col.contains(e.relatedTarget)) {
        col.classList.remove('drag-over');
      }
    });

    col.addEventListener('drop', function (e) {
      e.preventDefault();
      col.classList.remove('drag-over');
      var dragging = document.querySelector('.is-dragging');
      if (dragging && dragging !== col) {
        cardsContainer.appendChild(dragging);
        updateKanbanCounts();
      }
    });
  });
})();
