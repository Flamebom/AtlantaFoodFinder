//modify this later
// Initialize the Google Map with default center (can be overridden by user's location if geolocation is enabled)
function initMap() {
    // Default map center
    var defaultCenter = {lat: 37.7749, lng: -122.4194};  // San Francisco example
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: defaultCenter
    });

    // Use the `restaurants` variable that has been passed from the template
    restaurants.forEach(function(restaurant) {
        var marker = new google.maps.Marker({
            position: {lat: parseFloat(restaurant.latitude), lng: parseFloat(restaurant.longitude)},
            map: map,
            title: restaurant.name
        });

        // Create info window content for each restaurant
        var infoWindow = new google.maps.InfoWindow({
            content: `<div>
                        <h3>${restaurant.name}</h3>
                        <p>Cuisine: ${restaurant.cuisine_type}</p>
                        <p>Location: ${restaurant.location}</p>
                        <p>Rating: ${restaurant.rating}</p>
                        <p>Distance: ${restaurant.distance} km</p>
                      </div>`
        });

        // Show info window on marker click
        marker.addListener('click', function() {
            infoWindow.open(map, marker);
        });
    });

    // Optionally, attempt to get the user's geolocation for more accurate distance calculations
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var userLat = position.coords.latitude;
            var userLng = position.coords.longitude;

            // Update map center to user's location
            var userLocation = new google.maps.LatLng(userLat, userLng);
            map.setCenter(userLocation);

            // You can pass the user's lat/lng to the server to calculate distances
            console.log("User's Location: ", userLat, userLng);
        }, function(error) {
            console.log("Geolocation failed: ", error);
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}
