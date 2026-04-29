document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.premium-nav');

    // ──── Navbar scroll effect ────
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ──── Search Overlay ────
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.getElementById('searchInput');
    const searchSuggestions = document.getElementById('searchSuggestions');
    const searchHint = document.getElementById('searchHint');
    const searchForm = document.getElementById('searchForm');

    let debounceTimer = null;
    let activeIndex = -1;

    function openSearch() {
        if (!searchOverlay) return;
        searchOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        setTimeout(() => searchInput.focus(), 200);
    }

    function closeSearch() {
        if (!searchOverlay) return;
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
        searchInput.value = '';
        searchSuggestions.innerHTML = '';
        searchHint.style.display = '';
        activeIndex = -1;
    }

    if (searchToggle) searchToggle.addEventListener('click', openSearch);
    if (searchClose) searchClose.addEventListener('click', closeSearch);

    // Close on Escape or clicking outside
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchOverlay && searchOverlay.classList.contains('active')) {
            closeSearch();
        }
    });

    if (searchOverlay) {
        searchOverlay.addEventListener('click', (e) => {
            if (e.target === searchOverlay || e.target.classList.contains('search-overlay-inner')) {
                closeSearch();
            }
        });
    }

    // ──── Live Search Suggestions ────
    function highlightMatch(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    function renderSuggestions(results, query) {
        activeIndex = -1;

        if (results.length === 0 && query.length >= 2) {
            searchSuggestions.innerHTML = `
                <div class="search-no-results">
                    <i class="fa-regular fa-face-meh"></i>
                    <p>No dishes found for "${query}"</p>
                </div>`;
            searchHint.style.display = 'none';
            return;
        }

        if (results.length === 0) {
            searchSuggestions.innerHTML = '';
            searchHint.style.display = '';
            return;
        }

        searchHint.style.display = 'none';
        searchSuggestions.innerHTML = results.map((item, i) => `
            <a href="/details/${item.id}" class="search-suggestion-item" data-index="${i}">
                ${item.img ? `<img src="${item.img}" alt="${item.title}" class="search-suggestion-img">` : ''}
                <div class="search-suggestion-info">
                    <p class="search-suggestion-title">${highlightMatch(item.title, query)}</p>
                    <p class="search-suggestion-price">£${item.price}</p>
                </div>
                <i class="fa-solid fa-arrow-right search-suggestion-arrow"></i>
            </a>
        `).join('');
    }

    function fetchSuggestions(query) {
        if (query.length < 2) {
            renderSuggestions([], query);
            return;
        }

        fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                renderSuggestions(data.results || [], query);
            })
            .catch(() => {
                searchSuggestions.innerHTML = '';
            });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => fetchSuggestions(query), 250);
        });

        // Keyboard navigation inside suggestions
        searchInput.addEventListener('keydown', (e) => {
            const items = searchSuggestions.querySelectorAll('.search-suggestion-item');
            if (!items.length) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                activeIndex = Math.min(activeIndex + 1, items.length - 1);
                updateActive(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                activeIndex = Math.max(activeIndex - 1, -1);
                updateActive(items);
            } else if (e.key === 'Enter' && activeIndex >= 0) {
                e.preventDefault();
                items[activeIndex].click();
            }
        });
    }

    function updateActive(items) {
        items.forEach((el, i) => {
            el.classList.toggle('active', i === activeIndex);
            if (i === activeIndex) {
                el.scrollIntoView({ block: 'nearest' });
            }
        });
    }

    // ──── Add to Cart: prevent parent link navigation ────
    const addCartForms = document.querySelectorAll('.add-cart-form');
    addCartForms.forEach(form => {
        form.addEventListener('click', (e) => e.stopPropagation());
        const parentLink = form.closest('a');
        if (parentLink) {
            form.querySelector('button').addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                form.submit();
            });
        }
    });

    // ──── Auto-dismiss messages after 5 seconds ────
    const alerts = document.querySelectorAll('.messages-container .alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
