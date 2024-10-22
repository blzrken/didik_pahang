document.addEventListener('DOMContentLoaded', function () {
    const carousels = [
        ...document.querySelectorAll('.package-card .carousel-container'),
        ...document.querySelectorAll('.carousel-container-horizontal'),
        ...document.querySelectorAll('.carousel-container-horizontal2')
    ];

    carousels.forEach((carousel) => {
        const images = carousel.querySelectorAll('.carousel-image');
        let currentImageIndex = 0;

        function showNextImage() {
            images[currentImageIndex].classList.remove('active');
            images[currentImageIndex].style.opacity = 0;
            
            currentImageIndex = (currentImageIndex + 1) % images.length;
            
            images[currentImageIndex].classList.add('active');
            setTimeout(() => {
                images[currentImageIndex].style.opacity = 1;
            }, 50); // Small delay to ensure the opacity transition is visible
        }

        // Start the carousel automatically
        setInterval(showNextImage, 5000); // Change image every 5 seconds
    });

    // Scroll Animation Script
    const packageCards = document.querySelectorAll('.package-card, .package-card-horizontal');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            }
        });
    });

    packageCards.forEach(card => {
        observer.observe(card);
    });
});
