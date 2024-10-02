document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const registerButton = document.querySelector('.button');

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


    function handleRegistration() {
        const email = emailInput.value;
        const password = passwordInput.value;

        if (email && password) {
            const csrftoken = getCookie('csrftoken');

            const formData = new FormData();
            formData.append('email', email);
            formData.append('password1', password);

            fetch('/signup/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: formData,
            })
                .then(response => {
                    if (response.ok) {
                        // Registration successful
                        window.location.href = 'index/';  // Redirect to homepage
                    } else {
                        // Handle errors
                        response.json().then(data => {
                            alert(data.error || 'Registration failed.');
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
