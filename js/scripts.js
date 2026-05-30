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

    // Touch-driven rotation for mobile
    var spinViewer = document.getElementById('sticky-spin');
    var touchStartX = 0;
    var touchLastX = 0;
    var touchSpinProgress = 0;

    if (spinViewer) {
      spinViewer.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        touchLastX = touchStartX;
        touchSpinProgress = currentFrame / (SPIN_TOTAL - 1);
      }, { passive: true });

      spinViewer.addEventListener('touchmove', function(e) {
        var dx = e.touches[0].clientX - touchLastX;
        touchLastX = e.touches[0].clientX;
        var viewW = spinViewer.offsetWidth;
        touchSpinProgress += dx / (viewW * 0.6);
        touchSpinProgress = Math.max(0, Math.min(1, touchSpinProgress));
        setFrame(touchSpinProgress * (SPIN_TOTAL - 1));
      }, { passive: true });

      spinViewer.addEventListener('touchend', function() {
        touchSpinProgress = currentFrame / (SPIN_TOTAL - 1);
      }, { passive: true });
    }

    var stickyScroll = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        var section = entry.target;
        var ratio = entry.intersectionRatio;

        // Activate section when crossing threshold
        if (ratio > 0.3) {
          var wasInactive = !section.classList.contains('is-active');
          if (wasInactive) {
            // Activate new section BEFORE deactivating others to avoid flash
            section.classList.add('is-active');
            stickySections.forEach(function(s) {
              if (s !== section) s.classList.remove('is-active');
            });
            var kids = section.querySelectorAll('.sticky-media__label, .sticky-media__title, .sticky-media__text, .sticky-media__stats, .sticky-media__stars, .sticky-media__attribution');
            kids.forEach(function(k, i) {
              k.classList.add('stagger-enter');
              k.style.setProperty('--stagger-i', i);
            });
          }
        } else if (section.classList.contains('is-active')) {
          section.classList.remove('is-active');
          var leavingKids = section.querySelectorAll('.sticky-media__label, .sticky-media__title, .sticky-media__text, .sticky-media__stats, .sticky-media__stars, .sticky-media__attribution');
          leavingKids.forEach(function(k) {
            k.classList.remove('stagger-enter');
            k.classList.add('stagger-leave');
            k.style.removeProperty('--stagger-i');
          });
          // Clean up stagger-leave after animation completes
          if (section._leaveTimer) clearTimeout(section._leaveTimer);
          const sec = section;
          sec._leaveTimer = setTimeout(function() {
            sec.querySelectorAll('.sticky-media__label, .sticky-media__title, .sticky-media__text, .sticky-media__stats, .sticky-media__stars, .sticky-media__attribution').forEach(function(k) {
              k.classList.remove('stagger-leave');
            });
          }, 1100);
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

  if (hero3d && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
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
          // Nav name stays as brand logo; no update needed
        }
      });
    }, { threshold: 0.3 });

    navSections.forEach(function(s) { spyObserver.observe(s); });
  }

  // 6. Product nav hamburger toggle
  var productHamburger = document.querySelector('.product-nav__hamburger');
  var productMobile = document.querySelector('.product-nav__mobile');

  if (productHamburger && productMobile) {
    productHamburger.addEventListener('click', function() {
      var expanded = productHamburger.getAttribute('aria-expanded') === 'true';
      productHamburger.setAttribute('aria-expanded', !expanded);
      productMobile.classList.toggle('is-open');
    });

    // Close menu on link click
    productMobile.querySelectorAll('.product-nav__mobile-link').forEach(function(link) {
      link.addEventListener('click', function() {
        productHamburger.setAttribute('aria-expanded', 'false');
        productMobile.classList.remove('is-open');
      });
    });

    // Close on resize past breakpoint
    window.addEventListener('resize', function() {
      if (window.innerWidth > 900) {
        productHamburger.setAttribute('aria-expanded', 'false');
        productMobile.classList.remove('is-open');
      }
    });
  }

})();

/* ==========================================
   SLIDE STORY — Mobile interactive slides
   ========================================== */

(function() {
  'use strict';

  var track = document.querySelector('.slide-story__track');
  var slides = document.querySelectorAll('.slide-story__slide');
  var dotsContainer = document.querySelector('.slide-story__dots');
  if (!track || !slides.length) return;

  var totalSlides = slides.length;

  // Preload spin frames for mobile 360
  var mobileSpinA = document.getElementById('slide-spin-a');
  var mobileSpinB = document.getElementById('slide-spin-b');
  var SPIN_TOTAL = 8;
  var currentFrame = -1;
  var activeImg = mobileSpinA;

  if (mobileSpinA) {
    for (var si = 0; si < SPIN_TOTAL; si++) {
      var snum = (si + 1).toString().padStart(2, '0');
      var simg = new Image();
      simg.src = 'images/spin-' + snum + '.webp';
    }
  }

  function setFrame(idx) {
    if (!mobileSpinA) return;
    idx = Math.round(idx);
    idx = ((idx % SPIN_TOTAL) + SPIN_TOTAL) % SPIN_TOTAL;
    if (idx === currentFrame) return;
    currentFrame = idx;
    var num = (idx + 1).toString().padStart(2, '0');
    var inactiveImg = (activeImg === mobileSpinA) ? mobileSpinB : mobileSpinA;
    inactiveImg.src = 'images/spin-' + num + '.webp';
    activeImg.style.opacity = '0';
    inactiveImg.style.opacity = '1';
    activeImg = inactiveImg;
  }

  // Touch-driven rotation on mobile
  var slideSpinViewer = document.getElementById('slide-spin');
  var touchStartX = 0;
  var touchLastX = 0;
  var touchSpinProgress = 0;

  if (slideSpinViewer) {
    slideSpinViewer.addEventListener('touchstart', function(e) {
      touchStartX = e.touches[0].clientX;
      touchLastX = touchStartX;
      touchSpinProgress = currentFrame / (SPIN_TOTAL - 1) || 0;
    }, { passive: true });

    slideSpinViewer.addEventListener('touchmove', function(e) {
      var dx = e.touches[0].clientX - touchLastX;
      touchLastX = e.touches[0].clientX;
      var viewW = slideSpinViewer.offsetWidth;
      touchSpinProgress += dx / (viewW * 0.6);
      touchSpinProgress = Math.max(0, Math.min(1, touchSpinProgress));
      setFrame(touchSpinProgress * (SPIN_TOTAL - 1));
    }, { passive: true });

    slideSpinViewer.addEventListener('touchend', function() {
      touchSpinProgress = currentFrame / (SPIN_TOTAL - 1) || 0;
    }, { passive: true });
  }

  // Create progress dots
  for (var d = 0; d < totalSlides; d++) {
    var dot = document.createElement('div');
    dot.className = 'slide-story__dot' + (d === 0 ? ' is-active' : '');
    dot.setAttribute('data-dot', d);
    dot.addEventListener('click', function() {
      var idx = parseInt(this.getAttribute('data-dot'));
      var targetSlide = slides[idx];
      if (targetSlide) targetSlide.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    dotsContainer.appendChild(dot);
  }

  var dots = dotsContainer.querySelectorAll('.slide-story__dot');

  // IntersectionObserver for slide visibility + animations
  var currentActive = 0;

  var slideObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      var slide = entry.target;
      var idx = parseInt(slide.getAttribute('data-slide'));

      if (entry.isIntersecting) {
        if (!slide.classList.contains('is-visible')) {
          slide.classList.add('is-visible');
          animateCounters(slide);
        }

        if (idx >= 0 && idx < totalSlides) {
          currentActive = idx;
          dots.forEach(function(d, i) {
            d.classList.toggle('is-active', i === idx);
          });
        }
      }
    });
  }, { threshold: 0.3 });

  slides.forEach(function(s) { slideObserver.observe(s); });

  function animateCounters(slide) {
    var counters = slide.querySelectorAll('.slide-story__stat-value[data-target]');
    counters.forEach(function(el) {
      var target = parseFloat(el.getAttribute('data-target'));
      if (isNaN(target)) return;
      var duration = 600;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = eased * target;

        if (Number.isInteger(target)) {
          el.textContent = Math.round(current);
        } else {
          el.textContent = current.toFixed(1);
        }

        if (progress < 1) {
          window.requestAnimationFrame(step);
        }
      }

      window.requestAnimationFrame(step);
    });
  }

})();

