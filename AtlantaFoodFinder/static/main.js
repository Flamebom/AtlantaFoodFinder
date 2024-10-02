// Initialize and add the map
let map;
let currentRestaurantName = null;  // Global variable to store the current restaurant name

console.log('main.js is loaded');

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // Creates map centered around GT
  map = new Map(document.getElementById("map"), {
    zoom: 15,
    center: { lat: 33.7749, lng: 84.3964 },
    mapId: "YOUR_MAP_ID",
  });

  // Checks if user has enabled location services
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        }
        const marker = new AdvancedMarkerElement({
          map: map,
          position: pos,
        })
        map.setCenter(pos);
      }
    );
  }
}

// Creates map
initMap();

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector('.search-input');
  const searchCategory = document.getElementById('search-category');
  const searchButton = document.querySelector('.button');

  searchButton.addEventListener('click', function () {
    const distanceSlider = document.getElementById('distance-slider');
    const ratingSlider = document.getElementById('rating-slider');

    let distance = distanceSlider.value;
    let ratings = ratingSlider.value;

    distanceSlider.addEventListener('input', function () {
      distance = this.value; // Update the distance value
      console.log(`Selected distance: ${distance} miles`);
    });

    ratingSlider.addEventListener('input', function () {
      ratings = this.value; // Update the ratings value
      console.log(`Selected minimum rating: ${ratings}`);
    });

    const selectedCategory = searchCategory.value;
    const searchTerm = searchInput.value;

    clearAllPropertyCards() // Clear existing Cards

    // Logic for handling the search based on the selected category
    console.log(`Searching for ${searchTerm} in category: ${selectedCategory}`);

    // Add search logic here...

    function parseRestaurantStr(restaurantStr) {
      const result = {};

      const reviewsIndex = restaurantStr.indexOf('reviews :');
      let dataPart;
      let reviewsPart;

      if (reviewsIndex !== -1) {
        dataPart = restaurantStr.substring(0, reviewsIndex).trim();
        reviewsPart = restaurantStr.substring(reviewsIndex + 'reviews :'.length).trim();
      } else {
        dataPart = restaurantStr.trim();
      }

      // Parse the dataPart line by line
      const lines = dataPart.split('\n');
      for (const line of lines) {
        const colonIndex = line.indexOf(':');
        if (colonIndex !== -1) {
          const key = line.substring(0, colonIndex).trim();
          const value = line.substring(colonIndex + 1).trim();
          result[key] = value;
        }
      }

      // Set the reviews field
      if (reviewsPart) {
        result['reviews'] = reviewsPart;
      }

      return result;
    }

    console.log(distance),
      console.log(ratings),

      fetch('http://127.0.0.1:5000/search-restaurants', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },

        body: JSON.stringify({
          latitude: 33.749, // Replace with actual data
          longitude: -84.388, // Replace with actual data
          name_or_cuisine: searchTerm, // Use the search term
          distance: distance,
          ratings: ratings
        })
      })
        .then(response => response.json())
        .then(data => {
          console.log('Response from Flask:', data);

          if (data) {
            Object.keys(data).forEach(key => {
              const restaurantStr = data[key];
              console.log('Restaurant String:', restaurantStr);

              // Parse the restaurant string to extract information
              const restaurant = parseRestaurantStr(restaurantStr);

              // Handle the restaurant image (if available)
              let restaurantImage = 'img/placeholder.png'; // Default placeholder image
              if (restaurant.photoUri) {
                restaurantImage = restaurant.photoUri;
              }

              // Construct propertyDetails object
              const propertyDetails = {
                image1: restaurantImage,
                image2: restaurantImage,
                heartIcon1: 'img/sky-blue.svg',
                heartIcon2: 'img/Vector.svg',
                name: restaurant.name || 'Unknown',
                rating: restaurant.rating || 'N/A',
                starImage: 'img/star-2.svg',
                distance: '2.3 miles away', // Placeholder distance
                address: restaurant.address || 'Address not available',
                info: `${restaurant.cuisine || 'Restaurant'} | Open`,
                phoneNumber: restaurant['phone number'] || 'Not Available'
              };

              // Parse the reviews
              var reviews = [];
              if (restaurant.reviews) {
                try {
                  // Prepare the reviews string
                  let reviewsStr = restaurant.reviews.trim();

                  // Replace Python None, True, False with JavaScript null, true, false
                  reviewsStr = reviewsStr.replace(/\bNone\b/g, 'null')
                    .replace(/\bTrue\b/g, 'true')
                    .replace(/\bFalse\b/g, 'false');

                  // Replace single quotes with double quotes, but carefully
                  reviewsStr = reviewsStr.replace(/'/g, '"');

                  // Now, we can attempt to parse it as JSON
                  const reviewsData = JSON.parse(reviewsStr);

                  reviews = reviewsData.map(review => ({
                    title: review.authorAttribution.displayName || 'Anonymous',
                    rating: review.rating.toString(),
                    date: new Date(review.publishTime).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    }),
                    text: review.text?.text || 'No review text available.',
                    starImage: 'img/star-2.svg',
                    reviewerImage: review.authorAttribution.photoUri || 'img/default-user.png'
                  }));
                } catch (e) {
                  console.error('Failed to parse reviews for restaurant:', restaurant.name);
                  console.error('Reviews String:', restaurant.reviews);
                  console.error('Parsing Error:', e);
                }
              }

              // Call the createPropertyCard function
              createPropertyCard(
                restaurantImage,                             // Image source for the restaurant
                restaurant.name || 'Unknown',                // Restaurant name
                restaurant.rating || 'N/A',                  // Rating
                '2.3 miles away',                            // Distance (placeholder)
                '',                                    // Price range (placeholder)
                restaurant.cuisine || 'Restaurant',          // Restaurant type
                'Open',                                      // Status (adjust if available)
                restaurant.address || 'Address not available', // Address
                propertyDetails,                             // Property details for description card
                reviews                                      // Reviews for description card
              );
            });
          }
        })
        .catch(error => {
          console.error('Error fetching or processing data:', error);
        });

  });

});

document.addEventListener("DOMContentLoaded", function () {
  const folderIcon = document.querySelector('.selection-card2');
  let isFavorite = false;  // Track if the Big Card is in Favorite
  const folderContainer = document.querySelector('.selection-card'); // Where favorite folder is shown
  console.log('DOM fully loaded');

  // Add event listener to the Folder icon to directly add or remove BigCard to/from "Favorite"
  if (folderIcon) {
    folderIcon.addEventListener('click', function () {
      console.log("Current Restaurant Name:", currentRestaurantName);  // Ensure we have the right name

      if (currentRestaurantName && !isFavorite) {
        addBigCardToFavorite(currentRestaurantName);  // Add to Favorite
        updateFavoriteText("Delete from Favorite");
      } else if (currentRestaurantName) {
        removeBigCardFromFavorite(currentRestaurantName);  // Remove from Favorite
        updateFavoriteText("Favorite");
      }

      isFavorite = !isFavorite;  // Toggle favorite status
    });
  } else {
    console.log('Folder icon not found');
  }

  function addBigCardToFavorite(restaurantName) {
    console.log(`Adding ${restaurantName} to favorites...`);

    fetch(`/favorite/${restaurantName}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log('Added to favorites:', data);
      })
      .catch(error => {
        console.error('Error adding to favorites:', error);
      });
  }

  function removeBigCardFromFavorite(restaurantName) {
    fetch(`/remove_favorite/${restaurantName}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log('Removed from favorites:', data);
      })
      .catch(error => {
        console.error('Error removing from favorites:', error);
      });
  }

  function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function updateFavoriteText(text) {
    const favoriteText = document.querySelector('.selection-card2 .type');
    if (favoriteText) {
      favoriteText.textContent = text;
    }
  }

  // Render only the "Favorite" folder in the folder container
  function renderFavoriteFolder() {
    console.log('Rendering favorite folder');

    // Clear any previous rendered folders
    document.querySelectorAll('.folder-item').forEach(item => item.remove());

    // Render "Favorite" folder if not already rendered
    if (!document.querySelector('.favoriteframe-rendered')) {
      console.log('Rendering new Favorite folder');
      const favoriteFolderHTML = `
        <div class="favoriteframe favoriteframe-rendered" data-folder="Favorite">
          <div class="type">Favorite</div>
          <img class="generalline" src="img/generalline.svg" />
          <img class="vector" src="img/vector.svg" />
        </div>
      `;

      // Insert "Favorite" into the folderContainer
      folderContainer.insertAdjacentHTML('afterbegin', favoriteFolderHTML);

      // Check if Favorite element is present
      const favoriteElement = document.querySelector('.favoriteframe');
      if (favoriteElement) {
        console.log('Favorite folder element found, adding click event listener');
        favoriteElement.addEventListener('click', function () {
          const folderName = favoriteElement.getAttribute('data-folder');
          console.log(`Favorite folder clicked: ${folderName}`);
          loadFavoriteData(folderName);
        });
      } else {
        console.log('Favorite folder element not found after rendering');
      }
    }
  }

  // Function to load "Favorite" folder data
  function loadFavoriteData(folderName) {
    if (folderName === 'Favorite') {
      console.log(`Loading data for folder: ${folderName}`);
      clearAllPropertyCards() // Clear existing Cards

      fetch('http://127.0.0.1:8000/favorites/')
        .then(response => {
          console.log('Fetch response received. Status:', response.status);
          return response.json();
        })
        .then(data => {
          console.log('Fetched data:', data);
          const favorites = data.favorites;
          if (favorites.length === 0) {
            console.log('No favorite items found');
          } else {
            console.log('Favorite items array:', favorites);
            favorites.forEach(favorite => {
              // Remove everything before and including 'favorited'
              const cleanedFavorite = favorite.replace(/.*favorited\s*/, '');
              console.log('Cleaned favorite item:', cleanedFavorite);
              // Now you can display the cleanedFavorite in the UI as needed
            });
          }
        })
        .catch(error => {
          console.error('Error loading favorites:', error);
        });
    } else {
      console.log('Folder is not Favorite. Skipping data load.');
    }
  }


  // Expose current Big Card data setter globally
  window.setCurrentBigCardData = function (bigCardData) {
    currentBigCardData = bigCardData;
    // Reset the state of the button when a new Big Card is opened
    isFavorite = false;
    updateFavoriteText("Favorite");
  };





  // Initial render to show only "Favorite" folder
  renderFavoriteFolder();
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
  const distance = this.value;
  // Change background gradient to fill the bar based on the slider value
  const percentage = (this.value - this.min) / (this.max - this.min) * 100;
  this.style.background = `linear-gradient(to right, #000000 ${percentage}%, #d9d9d980 ${percentage}%)`;
});



// Rating slider functionality
const ratingSlider = document.getElementById('rating-slider');
const ratingValue = document.getElementById('rating-value');

ratingSlider.addEventListener('input', function () {
  ratingValue.textContent = `${this.value} Stars`;
  const ratings = this.value

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
    accountElement.href = "login.html";  // Redirect to login page
  }
}

// Initialize the account status on page load
updateAccountStatus();


function clearAllPropertyCards() {
  const propertyCards = document.querySelectorAll('.property-card-big');
  propertyCards.forEach(card => card.remove());  // Remove each card from the DOM
}



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
    // Update the global variable when this card is clicked
    currentRestaurantName = restaurantName;  // Update global variable with the clicked restaurant name
    console.log('Current Restaurant Name:', currentRestaurantName);  // Debugging to ensure it's updated

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

  // Add "Go Back" button at the top left
  const goBackBtn = document.createElement('div');
  goBackBtn.classList.add('BigCard-go-back');
  goBackBtn.innerText = "Go Back";
  bigCardMain.appendChild(goBackBtn);

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

  iconHeart.appendChild(heartImg1);
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

  // Add event listener to "Go Back" button to hide the BigCard
  goBackBtn.addEventListener('click', function () {
    // Hide the BigCard when "Go Back" is clicked
    bigCardMain.style.display = 'none';

    // Bring back the property-card-container by setting visibility to visible
    const container = document.querySelector('.property-card-container');
    container.style.visibility = 'visible'; // Set visibility back to visible
    console.log('Container visibility restored:', container.style.visibility);
  });

  let folderactive = false;

  heartImg1.addEventListener('click', function () {
    if (!folderactive) {  // When folder is not active
      console.log('folder clicked: ' + folderactive);
      document.querySelector('.selection-card2').style.display = 'flex'; // Show the selection card
      folderactive = true;  // Set folderactive to true
    } else {  // When folder is active
      console.log('folder clicked: ' + folderactive);
      document.querySelector('.selection-card2').style.display = 'none';  // Hide the selection card
      folderactive = false;  // Set folderactive to false
    }
  });
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
