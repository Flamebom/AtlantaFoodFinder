document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById('email');
    const requestButton = document.querySelector('.button');

    // Function to handle password reset request
    function handlePasswordReset() {
        const email = emailInput.value;

        if (email) {
            alert(`Password reset request for Email: ${email}`);
            // Here you can add the actual password reset request logic (e.g., form submission, API call)
        } else {
            alert('Please enter your email.');
        }
    }

    // Handle Request button click
    requestButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default form submission behavior
        handlePasswordReset();
    });

    // Event listener for "New Here? Create an Account"
    document.querySelector('.already-have-an').addEventListener('click', function () {
        // Redirect to the account creation page
        window.location.href = '/';  // Adjust the URL to your actual account creation page
    });
});
