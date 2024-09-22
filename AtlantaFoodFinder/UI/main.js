// Search Query 
document.querySelector('.search-input').addEventListener('input', function () {
  console.log(this.value);  // Perform search-related functionality
});


// Toggle the 'active' class and show/hide the slider
document.querySelector('.ellipse').addEventListener('click', function () {
  // Toggle the 'active' class on click
  this.classList.toggle('active');

  // Select the slider element and toggle its visibility
  const slider = document.querySelector('.secondary-menu'); // Assuming secondary-menu contains the sliders
  if (this.classList.contains('active')) {
    slider.style.display = 'flex';  // Use 'flex' to ensure correct alignment inside the box
  } else {
    slider.style.display = 'none';  // Hide the slider when not active
  }
});




// Distance slider functionality
const distanceSlider = document.getElementById('distance-slider');
const distanceValue = document.getElementById('distance-value');

distanceSlider.addEventListener('input', function () {
  distanceValue.textContent = `${this.value} Miles`;

  // Change background gradient to fill the bar based on the slider value
  const percentage = (this.value - this.min) / (this.max - this.min) * 100;
  this.style.background = `linear-gradient(to right, #000000 ${percentage}%, #d9d9d980 ${percentage}%)`;
});



// Rating slider functionality
const ratingSlider = document.getElementById('rating-slider');
const ratingValue = document.getElementById('rating-value');

ratingSlider.addEventListener('input', function () {
  ratingValue.textContent = `${this.value} Stars`;

  // Change background gradient to fill the bar based on the slider value
  const percentage = (this.value - this.min) / (this.max - this.min) * 100;
  this.style.background = `linear-gradient(to right, #000000 ${percentage}%, #d9d9d980 ${percentage}%)`;
});




let isLoggedIn = false;  // This should be updated based on actual login status
let userName = "JohnDoe";  // Placeholder for the user's name

function updateAccountStatus() {
  const accountElement = document.querySelector('.account');

  if (isLoggedIn) {
    accountElement.textContent = userName;
    accountElement.href = "/personal-account.html";  // Redirect to personal account page
  } else {
    accountElement.textContent = "Login";
    accountElement.href = "/login.html";  // Redirect to login page
  }
}

// Initialize the account status on page load
updateAccountStatus();













function createPropertyCard(imageSrc, restaurantName, rating, distance, priceRange, restaurantType, status, address) {
  // Remove the 'No restaurants found' message if it exists
  const message = document.getElementById('no-restaurants-message');
  if (message) {
    message.remove();  // Remove the message
  }

  // Create the main property card div with class 'property-card-big'
  const propertyCard = document.createElement('div');
  propertyCard.className = 'property-card-big';  // Use the original CSS class

  // Set the inner HTML structure of the property card to match your original layout
  propertyCard.innerHTML = `
        <img class="img" src="${imageSrc}" />
        <div class="frame-4">
          <div class="driver-name">${restaurantName}</div>
          <div class="frame-5">
            <div class="frame-6">
              <div class="star-wrapper"><img class="star" src="img/star-2.svg" /></div>
              <div class="text">${rating}</div>
            </div>
            <div class="text-2">${distance}</div>
          </div>
          <div class="div-wrapper">
            <div class="text-3">${priceRange} | ${restaurantType} | ${status}</div>
          </div>
          <div class="frame-7">
            <div class="group-wrapper">
              <div class="group-4">
                <div class="ellipse-2"></div>
                <div class="ellipse-3"></div>
              </div>
            </div>
            <p class="p">${address}</p>
          </div>
        </div>
    `;

  // Append the property card to the container
  document.querySelector('.property-card-container').appendChild(propertyCard);
}


// Example call to dynamically add a new property card
createPropertyCard(
  'img/image-2.png',       // Image source
  'Saltwood Charcuteri',  // Restaurant name
  '4.0',                 // Rating
  '2.3 miles away',       // Distance
  '$30-50',              // Price range
  'Spanish restaurant',   // Restaurant type
  'Open',                // Status
  '60 11th St NE, Atlanta, GA'  // Address
);

