const slider = document.querySelector('.package-slider');
const nextButton = document.querySelector('.next');
const prevButton = document.querySelector('.prev');
const packages = document.querySelectorAll('.package');
const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');

// Expand the search bar when clicking the search button
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
nextButton.addEventListener('click', () => {
    if (currentIndex < packages.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;  // Reset to the first package for the loop
    }
    updateSliderPosition();
});

// Event listener for previous button
prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = packages.length - 1;  // Loop to the last package
    }
    updateSliderPosition();
});

// Set initial position on load
updateSliderPosition();
