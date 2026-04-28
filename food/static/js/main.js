document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.premium-nav');

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // --- Search Bar Toggle ---
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.getElementById('searchInput');

    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', (e) => {
            e.preventDefault();
            searchOverlay.classList.add('active');
            setTimeout(() => searchInput.focus(), 300);
        });

        searchClose.addEventListener('click', () => {
            searchOverlay.classList.remove('active');
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
                searchOverlay.classList.remove('active');
            }
        });
    }

    // --- Add to Cart: prevent parent link navigation ---
    const addCartForms = document.querySelectorAll('.add-cart-form');
    addCartForms.forEach(form => {
        form.addEventListener('click', (e) => {
            e.stopPropagation();
        });
        // Also prevent the parent <a> from navigating
        const parentLink = form.closest('a');
        if (parentLink) {
            form.querySelector('button').addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                form.submit();
            });
        }
    });

    // --- Auto-dismiss messages after 5 seconds ---
    const alerts = document.querySelectorAll('.messages-container .alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
