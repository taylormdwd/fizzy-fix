/* ============================================================
   FIZZY FIX — script.js
   Vanilla JS. No bundler. GSAP loaded from CDN.
   ============================================================ */

(() => {
  'use strict';

  /* ---------- 1. Sticky banner rotation ---------- */
  const bannerMessages = [
    'DM @FIZZYFIXAZ TO LOCK IN YOUR DATE',
    'NOW BOOKING SPRING 2026 EVENTS',
    'SPRING MENU IS LIVE'
  ];
  const bannerEl = document.getElementById('topBannerText');
  if (bannerEl) {
    let idx = 0;
    setInterval(() => {
      bannerEl.classList.add('is-fading');
      setTimeout(() => {
        idx = (idx + 1) % bannerMessages.length;
        bannerEl.textContent = bannerMessages[idx];
        bannerEl.classList.remove('is-fading');
      }, 350);
    }, 5000);
  }

  /* ---------- 2. Mobile nav toggle ---------- */
  const navToggle = document.querySelector('.nav__toggle');
  const navLinks = document.getElementById('navLinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const open = navLinks.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    navLinks.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- 3. Hero GSAP fade-in ---------- */
  if (window.gsap) {
    gsap.from('.hero__copy > *', {
      opacity: 0, y: 24, duration: 0.7, ease: 'power2.out', stagger: 0.18
    });
    gsap.from('.hero__media', {
      opacity: 0, scale: 0.96, duration: 0.9, ease: 'power3.out', delay: 0.3
    });
    gsap.from('.hero__mascot', {
      opacity: 0, y: -20, scale: 0.5, duration: 0.6, ease: 'back.out(2.2)', delay: 0.9
    });
  }

  /* ---------- 4. Menu tab switcher (3 tabs) ---------- */
  const menuTabs = document.querySelectorAll('.menu__tab');
  const menuPanels = document.querySelectorAll('.menu__panel');
  menuTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      menuTabs.forEach((t) => {
        const active = t === tab;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      menuPanels.forEach((p) => {
        p.classList.toggle('is-active', p.id === `panel-${target}`);
      });
    });
  });

  /* ---------- 5. Trailer / Cart package toggle ---------- */
  const pkgBtns = document.querySelectorAll('.toggle-group__btn');
  const pkgPanels = document.querySelectorAll('.package-panel');
  pkgBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-pkg');
      pkgBtns.forEach((b) => {
        const active = b === btn;
        b.classList.toggle('is-active', active);
        b.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      pkgPanels.forEach((p) => {
        p.classList.toggle('is-active', p.id === `pkg-${target}`);
      });
    });
  });

  /* ---------- 6. Inquiry form toast ---------- */
  const form = document.getElementById('inquiry');
  const toast = document.getElementById('toast');

  function showToast(message) {
    if (!toast) {
      alert(message);
      return;
    }
    toast.textContent = message;
    toast.classList.add('is-visible');
    setTimeout(() => toast.classList.remove('is-visible'), 5000);
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      // demo only — prevent navigation, show confirmation toast.
      // In production, remove preventDefault to let Jotform action take over.
      e.preventDefault();
      showToast(
        "Thank you so much for your interest in booking us for your special event. " +
        "We will be in touch within the next 24 to 48 hours."
      );
      form.reset();
    });
  }

  /* ---------- 6b. Custom drink CTA: pre-fill inquiry notes ---------- */
  const customDrinkCta = document.getElementById('custom-drink-cta');
  if (customDrinkCta) {
    customDrinkCta.addEventListener('click', () => {
      const notes = document.querySelector('#inquiry textarea[name="notes"]');
      if (notes && !notes.value.trim()) {
        notes.value = "I'd like to chat about a custom signature drink for my event — colors, theme, name on the cup, etc.";
      }
      // Focus after the smooth-scroll handler finishes scrolling.
      setTimeout(() => notes && notes.focus({ preventScroll: true }), 700);
    });
  }

  /* ---------- 6c. Event tile lightbox ---------- */
  const lightbox = document.getElementById('eventLightbox');
  if (lightbox) {
    const lbImg = lightbox.querySelector('.lightbox__img');
    const lbTitle = lightbox.querySelector('#lightboxTitle');
    const lbLoc = lightbox.querySelector('#lightboxLoc');
    const lbClose = lightbox.querySelector('.lightbox__close');
    let lastFocused = null;

    const openLightbox = (btn) => {
      lastFocused = btn;
      lbImg.src = btn.dataset.src;
      lbImg.alt = btn.dataset.title + ' in ' + btn.dataset.loc;
      lbTitle.textContent = btn.dataset.title;
      lbLoc.textContent = btn.dataset.loc;
      lightbox.classList.add('is-open');
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      // focus close button for keyboard users
      requestAnimationFrame(() => lbClose.focus());
    };

    const closeLightbox = () => {
      lightbox.classList.remove('is-open');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      lbImg.src = '';
      if (lastFocused) lastFocused.focus();
    };

    document.querySelectorAll('.event-tile__btn').forEach((btn) => {
      btn.addEventListener('click', () => openLightbox(btn));
    });

    lbClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
      // click on backdrop (not the image or caption) closes
      if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('is-open')) {
        closeLightbox();
      }
    });
  }

  /* ---------- 6d. FAQ reveal on scroll (staggered fade-up) ---------- */
  const faqItems = document.querySelectorAll('.faq-item');
  if (faqItems.length && 'IntersectionObserver' in window) {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion) {
      faqItems.forEach((el) => el.classList.add('is-revealed'));
    } else {
      const revealedOrder = [];
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !entry.target.classList.contains('is-revealed')) {
            const idx = revealedOrder.length;
            revealedOrder.push(entry.target);
            // stagger by 90ms per item in the batch, capped so it never feels slow
            const delay = Math.min(idx * 90, 540);
            setTimeout(() => entry.target.classList.add('is-revealed'), delay);
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -60px 0px', threshold: 0.15 });
      faqItems.forEach((el) => observer.observe(el));
    }
  } else if (faqItems.length) {
    // older browsers — just show them
    faqItems.forEach((el) => el.classList.add('is-revealed'));
  }

  /* ---------- 7. Smooth scroll polish ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const banner = document.querySelector('.top-banner')?.offsetHeight || 0;
      const nav = document.querySelector('.nav')?.offsetHeight || 0;
      const top = target.getBoundingClientRect().top + window.scrollY - banner - nav - 8;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
})();
