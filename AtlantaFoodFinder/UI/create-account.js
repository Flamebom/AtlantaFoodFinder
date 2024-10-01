document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const registerButton = document.querySelector('.button');

    // Function to handle registration (replace this with your registration logic)
    function handleRegistration() {
        const email = emailInput.value;
        const password = passwordInput.value;

        if (email && password) {
            alert(`Registering with Email: ${email} and Password: ${password}`);
            // Here you can add the actual registration logic (e.g., form submission, API call)
        } else {
            alert('Please enter both email and password.');
        }
    }

    // Handle register button click
    registerButton.addEventListener('click', function (event) {
        event.preventDefault();
        handleRegistration();
    });

    // Event listener for "Already have an account? Login"
    document.querySelector('.already-have-an').addEventListener('click', function () {
        // Redirect to the login page
        window.location.href = 'login.html';  // Adjust the URL to your actual login page
    });
});
