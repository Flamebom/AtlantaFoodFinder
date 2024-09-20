// Search Query 
document.querySelector('.search-input').addEventListener('input', function () {
    console.log(this.value);  // Perform search-related functionality
});


// Filter On or OFF
document.querySelector('.ellipse').addEventListener('click', function () {
    // Toggle the 'active' class on click
    this.classList.toggle('active');
});

