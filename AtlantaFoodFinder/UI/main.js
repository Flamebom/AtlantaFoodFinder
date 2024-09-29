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







function createPropertyCard(imageSrc, restaurantName, rating, distance, priceRange, restaurantType, status, address, propertyDetails, reviews) {
  // Remove the 'No restaurants found' message if it exists
  const message = document.getElementById('no-restaurants-message');
  if (message) {
    message.remove();  // Remove the message
  }

  // Create the main property card div with class 'property-card-big'
  const propertyCard = document.createElement('div');
  propertyCard.className = 'property-card-big';

  // Add property details as data attributes to the card
  propertyCard.setAttribute('data-property-details', JSON.stringify(propertyDetails));
  propertyCard.setAttribute('data-reviews', JSON.stringify(reviews));

  // Set the inner HTML structure of the property card
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

  // Event listener to show description card
  propertyCard.addEventListener('click', function () {
    console.log('Property card clicked!');
    const propertyDetails = JSON.parse(this.getAttribute('data-property-details'));
    const reviews = JSON.parse(this.getAttribute('data-reviews'));

    const container = document.querySelector('.property-card-container');
    console.log('Container display before:', container.style.display);

    // Hide the property card container
    container.style.visibility = 'hidden';


    console.log('Container display after:', container.style.display);
    // Create and display the description card
    createBigCard(propertyDetails, reviews);
  });

  // Append the property card to the container
  document.querySelector('.property-card-container').appendChild(propertyCard);
}

function createBigCard(propertyDetails, reviews) {
  // Create the main container for the big card
  const bigCardMain = document.createElement('div');
  bigCardMain.classList.add('BigCard-main');

  // Frame container for the images
  const frame = document.createElement('div');
  frame.classList.add('BigCard-frame');

  const img1 = document.createElement('img');
  img1.classList.add('BigCard-rectangle');
  img1.src = propertyDetails.image1;

  const img2 = document.createElement('img');
  img2.classList.add('BigCard-rectangle');
  img2.src = propertyDetails.image2;

  frame.appendChild(img1);
  frame.appendChild(img2);
  bigCardMain.appendChild(frame);

  // Overlap group for rating and address
  const overlapGroup = document.createElement('div');
  overlapGroup.classList.add('BigCard-overlap-group');

  const iconHeart = document.createElement('div');
  iconHeart.classList.add('BigCard-icon-heart');

  const heartImg1 = document.createElement('img');
  heartImg1.classList.add('BigCard-sky-blue');
  heartImg1.src = propertyDetails.heartIcon1;

  const heartImg2 = document.createElement('img');
  heartImg2.classList.add('BigCard-vector');
  heartImg2.src = propertyDetails.heartIcon2;

  iconHeart.appendChild(heartImg1);
  iconHeart.appendChild(heartImg2);
  overlapGroup.appendChild(iconHeart);

  const frame2 = document.createElement('div');
  frame2.classList.add('BigCard-frame-2');

  const driverName = document.createElement('div');
  driverName.classList.add('BigCard-driver-name');
  driverName.innerText = propertyDetails.name;

  const frame3 = document.createElement('div');
  frame3.classList.add('BigCard-frame-3');

  const frame4 = document.createElement('div');
  frame4.classList.add('BigCard-frame-4');

  const starGroup = document.createElement('div');
  starGroup.classList.add('BigCard-group');

  const starImg = document.createElement('img');
  starImg.classList.add('BigCard-star');
  starImg.src = propertyDetails.starImage;

  const ratingText = document.createElement('div');
  ratingText.classList.add('BigCard-text');
  ratingText.innerText = propertyDetails.rating;

  starGroup.appendChild(starImg);
  frame4.appendChild(starGroup);
  frame4.appendChild(ratingText);
  frame3.appendChild(frame4);

  const milesAway = document.createElement('div');
  milesAway.classList.add('BigCard-text-wrapper');
  milesAway.innerText = propertyDetails.distance;

  const address = document.createElement('p');
  address.classList.add('BigCard-text-wrapper-2');
  address.innerText = propertyDetails.address;

  frame3.appendChild(milesAway);
  frame3.appendChild(address);
  frame2.appendChild(driverName);
  frame2.appendChild(frame3);

  const divWrapper = document.createElement('div');
  divWrapper.classList.add('BigCard-div-wrapper');
  const restaurantInfo = document.createElement('div');
  restaurantInfo.classList.add('BigCard-text-wrapper-2');
  restaurantInfo.innerText = propertyDetails.info;
  divWrapper.appendChild(restaurantInfo);
  frame2.appendChild(divWrapper);

  const frame5 = document.createElement('div');
  frame5.classList.add('BigCard-frame-5');
  const phoneNumber = document.createElement('div');
  phoneNumber.classList.add('BigCard-text-wrapper-2');
  phoneNumber.innerText = propertyDetails.phoneNumber;
  frame5.appendChild(phoneNumber);
  frame2.appendChild(frame5);

  overlapGroup.appendChild(frame2);

  const lineImg = document.createElement('img');
  lineImg.classList.add('BigCard-line');
  lineImg.src = 'img/line1.svg';
  overlapGroup.appendChild(lineImg);

  bigCardMain.appendChild(overlapGroup);

  // Create the reviews section
  const frame666 = document.createElement('div');
  frame666.classList.add('BigCard-frame-666');

  reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.classList.add('BigCard-property-card-big');

    const reviewFrame7 = document.createElement('div');
    reviewFrame7.classList.add('BigCard-frame-7');

    const reviewTitle = document.createElement('div');
    reviewTitle.classList.add('BigCard-driver-name-2');
    reviewTitle.innerText = review.title;

    const reviewFrame8 = document.createElement('div');
    reviewFrame8.classList.add('BigCard-frame-8');

    const reviewFrame4 = document.createElement('div');
    reviewFrame4.classList.add('BigCard-frame-4');

    const reviewStarWrapper = document.createElement('div');
    reviewStarWrapper.classList.add('BigCard-star-wrapper');

    const reviewStarImg = document.createElement('img');
    reviewStarImg.classList.add('BigCard-img');
    reviewStarImg.src = review.starImage;

    const reviewRating = document.createElement('div');
    reviewRating.classList.add('BigCard-text-2');
    reviewRating.innerText = review.rating;

    reviewStarWrapper.appendChild(reviewStarImg);
    reviewFrame4.appendChild(reviewStarWrapper);
    reviewFrame4.appendChild(reviewRating);

    const reviewDate = document.createElement('div');
    reviewDate.classList.add('BigCard-text-3');
    reviewDate.innerText = `Posted on: ${review.date}`;

    reviewFrame8.appendChild(reviewFrame4);
    reviewFrame8.appendChild(reviewDate);

    reviewFrame7.appendChild(reviewTitle);
    reviewFrame7.appendChild(reviewFrame8);

    const reviewText = document.createElement('div');
    reviewText.classList.add('BigCard-driver-name-3');
    reviewText.innerHTML = `Review:<br>${review.text}`;

    reviewFrame7.appendChild(reviewText);
    reviewCard.appendChild(reviewFrame7);

    frame666.appendChild(reviewCard);
  });

  bigCardMain.appendChild(frame666);

  // Append to the 'main-page' element
  const list = document.querySelector('.div');
  if (list) {
    list.appendChild(bigCardMain);
  } else {
    console.error('Error: Main page container not found!');
  }

  document.addEventListener('click', function (event) {
    const isClickInside = card.contains(event.target);
    if (!isClickInside) {
      // Hide the description card and show property cards again
      bigCardMain.remove();
      document.querySelector('.property-card-container').style.display = 'block';
    }
  }, { once: true }); // Event listener will run only once
}


// Example of usage
const propertyDetails = {
  image1: 'img/rectangle-12-2.png',
  image2: 'img/rectangle-12-2.png',
  heartIcon1: 'img/sky-blue.svg',
  heartIcon2: 'img/Vector.svg',
  name: 'Clasic Studio Apartment',
  rating: '4.0',
  starImage: 'img/star-2.svg',
  distance: '2.3 miles away',
  address: '60 11th St NE, Atlanta, GA',
  info: '$30-50 | Spanish restaurant | Open',
  phoneNumber: '+1234567890'
};

const reviews = [
  {
    title: "Saltwood Charcuteri",
    rating: "4.0",
    date: "September 16th 2024",
    text: "This place was amazing! Great food and ambiance.",
    starImage: 'img/star-2.svg'
  },
  {
    title: "Saltwood Charcuteri",
    rating: "4.0",
    date: "August 4th 2023",
    text: "Lovely restaurant, would definitely come again.",
    starImage: 'img/star-2.svg'
  }
];


// Example call to dynamically add a new property card
createPropertyCard(
  'img/image-2.png',       // Image source
  'Saltwood Charcuteri',  // Restaurant name
  '4.0',                 // Rating
  '2.3 miles away',       // Distance
  '$30-50',              // Price range
  'Spanish restaurant',   // Restaurant type
  'Open',                // Status
  '60 11th St NE, Atlanta, GA', // Address
  propertyDetails,        // Property details for description card
  reviews                 // Reviews for description card
);

// Example call to dynamically add a new property card
createPropertyCard(
  'img/image-2.png',       // Image source
  'Saltwood Charcuteri',  // Restaurant name
  '4.0',                 // Rating
  '2.3 miles away',       // Distance
  '$30-50',              // Price range
  'Spanish restaurant',   // Restaurant type
  'Open',                // Status
  '60 11th St NE, Atlanta, GA', // Address
  propertyDetails,        // Property details for description card
  reviews                 // Reviews for description card
);
// Example call to dynamically add a new property card
createPropertyCard(
  'img/image-2.png',       // Image source
  'Saltwood Charcuteri',  // Restaurant name
  '4.0',                 // Rating
  '2.3 miles away',       // Distance
  '$30-50',              // Price range
  'Spanish restaurant',   // Restaurant type
  'Open',                // Status
  '60 11th St NE, Atlanta, GA', // Address
  propertyDetails,        // Property details for description card
  reviews                 // Reviews for description card
);






