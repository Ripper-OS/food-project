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

    // Inline Search Logic
    const searchContainer = document.querySelector('.search-container');
    const searchInput = document.getElementById('searchInputInline');
    const searchSubmit = document.querySelector('.search-submit-btn');

    if (searchContainer && searchInput && searchSubmit) {
        searchSubmit.addEventListener('click', (e) => {
            if (!searchContainer.classList.contains('active')) {
                e.preventDefault();
                searchContainer.classList.add('active');
                searchInput.focus();
            } else if (searchInput.value.trim() === '') {
                e.preventDefault();
                searchContainer.classList.remove('active');
            }
            // If active and has value, form submits naturally
        });

        // Close search on click outside
        document.addEventListener('click', (e) => {
            if (!searchContainer.contains(e.target) && searchContainer.classList.contains('active')) {
                searchContainer.classList.remove('active');
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && searchContainer.classList.contains('active')) {
                searchContainer.classList.remove('active');
                searchInput.blur();
            }
        });
    }

    // Auto-dismiss toast notifications after 4 seconds
    const toasts = document.querySelectorAll('.toast.show');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.classList.remove('show');
            toast.classList.add('hide');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    });
});
