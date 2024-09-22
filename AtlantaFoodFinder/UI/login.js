// JavaScript to handle Enter key submission for email and password fields
document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginButton = document.getElementById('login-btn');

    // Function to handle login submission
    function handleLogin() {
        const email = emailInput.value;
        const password = passwordInput.value;

        if (email && password) {
            alert(`Logging in with Email: ${email} and Password: ${password}`);
            // Here you can add the actual login logic (e.g., form submission, API call)



            // PUT IN ACTUAL LOGIC HERE





        } else {
            alert('Please enter both email and password.');
        }
    }

    // Listen for "Enter" key in the email and password fields
    emailInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            passwordInput.focus();  // Move to the password input if Enter is pressed in email field
        }
    });

    passwordInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleLogin();  // Submit the login if Enter is pressed in the password field
        }
    });

    // Handle login button click
    loginButton.addEventListener('click', function (event) {
        event.preventDefault();
        handleLogin();
    });
});
