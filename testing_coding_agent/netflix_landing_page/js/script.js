/**
 * Netflix-Inspired Landing Page - JavaScript
 * Minimal interactivity for FAQ, mobile menu, and form validation
 */

// ============================================
// 1. DOM Content Loaded
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all components
    initNavbar();
    initMobileMenu();
    initFAQAccordion();
    initEmailForms();
    initSmoothScrolling();
    initBackgroundVideoFallback();
});

// ============================================
// 2. Navigation Bar (Scroll Effect)
// ============================================
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ============================================
// 3. Mobile Menu Toggle
// ============================================
function initMobileMenu() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navbarContainer = document.querySelector('.navbar-container');
    
    if (!mobileMenuToggle || !navbarContainer) return;

    // Create mobile navigation menu if it doesn't exist
    let mobileNav = document.querySelector('.mobile-nav');
    if (!mobileNav) {
        mobileNav = document.createElement('nav');
        mobileNav.className = 'mobile-nav';
        
        // Add links to mobile nav
        const signInBtn = document.querySelector('.sign-in-btn');
        if (signInBtn) {
            const signInLink = document.createElement('a');
            signInLink.href = signInBtn.href;
            signInLink.textContent = signInBtn.textContent;
            mobileNav.appendChild(signInLink);
        }
        
        // Add language selector
        const languageSelector = document.querySelector('.language-selector');
        if (languageSelector) {
            const langClone = languageSelector.cloneNode(true);
            mobileNav.appendChild(langClone);
        }
        
        document.body.appendChild(mobileNav);
    }

    // Toggle mobile menu
    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        mobileNav.classList.toggle('active');
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!mobileMenuToggle.contains(e.target) && !mobileNav.contains(e.target)) {
            mobileMenuToggle.classList.remove('active');
            mobileNav.classList.remove('active');
        }
    });
}

// ============================================
// 4. FAQ Accordion
// ============================================
function initFAQAccordion() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        const answerId = question.getAttribute('aria-controls');
        const answer = document.getElementById(answerId);
        
        if (!answer) return;

        // Set initial ARIA attributes
        answer.setAttribute('aria-hidden', 'true');
        question.setAttribute('aria-expanded', 'false');

        // Toggle answer on click
        question.addEventListener('click', () => {
            const isExpanded = question.getAttribute('aria-expanded') === 'true';
            
            // Close all other FAQ items
            faqQuestions.forEach(q => {
                if (q !== question) {
                    q.setAttribute('aria-expanded', 'false');
                    const otherAnswerId = q.getAttribute('aria-controls');
                    const otherAnswer = document.getElementById(otherAnswerId);
                    if (otherAnswer) {
                        otherAnswer.setAttribute('aria-hidden', 'true');
                    }
                }
            });

            // Toggle current item
            question.setAttribute('aria-expanded', !isExpanded);
            answer.setAttribute('aria-hidden', isExpanded);
        });

        // Keyboard navigation
        question.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                question.click();
            }
        });
    });
}

// ============================================
// 5. Email Form Validation
// ============================================
function initEmailForms() {
    const forms = document.querySelectorAll('.email-form');
    
    forms.forEach(form => {
        const emailInput = form.querySelector('input[type="email"]');
        const errorElement = form.querySelector('.form-error');
        
        if (!emailInput || !errorElement) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const email = emailInput.value.trim();
            const isValid = validateEmail(email);

            if (isValid) {
                // Form is valid - you can submit it here
                errorElement.textContent = '';
                
                // For demo purposes, just show a success message
                errorElement.textContent = 'Email submitted successfully!';
                errorElement.style.color = '#4CAF50';
                
                // Reset form after 2 seconds
                setTimeout(() => {
                    errorElement.textContent = '';
                    errorElement.style.color = '';
                    form.reset();
                }, 2000);
            } else {
                // Show error message
                errorElement.textContent = 'Please enter a valid email address.';
                errorElement.style.color = '#ff6b6b';
                emailInput.focus();
            }
        });

        // Clear error on input
        emailInput.addEventListener('input', () => {
            errorElement.textContent = '';
            errorElement.style.color = '';
        });
    });
}

// Email validation helper
function validateEmail(email) {
    // Basic email validation regex
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// ============================================
// 6. Smooth Scrolling
// ============================================
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Calculate position accounting for fixed navbar
                const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 0;
                const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Focus the target element for accessibility
                targetElement.setAttribute('tabindex', '-1');
                targetElement.focus();
            }
        });
    });
}

// ============================================
// 7. Background Video Fallback
// ============================================
function initBackgroundVideoFallback() {
    const backgroundVideo = document.querySelector('.background-video');
    const backgroundFallback = document.querySelector('.background-fallback');
    
    if (!backgroundVideo || !backgroundFallback) return;

    // Check if video can play
    backgroundVideo.addEventListener('error', () => {
        backgroundFallback.style.display = 'block';
    });

    // Also check if video is not supported
    if (!backgroundVideo.canPlayType) {
        backgroundFallback.style.display = 'block';
    }

    // Hide fallback if video starts playing
    backgroundVideo.addEventListener('play', () => {
        backgroundFallback.style.display = 'none';
    });
}

// ============================================
// 8. Utility Functions
// ============================================

// Debounce function for performance
function debounce(func, wait) {
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

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ============================================
// 9. Keyboard Navigation Enhancements
// ============================================

// Add keyboard support for mobile menu
function initKeyboardNavigation() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    
    if (!mobileMenuToggle || !mobileNav) return;

    // Close menu with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            mobileMenuToggle.classList.remove('active');
            mobileNav.classList.remove('active');
            mobileMenuToggle.focus();
        }
    });

    // Trap focus in mobile menu
    mobileNav.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            const firstFocusable = mobileNav.querySelector('a, button, input, select');
            const lastFocusable = mobileNav.querySelectorAll('a, button, input, select')[mobileNav.querySelectorAll('a, button, input, select').length - 1];
            
            if (e.shiftKey && document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
}

// Initialize keyboard navigation
document.addEventListener('DOMContentLoaded', initKeyboardNavigation);

// ============================================
// 10. Lazy Loading Images
// ============================================

// Add lazy loading to all images
function initLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);

// ============================================
// Console Easter Egg
// ============================================
console.log('%c StreamFlix ', 'background: #E50914; color: #FFFFFF; font-size: 20px; padding: 10px;');
console.log('%c Welcome to the Netflix-inspired landing page! ', 'color: #737373; font-size: 14px;');
