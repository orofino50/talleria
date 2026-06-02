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
      if (isOpen) {
        item.removeAttribute('open');
      } else {
        item.setAttribute('open', '');
      }
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

  // 1. Unified 360 Touch Rotation + Section Reveal
  var SPIN_TOTAL = 8;
  var spinPreloaded = false;

  function preloadSpinFrames() {
    if (spinPreloaded) return;
    spinPreloaded = true;
    for (var si = 0; si < SPIN_TOTAL; si++) {
      var snum = (si + 1).toString().padStart(2, '0');
      var simg = new Image();
      simg.src = 'images/spin-' + snum + '.webp';
    }
  }

  // Lazy-load spin frames when any viewer enters viewport
  var productSpin = document.getElementById('product-spin');
  var spinMobile = document.getElementById('spin-mobile');
  var spinTargets = [productSpin, spinMobile].filter(Boolean);

  if (spinTargets.length && 'IntersectionObserver' in window) {
    var spinObserver = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting) {
        preloadSpinFrames();
        spinObserver.disconnect();
      }
    }, { rootMargin: '200px' });
    spinTargets.forEach(function(el) { spinObserver.observe(el); });
  } else {
    preloadSpinFrames();
  }

  var spinA = document.getElementById('spin-a');
  var spinB = document.getElementById('spin-b');
  var spinMobileA = document.getElementById('spin-mobile-a');
  var spinMobileB = document.getElementById('spin-mobile-b');
  var currentFrame = -1;
  var activeImg = spinA;
  var activeMobileImg = spinMobileA;

  function setFrame(idx) {
    idx = Math.round(idx);
    idx = ((idx % SPIN_TOTAL) + SPIN_TOTAL) % SPIN_TOTAL;
    if (idx === currentFrame) return;
    currentFrame = idx;
    var num = (idx + 1).toString().padStart(2, '0');
    var src = 'images/spin-' + num + '.webp';

    // Update desktop frames
    if (spinA) {
      var inactiveImg = (activeImg === spinA) ? spinB : spinA;
      inactiveImg.src = src;
      activeImg.style.opacity = '0';
      inactiveImg.style.opacity = '1';
      activeImg = inactiveImg;
    }

    // Update mobile frames
    if (spinMobileA) {
      var inactiveMobile = (activeMobileImg === spinMobileA) ? spinMobileB : spinMobileA;
      inactiveMobile.src = src;
      activeMobileImg.style.opacity = '0';
      inactiveMobile.style.opacity = '1';
      activeMobileImg = inactiveMobile;
    }
  }

  // Touch-driven rotation — reusable for any viewer
  function setupTouchSpin(viewer) {
    if (!viewer) return;
    var lastX = 0;
    var progress = 0;

    viewer.addEventListener('touchstart', function(e) {
      lastX = e.touches[0].clientX;
      progress = currentFrame / (SPIN_TOTAL - 1) || 0;
    }, { passive: true });

    viewer.addEventListener('touchmove', function(e) {
      var dx = e.touches[0].clientX - lastX;
      lastX = e.touches[0].clientX;
      var viewW = viewer.offsetWidth;
      progress += dx / (viewW * 0.6);
      progress = Math.max(0, Math.min(1, progress));
      setFrame(progress * (SPIN_TOTAL - 1));
    }, { passive: true });

    viewer.addEventListener('touchend', function() {
      progress = currentFrame / (SPIN_TOTAL - 1) || 0;
    }, { passive: true });

    var hint = viewer.querySelector('.spin-360__scroll-hint');
    if (hint) {
      viewer.addEventListener('touchstart', function() {
        hint.classList.add('is-hidden');
      }, { once: true, passive: true });
    }
  }

  setupTouchSpin(productSpin);
  setupTouchSpin(document.getElementById('spin-mobile'));

  // Simple reveal on scroll for showcase sections (all viewports)
  var showcaseSections = document.querySelectorAll('.product-showcase__section');
  if (showcaseSections.length) {
    var secObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          secObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    showcaseSections.forEach(function(s) { secObserver.observe(s); });
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

    var heroTicking = false;
    var heroLastEvent = null;
    hero3d.addEventListener('mousemove', function(e) {
      heroLastEvent = e;
      if (heroTicking) return;
      heroTicking = true;
      requestAnimationFrame(function() {
        heroTicking = false;
        var ev = heroLastEvent;
        if (!ev) return;
        var bg = hero3d.querySelector('.hero--apple__bg');
        if (!bg) return;

        var rect = hero3d.getBoundingClientRect();
        var x = (ev.clientX - rect.left) / rect.width - 0.5;
        var y = (ev.clientY - rect.top) / rect.height - 0.5;

        var rotateY = x * 8;
        var rotateX = -y * 8;

        bg.style.transform = 'perspective(1000px) rotateY(' + rotateY + 'deg) rotateX(' + rotateX + 'deg) scale(1.05)';
      });
    });

    hero3d.addEventListener('mouseleave', function() {
      heroLastEvent = null;
      var bg = hero3d.querySelector('.hero--apple__bg');
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

  // 6. Video player (autoplay muted, pause off-screen, click to toggle)
  var videoPlayers = document.querySelectorAll('[data-video-player]');
  videoPlayers.forEach(function(videoPlayer) {
    var videoPlayBtn = videoPlayer.querySelector('[data-video-play]');
    var video = videoPlayer.querySelector('video');
    if (!video) return;

    function togglePlay(e) {
      if (e) e.stopPropagation();
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    }
    if (videoPlayBtn) videoPlayBtn.addEventListener('click', togglePlay);
    videoPlayer.addEventListener('click', togglePlay);
    videoPlayer.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        togglePlay();
      }
    });

    // Sincronizar classe is-paused com estado real do vídeo
    // - playing event: vídeo começou a tocar (autoplay ou click)
    // - pause event: usuário pausou
    // - ended event: vídeo terminou
    function setPaused(paused) {
      if (paused) {
        videoPlayer.classList.add('is-paused');
        if (videoPlayBtn) {
          videoPlayBtn.setAttribute('aria-label', 'Reproducir video');
          videoPlayBtn.setAttribute('aria-pressed', 'false');
        }
      } else {
        videoPlayer.classList.remove('is-paused');
        if (videoPlayBtn) {
          videoPlayBtn.setAttribute('aria-label', 'Pausar video');
          videoPlayBtn.setAttribute('aria-pressed', 'true');
        }
      }
    }
    video.addEventListener('playing', function() { setPaused(false); });
    video.addEventListener('pause', function() { setPaused(true); });
    video.addEventListener('ended', function() { setPaused(true); });

    // Estado inicial: se o vídeo já está tocando (autoplay começou antes do listener),
    // remove is-paused; se está pausado (autoplay bloqueado), mostra play button
    if (!video.paused) {
      setPaused(false);
    } else {
      // Esperar 300ms para ver se autoplay começa
      setTimeout(function() {
        if (video.paused) setPaused(true);
      }, 300);
    }

    // Pausar quando sai do viewport (performance: não toca áudio/vídeo off-screen)
    if ('IntersectionObserver' in window) {
      var videoObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
            // Tentar reproduzir (silencia erros de autoplay bloqueado)
            video.play().catch(function() { /* autoplay bloqueado, sem problema */ });
          } else {
            video.pause();
          }
        });
      }, { threshold: [0, 0.3, 0.5] });
      videoObserver.observe(videoPlayer);
    }
  });

})();



