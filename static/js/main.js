document.addEventListener('DOMContentLoaded', () => {
    // Mobile navigation toggle
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            if (navMenu.classList.contains('active')) {
                menuToggle.innerHTML = '&times;';
            } else {
                menuToggle.innerHTML = '&#9776;';
            }
        });

        // Close menu on link click for mobile screens
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                if (menuToggle) {
                    menuToggle.innerHTML = '&#9776;';
                }
            });
        });
    }

    // Smooth scroll for internal anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId.length > 1) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});