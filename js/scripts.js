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

  // 1. Continuous Sticky Media Transition — staggered element reveal + 360 spin
  var stickySections = document.querySelectorAll('.sticky-media__section');
  var stickyMedia = document.querySelector('.sticky-media');

  if (stickySections.length && stickyMedia) {
    var SPIN_TOTAL = 8;
    var frameA = document.getElementById('spin-frame-a');
    var frameB = document.getElementById('spin-frame-b');
    // Preload 8 spin frames
    for (var si = 0; si < SPIN_TOTAL; si++) {
      var snum = (si + 1).toString().padStart(2, '0');
      var simg = new Image();
      simg.src = 'images/spin-' + snum + '.webp';
    }

    var currentFrame = -1;
    var scrollTicking = false;
    var activeImg = frameA;

    function setFrame(idx) {
      idx = Math.round(idx);
      idx = ((idx % SPIN_TOTAL) + SPIN_TOTAL) % SPIN_TOTAL;
      if (idx === currentFrame) return;
      currentFrame = idx;
      var num = (idx + 1).toString().padStart(2, '0');
      var inactiveImg = (activeImg === frameA) ? frameB : frameA;
      inactiveImg.src = 'images/spin-' + num + '.webp';
      activeImg.style.opacity = '0';
      inactiveImg.style.opacity = '1';
      activeImg = inactiveImg;
    }

    // Smooth scroll-driven rotation
    window.addEventListener('scroll', function() {
      if (!scrollTicking) {
        window.requestAnimationFrame(function() {
          var rect = stickyMedia.getBoundingClientRect();
          var viewH = window.innerHeight;
          var totalH = stickyMedia.offsetHeight;
          var progress = (viewH - rect.top) / (totalH + viewH);
          progress = Math.max(0, Math.min(1, progress));
          setFrame(progress * (SPIN_TOTAL - 1));
          scrollTicking = false;
        });
        scrollTicking = true;
      }
    }, { passive: true });

    var stickyScroll = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var section = entry.target;
        var ratio = entry.intersectionRatio;

        // Activate section when crossing threshold
        if (ratio > 0.35) {
          var wasInactive = !section.classList.contains('is-active');
          stickySections.forEach(function(s) { s.classList.remove('is-active'); });
          section.classList.add('is-active');
          if (wasInactive) {
            var kids = section.querySelectorAll('.sticky-media__label, .sticky-media__title, .sticky-media__text, .sticky-media__stats, .sticky-media__stars, .sticky-media__attribution');
            kids.forEach(function(k, i) {
              k.classList.add('stagger-enter');
              k.style.setProperty('--stagger-i', i);
            });
          }
        } else if (section.classList.contains('is-active')) {
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


