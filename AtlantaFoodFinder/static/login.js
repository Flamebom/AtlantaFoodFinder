document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginButton = document.getElementById('login-btn');

    // Function to get the CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const cookieTrimmed = cookie.trim();
                if (cookieTrimmed.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookieTrimmed.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to handle the login process
    function handleLogin() {
        const email = emailInput.value;
        const password = passwordInput.value;

        // Log the email and password for debugging purposes
        console.log("Email:", email);
        console.log("Password:", password);

        if (email && password) {
            const csrftoken = getCookie('csrftoken');
            console.log("CSRF Token:", csrftoken);  // Log the CSRF token

            const formData = new FormData();
            formData.append('username', email);  // Use 'username' because Django's AuthenticationForm expects it
            formData.append('password', password);

            fetch('/login/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: formData,
            })
                .then(response => {
                    console.log("Response status:", response.status);  // Log response status
                    if (response.ok) {
                        window.location.href = 'signup/';  // Redirect to homepage
                        console.log("Login successful");
                    } else {
                        response.json().then(data => {
                            console.error("Login failed:", data);  // Log any returned errors
                            alert(data.error || 'Login failed.');
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        } else {
            alert('Please enter both email and password.');
        }
    }

    // Listen for "Enter" key in the email and password fields
    emailInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();  // Prevent the default form submission behavior
            passwordInput.focus();  // Move to the password input if Enter is pressed in the email field
        }
    });

    passwordInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();  // Prevent the default form submission behavior
            console.log("Handling login on Enter key in password field");
            handleLogin();  // Submit the login if Enter is pressed in the password field
        }
    });

    // Handle login button click
    loginButton.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default form submission behavior
        console.log("Login button clicked");
        handleLogin();
    });

    // Event listener for "Create an Account"
    const createAccountLink = document.querySelector('.already-have-an');
    if (createAccountLink) {
        createAccountLink.addEventListener('click', function (event) {
            if (event.target.textContent.includes('Create an Account')) {
                window.location.href = 'create-account.html';  // Adjust the URL to your actual account creation page
            }
        });
    }

    // Event listener for "Forgot your Password"
    const forgotPasswordLink = document.querySelectorAll('.already-have-an')[1];
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function () {
            window.location.href = 'passwordreset.html';  // Adjust the URL to your actual password reset page
        });
    }
});
