/* ===================================
   EDITORIAL INTERACTIONS - AWWWARDS LEVEL
   =================================== */

class EditorialSite {
  constructor() {
    this.init();
  }

  init() {
    // Core interaction systems
    this.setupScrollReveal();
    this.setupMagneticButtons();
    this.setupCounters();
    this.setupApiDemo();
    this.setupAccessibility();
    this.setupRegionalParallax(); // Add regional storytelling parallax
    
    // Initialize on load
    document.addEventListener('DOMContentLoaded', () => {
      this.triggerEntryAnimation();
    });
  }

  /* ===================================
     SCROLL REVEAL - PURPOSEFUL MOTION
     =================================== */
  
  setupScrollReveal() {
    const observerOptions = {
      threshold: 0.15,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          
          // Trigger counter animations for stats
          if (entry.target.querySelector('[data-count]')) {
            this.animateCounters(entry.target);
          }
        }
      });
    }, observerOptions);

    // Observe methodology and API sections
    document.querySelectorAll('.methodology, .api, .sources').forEach((el) => {
      el.classList.add('scroll-reveal');
      observer.observe(el);
    });
  }

  /* ===================================
     MAGNETIC BUTTONS - TACTILE FEEL
     =================================== */
  
  setupMagneticButtons() {
    const magneticElements = document.querySelectorAll('.cta-primary, .api-try-btn');
    
    magneticElements.forEach((button) => {
      button.addEventListener('mousemove', (e) => {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        // Subtle magnetic strength - editorial restraint
        const strength = 0.15;
        const translateX = x * strength;
        const translateY = y * strength;
        
        button.style.transform = `translate(${translateX}px, ${translateY}px)`;
      });

      button.addEventListener('mouseleave', () => {
        button.style.transform = 'translate(0, 0)';
      });

      // Add active state
      button.addEventListener('mousedown', () => {
        button.style.transform = 'translate(0, 2px) scale(0.98)';
      });

      button.addEventListener('mouseup', () => {
        button.style.transform = 'translate(0, 0)';
      });
    });
  }

  /* ===================================
     COUNTER ANIMATIONS - DATA FOCUS WITH REGIONAL STORYTELLING
     =================================== */
  
  animateCounters(container = document) {
    const counters = container.querySelectorAll('[data-count]');
    
    counters.forEach((counter, index) => {
      if (counter.classList.contains('counted')) return;
      
      const target = parseInt(counter.getAttribute('data-count'));
      const duration = 1200; // Slightly faster for editorial feel
      
      // Stagger animation start for regional flow effect
      const delay = index * 120; // 120ms stagger between stats
      
      setTimeout(() => {
        const startTime = performance.now();
        
        const updateCounter = (currentTime) => {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          
          // Smooth easing - no bounce
          const easeOut = 1 - Math.pow(1 - progress, 2.5);
          const current = Math.floor(easeOut * target);
          
          // Format numbers appropriately
          counter.textContent = this.formatNumber(current, target);
          
          // Add subtle glow effect during animation for regional emphasis
          if (progress > 0 && progress < 1) {
            counter.style.textShadow = `0 0 ${8 * progress}px rgba(0, 102, 204, 0.3)`;
          } else {
            counter.style.textShadow = 'none';
          }
          
          if (progress < 1) {
            requestAnimationFrame(updateCounter);
          } else {
            counter.textContent = this.formatNumber(target, target);
            counter.style.textShadow = 'none';
            counter.classList.add('counted', 'animate-counter');
          }
        };
        
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          requestAnimationFrame(updateCounter);
        } else {
          counter.textContent = this.formatNumber(target, target);
          counter.classList.add('counted');
        }
      }, delay);
    });
  }

  formatNumber(num, target) {
    // Keep original formatting for specific cases
    if (target === 21 || target.toString().includes('%')) {
      return target.toString();
    }
    
    // Add commas for larger numbers
    if (num >= 1000) {
      return num.toLocaleString();
    }
    
    return num.toString();
  }

  /* ===================================
     REGIONAL STORYTELLING - SUBTLE PARALLAX
     =================================== */
  
  setupRegionalParallax() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    // Subtle parallax effect for satellite background
    const parallaxHandler = this.throttle((e) => {
      const scrolled = window.pageYOffset;
      const heroHeight = hero.offsetHeight;
      const viewportHeight = window.innerHeight;
      
      // Only apply parallax when hero is visible
      if (scrolled < heroHeight) {
        const parallaxSpeed = 0.3; // Very subtle movement
        const yPos = -(scrolled * parallaxSpeed);
        
        // Apply transform to the pseudo-element background
        hero.style.setProperty('--parallax-y', `${yPos}px`);
      }
    }, 16); // 60fps throttling
    
    window.addEventListener('scroll', parallaxHandler, { passive: true });
    
    // Mouse-based subtle movement for regional storytelling
    const mouseHandler = this.throttle((e) => {
      if (window.innerWidth < 768) return; // Skip on mobile
      
      const centerX = window.innerWidth / 2;
      const centerY = window.innerHeight / 2;
      
      const mouseX = (e.clientX - centerX) / centerX;
      const mouseY = (e.clientY - centerY) / centerY;
      
      // Very subtle movement that suggests regional awareness
      const moveX = mouseX * 8; // Maximum 8px movement
      const moveY = mouseY * 5; // Maximum 5px movement
      
      hero.style.setProperty('--mouse-x', `${moveX}px`);
      hero.style.setProperty('--mouse-y', `${moveY}px`);
    }, 32); // Smooth but not too frequent
    
    document.addEventListener('mousemove', mouseHandler, { passive: true });
  }

  /* ===================================
     API DEMO - INTERACTIVE PROOF
     =================================== */
  
  setupApiDemo() {
    const demoButton = document.querySelector('[data-api-demo]');
    const resultContainer = document.querySelector('#api-result');
    
    if (demoButton && resultContainer) {
      demoButton.addEventListener('click', () => this.runApiDemo(resultContainer));
    }
  }

  async runApiDemo(resultContainer) {
    const baseUrl = window.location.origin;
    
    try {
      // Show loading state
      resultContainer.style.display = 'block';
      resultContainer.textContent = 'Fetching live data...';
      resultContainer.style.opacity = '0.6';
      
      const response = await fetch(`${baseUrl}/api/stats`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      
      // Format response for display
      const formattedResponse = JSON.stringify(data, null, 2);
      
      // Animate in result
      resultContainer.style.opacity = '0';
      setTimeout(() => {
        resultContainer.textContent = formattedResponse;
        resultContainer.style.opacity = '1';
      }, 150);
      
    } catch (error) {
      // Show graceful error
      resultContainer.style.opacity = '0';
      setTimeout(() => {
        resultContainer.textContent = `// API Demo\n// Error: ${error.message}\n// Note: Start local server for live data`;
        resultContainer.style.opacity = '0.7';
      }, 150);
    }
  }

  /* ===================================
     ENTRY ANIMATION - CINEMATIC REVEAL
     =================================== */
  
  triggerEntryAnimation() {
    // Hero elements already have CSS animations
    // This ensures they trigger properly
    const hero = document.querySelector('.hero');
    if (hero) {
      hero.classList.add('loaded');
    }
    
    // Subtle body fade-in
    document.body.style.opacity = '0';
    requestAnimationFrame(() => {
      document.body.style.transition = 'opacity 0.4s ease';
      document.body.style.opacity = '1';
    });
  }

  /* ===================================
     ACCESSIBILITY - INCLUSIVE DESIGN
     =================================== */
  
  setupAccessibility() {
    // Reduced motion handling
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    const handleReducedMotion = (e) => {
      if (e.matches) {
        document.body.classList.add('reduced-motion');
        
        // Disable complex animations
        const animatedElements = document.querySelectorAll('[style*="animation"]');
        animatedElements.forEach((el) => {
          el.style.animation = 'none';
          el.style.transform = 'none';
          el.style.opacity = '1';
        });
      } else {
        document.body.classList.remove('reduced-motion');
      }
    };

    mediaQuery.addEventListener('change', handleReducedMotion);
    handleReducedMotion(mediaQuery);

    // Focus management for skip links (future enhancement)
    this.setupFocusManagement();
    
    // Keyboard navigation enhancement
    this.setupKeyboardNavigation();
  }

  setupFocusManagement() {
    // Enhanced focus indicators already in CSS
    // This could be extended for skip links
    const focusableElements = document.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled])'
    );
    
    focusableElements.forEach(element => {
      element.addEventListener('focus', () => {
        element.classList.add('focused');
      });
      
      element.addEventListener('blur', () => {
        element.classList.remove('focused');
      });
    });
  }

  setupKeyboardNavigation() {
    // Enhanced keyboard navigation
    document.addEventListener('keydown', (e) => {
      // ESC to close any open modals/dropdowns (future)
      if (e.key === 'Escape') {
        // Could close open elements
      }
      
      // Enter/Space for button-like elements
      if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[role="button"]')) {
        e.preventDefault();
        e.target.click();
      }
    });
  }

  /* ===================================
     PERFORMANCE UTILITIES
     =================================== */
  
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }
}

/* ===================================
   INITIALIZATION
   =================================== */

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new EditorialSite();
  });
} else {
  new EditorialSite();
}

// Export for potential module usage
window.EditorialSite = EditorialSite;