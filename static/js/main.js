// ===========================
// ProInvest Main JavaScript
// ===========================

// Smooth Scroll to Sections
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            const element = document.querySelector(href);
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar Sticky Scroll Effect
let lastScrollTop = 0;
const navbar = document.querySelector('nav');

window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 100) {
        navbar.classList.add('shadow-lg');
    } else {
        navbar.classList.remove('shadow-lg');
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Animated Counter
class Counter {
    constructor(element) {
        this.element = element;
        this.target = parseInt(element.dataset.target) || 0;
        this.current = 0;
        this.duration = 2000;
        this.observed = false;
    }
    
    animate() {
        if (this.observed) return;
        this.observed = true;
        
        const increment = this.target / (this.duration / 16);
        const timer = setInterval(() => {
            this.current += increment;
            if (this.current >= this.target) {
                this.current = this.target;
                clearInterval(timer);
            }
            this.element.textContent = Math.floor(this.current).toLocaleString();
        }, 16);
    }
}

// Initialize counters on scroll
const initializeCounters = () => {
    const counterElements = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                new Counter(entry.target).animate();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    counterElements.forEach(el => observer.observe(el));
};

document.addEventListener('DOMContentLoaded', initializeCounters);

// Form Validation
const validateForm = (form) => {
    const fields = form.querySelectorAll('[required]');
    let isValid = true;
    
    fields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('border-red-500');
            isValid = false;
        } else {
            field.classList.remove('border-red-500');
        }
    });
    
    return isValid;
};

// Button Ripple Effect
document.querySelectorAll('button, [role="button"]').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        // Clean up old ripples
        this.querySelectorAll('.ripple').forEach(r => r.remove());
        this.appendChild(ripple);
    });
});

// Typing Animation
const typeWriter = (element, text, speed = 100) => {
    let index = 0;
    element.textContent = '';
    
    const type = () => {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        }
    };
    
    type();
};

// Parallax Effect
const initParallax = () => {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    window.addEventListener('scroll', () => {
        parallaxElements.forEach(element => {
            const speed = element.dataset.parallax || 0.5;
            const offset = window.pageYOffset;
            element.style.transform = `translateY(${offset * speed}px)`;
        });
    });
};

initParallax();

// Toast Notification
class Toast {
    static show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `fixed top-24 left-4 right-4 md:left-auto md:right-4 md:w-96 z-50 animate-fade-in-down`;
        
        const bgColor = {
            'success': 'from-green-600 to-emerald-600',
            'error': 'from-red-600 to-rose-600',
            'warning': 'from-yellow-600 to-orange-600',
            'info': 'from-blue-600 to-cyan-600'
        }[type] || 'from-blue-600 to-cyan-600';
        
        const icon = {
            'success': 'check-circle',
            'error': 'alert-circle',
            'warning': 'alert-triangle',
            'info': 'info'
        }[type] || 'info';
        
        toast.innerHTML = `
            <div class="px-6 py-4 rounded-lg bg-gradient-to-r ${bgColor} text-white shadow-lg flex items-center gap-3">
                <i data-lucide="${icon}" class="w-5 h-5"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        lucide.createIcons();
        
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease-out forwards';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// Lazy Loading Images
const initLazyLoad = () => {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
};

document.addEventListener('DOMContentLoaded', initLazyLoad);

// Floating Animation
const initFloatingAnimation = () => {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .particle {
            animation: float 6s ease-in-out infinite;
        }
    `;
    document.head.appendChild(style);
};

initFloatingAnimation();

// Dark Mode Support
const initDarkMode = () => {
    // Already in dark mode by default
    localStorage.setItem('theme', 'dark');
};

document.addEventListener('DOMContentLoaded', initDarkMode);

// Performance Optimization
const initPerformance = () => {
    if ('loading' in HTMLImageElement.prototype) {
        // Use native lazy loading
        document.querySelectorAll('img').forEach(img => {
            if (img.dataset.src) {
                img.loading = 'lazy';
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', initPerformance);

// Analytics Event Tracking
const trackEvent = (eventName, eventData = {}) => {
    console.log(`Event: ${eventName}`, eventData);
    // Add your analytics code here (e.g., Google Analytics)
};

// Track page views
trackEvent('page_view', { page: window.location.pathname });

// Export functions for use in HTML
window.Toast = Toast;
window.trackEvent = trackEvent;
window.validateForm = validateForm;
