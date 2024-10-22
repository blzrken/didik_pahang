document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.package-slider');
    const nextButton = document.querySelector('.next');
    const prevButton = document.querySelector('.prev');
    const packages = document.querySelectorAll('.package');
    const searchBtn = document.getElementById('search-btn');
    const searchInput = document.getElementById('search-input');

    // Expand the search bar when clicking the search button
    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', () => {
            if (searchInput.style.width === '100px') {
                searchBtn.style.width = '100px';
                searchInput.style.width = '0';
                searchInput.style.opacity = '0';
            } else {
                searchInput.style.width = '100px';
                searchInput.style.opacity = '1';
                searchInput.focus(); // Focus on input when expanded
            }
        });
    }

    let currentIndex = 0;

    // Function to update the slider position and apply active class to the center package
    const updateSliderPosition = () => {
        slider.style.transform = `translateX(-${currentIndex * 270}px)`;

        // Remove 'active' class from all packages
        packages.forEach((pkg, index) => {
            pkg.classList.remove('active');
        });

        // Add 'active' class to the center package
        if (packages[currentIndex]) {
            packages[currentIndex].classList.add('active');
        }
    };

    // Event listener for next button
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (currentIndex < packages.length - 1) {
                currentIndex++;
            } else {
                currentIndex = 0;  // Reset to the first package for the loop
            }
            updateSliderPosition();
        });
    }

    // Event listener for previous button
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
            } else {
                currentIndex = packages.length - 1;  // Loop to the last package
            }
            updateSliderPosition();
        });
    }

    // Set initial position on load
    if (slider) {
        updateSliderPosition();
    }

    window.addEventListener('scroll', function () {
        var footer = document.querySelector('.contact-footer');
        if (footer) {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
                footer.classList.add('footer-visible');
            } else {
                footer.classList.remove('footer-visible');
            }
        }
    });
});

const modal = document.getElementById("modal");
        const modalImg = document.getElementById("modal-img");
    
        // Get all gallery images
        const images = document.querySelectorAll(".gallery-item img");
    
        // Open the modal on image click
        images.forEach(image => {
            image.addEventListener("click", () => {
                modal.style.display = "flex";
                modalImg.src = image.src; // Set the modal image to the clicked image
            });
        });
    
        // Close the modal when the 'x' is clicked
        const closeModal = document.querySelector(".close");
        closeModal.onclick = () => {
            modal.style.display = "none";
        };

