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

    // Simple cart increment logic (demo)
    const addCartBtns = document.querySelectorAll('.btn-add-cart');
    const cartBadge = document.querySelector('.cart-badge');
    let cartCount = 0;

    addCartBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            cartCount++;
            cartBadge.textContent = cartCount;
            
            // Animation effect
            btn.innerHTML = '<i class="fa-solid fa-check"></i>';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-plus"></i>';
            }, 2000);
        });
    });
});
