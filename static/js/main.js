/**
 * Django E-Commerce Main JavaScript
 * Handles UI interactions and functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initScrollToTop();
    initNavbarScroll();
    initTooltips();
    initAutoHideAlerts();
    initQuantityInputs();
});

/**
 * Scroll to Top Button
 */
function initScrollToTop() {
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    
    if (scrollTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollTopBtn.style.display = 'flex';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });
        
        // Scroll to top when clicked
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Navbar Scroll Effect
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                navbar.classList.add('shadow-sm');
            } else {
                navbar.classList.remove('shadow-sm');
            }
        });
    }
}

/**
 * Initialize Bootstrap Tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Auto-hide Alerts
 */
function initAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Auto-hide after 5 seconds
    });
}

/**
 * Quantity Input Validation
 */
function initQuantityInputs() {
    const quantityInputs = document.querySelectorAll('input[type="number"][name="quantity"]');
    
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const min = parseInt(this.getAttribute('min')) || 1;
            const max = parseInt(this.getAttribute('max')) || 999;
            let value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });
}

/**
 * Add to Cart Animation
 */
function animateAddToCart(button) {
    button.classList.add('btn-success');
    button.innerHTML = '<i class="bi bi-check me-2"></i>Added!';
    
    setTimeout(function() {
        button.classList.remove('btn-success');
        button.innerHTML = '<i class="bi bi-cart-plus me-2"></i>Add to Cart';
    }, 1500);
}

/**
 * Confirm Delete
 */
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

/**
 * Format Currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Debounce Function
 */
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

/**
 * AJAX Search for Products
 */
function initAjaxSearch() {
    const searchInput = document.getElementById('ajax-search');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        const debouncedSearch = debounce(function() {
            const query = searchInput.value.trim();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            fetch(`/search/ajax/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    displaySearchResults(data.products, searchResults);
                })
                .catch(error => console.error('Error:', error));
        }, 300);
        
        searchInput.addEventListener('input', debouncedSearch);
    }
}

/**
 * Display Search Results
 */
function displaySearchResults(products, container) {
    if (products.length === 0) {
        container.innerHTML = '<div class="p-3 text-muted">No products found</div>';
    } else {
        container.innerHTML = products.map(product => `
            <a href="/shop/${product.id}/${product.slug}/" class="d-flex align-items-center p-3 text-decoration-none border-bottom">
                ${product.image ? `<img src="${product.image}" alt="${product.name}" class="me-3" width="50" height="50" style="object-fit: cover;">` : ''}
                <div>
                    <h6 class="mb-0">${product.name}</h6>
                    <small class="text-primary">$${product.price}</small>
                </div>
            </a>
        `).join('');
    }
    container.style.display = 'block';
}

/**
 * Image Lazy Loading
 */
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
});

/**
 * Smooth Scroll for Anchor Links
 */
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

/**
 * Form Validation Enhancement
 */
document.addEventListener('submit', function(e) {
    const form = e.target;
    
    if (form.classList.contains('needs-validation')) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    }
});

/**
 * Rating Stars Interactive
 */
function initRatingStars() {
    const ratingContainers = document.querySelectorAll('.rating-interactive');
    
    ratingContainers.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const input = container.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const rating = index + 1;
                input.value = rating;
                updateStarDisplay(stars, rating);
            });
            
            star.addEventListener('mouseenter', () => {
                updateStarDisplay(stars, index + 1);
            });
        });
        
        container.addEventListener('mouseleave', () => {
            updateStarDisplay(stars, input.value);
        });
    });
}

/**
 * Update Star Display
 */
function updateStarDisplay(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

/**
 * Copy to Clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    } else {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Copied to clipboard!');
    }
}

/**
 * Show Toast Notification
 */
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    document.getElementById('toast-container').insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Export functions for global access
window.animateAddToCart = animateAddToCart;
window.confirmDelete = confirmDelete;
window.formatCurrency = formatCurrency;
window.copyToClipboard = copyToClipboard;
window.showToast = showToast;
