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
   APPLE-STYLE LANDING PAGE — Interactions
   ========================================== */

(function() {
  'use strict';

  // 1. Product Nav Transition
  var nav = document.querySelector('.product-nav');
  var hero = document.querySelector('.hero--apple');

  if (nav && hero) {
    function updateNav() {
      var heroBottom = hero.offsetTop + hero.offsetHeight;
      if (window.scrollY >= heroBottom - 80) {
        nav.classList.add('product-nav--scrolled');
      } else {
        nav.classList.remove('product-nav--scrolled');
      }
    }

    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  }



})();

/* ==========================================
   APPLE FIDELITY — New Interactions
   ========================================== */

(function() {
  'use strict';



  // 2. Paint Reveal — trigger clip-path animation on scroll
  var paintReveal = document.querySelector('.paint-reveal');

  if (paintReveal) {
    var revealObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          paintReveal.classList.add('is-revealed');
        }
      });
    }, { threshold: 0.3 });

    revealObserver.observe(paintReveal);
  }



})();

/* ==========================================
   SQUAD UPGRADE — Continuous + Interactive
   ========================================== */

(function() {
  'use strict';

  // 1. Continuous Sticky Media Transition — staggered element reveal
  var stickySections = document.querySelectorAll('.sticky-media__section');
  var stickyImages = document.querySelectorAll('.sticky-media__image');

  if (stickySections.length && stickyImages.length) {
    var stickyScroll = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var section = entry.target;
        var sectionId = section.getAttribute('data-section');
        var ratio = entry.intersectionRatio;
        var img = document.querySelector('.sticky-media__image[data-section="' + sectionId + '"]');

        // Image parallax scale (scroll-driven)
        if (img && ratio > 0 && ratio < 0.6) {
          img.style.transform = 'scale(' + (0.96 + ratio * 0.06) + ')';
        } else if (img) {
          img.style.transform = 'scale(1)';
        }

        // Activate section when crossing threshold
        if (ratio > 0.35) {
          var wasInactive = !section.classList.contains('is-active');
          stickyImages.forEach(function(i) { i.classList.remove('is-active'); });
          stickySections.forEach(function(s) { s.classList.remove('is-active'); });
          if (img) img.classList.add('is-active');
          section.classList.add('is-active');

          // Trigger stagger animation on first activation
          if (wasInactive) {
            var kids = section.querySelectorAll('.sticky-media__label, .sticky-media__title, .sticky-media__text, .sticky-media__stats, .sticky-media__stars, .sticky-media__attribution');
            kids.forEach(function(k, i) {
              k.classList.add('stagger-enter');
              k.style.setProperty('--stagger-i', i);
            });
          }
        } else if (section.classList.contains('is-active')) {
          // Reset stagger when leaving
          var kids = section.querySelectorAll('.sticky-media__label, .sticky-media__title, .sticky-media__text, .sticky-media__stats, .sticky-media__stars, .sticky-media__attribution');
          kids.forEach(function(k) {
            k.classList.remove('stagger-enter');
            k.style.removeProperty('--stagger-i');
          });
          section.classList.remove('is-active');
        }
      });
    }, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] });

    stickySections.forEach(function(s) { stickyScroll.observe(s); });
  }

  // 2. Highlights Interactive Tabs
  var tabCards = document.querySelectorAll('.highlights--tabs .highlights__card');
  var tabImages = document.querySelectorAll('.highlights--tabs .highlights__img');

  if (tabCards.length && tabImages.length) {
    tabCards.forEach(function(card) {
      card.addEventListener('click', function() {
        var highlight = this.getAttribute('data-highlight');

        tabCards.forEach(function(c) { c.classList.remove('is-active'); c.setAttribute('aria-selected', 'false'); c.setAttribute('tabindex', '-1'); });
        tabImages.forEach(function(img) { img.classList.remove('is-active'); });

        this.classList.add('is-active');
        this.setAttribute('aria-selected', 'true');
        this.setAttribute('tabindex', '0');
        var activeImg = document.querySelector('.highlights--tabs .highlights__img[data-highlight="' + highlight + '"]');
        if (activeImg) activeImg.classList.add('is-active');
      });

      card.addEventListener('keydown', function(e) {
        var cards = Array.from(tabCards);
        var idx = cards.indexOf(this);
        
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.click();
        } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          var nextIdx = (idx + 1) % cards.length;
          cards[nextIdx].click();
          cards[nextIdx].focus();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          var prevIdx = (idx - 1 + cards.length) % cards.length;
          cards[prevIdx].click();
          cards[prevIdx].focus();
        }
      });
    });
  }

  // 3. 3D Parallax Hero
  var hero3d = document.querySelector('.hero--apple');

  if (hero3d) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return;
    }
    hero3d.classList.add('is-3d');

    hero3d.addEventListener('mousemove', function(e) {
      var bg = this.querySelector('.hero--apple__bg');
      if (!bg) return;

      var rect = this.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width - 0.5;
      var y = (e.clientY - rect.top) / rect.height - 0.5;

      var rotateY = x * 8;
      var rotateX = -y * 8;

      bg.style.transform = 'perspective(1000px) rotateY(' + rotateY + 'deg) rotateX(' + rotateX + 'deg) scale(1.05)';
    });

    hero3d.addEventListener('mouseleave', function() {
      var bg = this.querySelector('.hero--apple__bg');
      if (bg) {
        bg.style.transform = '';
      }
    });
  }

  // 4. Why Buy cards — sequential reveal
  var whyBuyCards = document.querySelectorAll('.whybuy__card');

  if (whyBuyCards.length) {
    whyBuyCards.forEach(function(card) {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
    });

    var whyBuyObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var cards = entry.target.querySelectorAll('.whybuy__card');
          cards.forEach(function(card, i) {
            setTimeout(function() {
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            }, i * 100);
          });
          whyBuyObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    var whyBuySection = document.querySelector('.whybuy');
    if (whyBuySection) whyBuyObserver.observe(whyBuySection);
  }

  // 5. Scroll-spy for product nav
  var navLinks = document.querySelectorAll('.product-nav__link');
  var navSections = document.querySelectorAll('[data-nav]');

  if (navLinks.length && navSections.length) {
    var spyObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var sectionId = entry.target.getAttribute('data-nav');
          navLinks.forEach(function(link) {
            link.removeAttribute('aria-current');
            link.style.fontWeight = '';
          });
          var activeLink = document.querySelector('.product-nav__link[href="#' + sectionId + '"]');
          if (activeLink) {
            activeLink.setAttribute('aria-current', 'section');
            activeLink.style.fontWeight = '700';
          }
          // Also update product-nav name for hero
          var navName = document.querySelector('.product-nav__name');
          if (sectionId === 'hero' && navName) {
            navName.textContent = 'PaintPro™';
          }
        }
      });
    }, { threshold: 0.3 });

    navSections.forEach(function(s) { spyObserver.observe(s); });
  }

})();

/* ==========================================
   VISTA 360° — Spin Viewer
   ========================================== */

(function() {
  'use strict';

  var frame = document.getElementById('spin-frame');
  if (!frame) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var TOTAL = 10;
  var images = [];
  var current = 0;
  var isDragging = false;
  var startX = 0;
  var autoTimer = null;
  var viewer = frame.parentElement;
  var dots = document.getElementById('spin-dots');
  var hint = viewer.querySelector('.spin-360__hint');
  var loaded = 0;

  // Preload all frames
  for (var i = 0; i < TOTAL; i++) {
    var num = (i + 1).toString().padStart(2, '0');
    var img = new Image();
    img.onload = function() { loaded++; };
    img.src = 'images/spin-' + num + '.webp';
    images.push(img);
  }

  // Create dots
  for (var i = 0; i < TOTAL; i++) {
    var dot = document.createElement('button');
    dot.className = 'spin-360__dot' + (i === 0 ? ' is-active' : '');
    dot.setAttribute('data-dot', i);
    dot.setAttribute('aria-label', 'Angulo ' + (i + 1));
    dot.addEventListener('click', function() {
      var idx = parseInt(this.getAttribute('data-dot'));
      showFrame(idx);
    });
    dots.appendChild(dot);
  }

  function showFrame(idx) {
    if (idx < 0) idx = TOTAL - 1;
    if (idx >= TOTAL) idx = 0;
    current = idx;
    var num = (current + 1).toString().padStart(2, '0');
    frame.src = 'images/spin-' + num + '.webp';
    var allDots = dots.querySelectorAll('.spin-360__dot');
    allDots.forEach(function(d, i) {
      d.classList.toggle('is-active', i === current);
    });
  }

  function autoRotate() {
    showFrame(current + 1);
  }

  function startAuto() {
    stopAuto();
    autoTimer = setInterval(autoRotate, 200);
  }

  function stopAuto() {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
    }
  }

  // Mouse drag
  viewer.addEventListener('mousedown', function(e) {
    isDragging = true;
    startX = e.clientX;
    stopAuto();
    if (hint) hint.classList.add('is-hidden');
    e.preventDefault();
  });

  window.addEventListener('mousemove', function(e) {
    if (!isDragging) return;
    var delta = e.clientX - startX;
    if (Math.abs(delta) > 30) {
      var dir = delta > 0 ? 1 : -1;
      showFrame(current + dir);
      startX = e.clientX;
    }
  });

  window.addEventListener('mouseup', function() {
    if (isDragging) {
      isDragging = false;
      startAuto();
    }
  });

  // Touch support
  viewer.addEventListener('touchstart', function(e) {
    isDragging = true;
    startX = e.touches[0].clientX;
    stopAuto();
    if (hint) hint.classList.add('is-hidden');
  }, { passive: true });

  viewer.addEventListener('touchmove', function(e) {
    if (!isDragging) return;
    var delta = e.touches[0].clientX - startX;
    if (Math.abs(delta) > 30) {
      var dir = delta > 0 ? 1 : -1;
      showFrame(current + dir);
      startX = e.touches[0].clientX;
    }
  }, { passive: true });

  viewer.addEventListener('touchend', function() {
    if (isDragging) {
      isDragging = false;
      startAuto();
    }
  }, { passive: true });

  // Start auto-rotate
  startAuto();

  // Stop on visibility change
  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      stopAuto();
    } else {
      startAuto();
    }
  });

})();
