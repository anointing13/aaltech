document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#newsletter-form');
    const emailInput = document.querySelector('#email-input');
    const responseMessage = document.querySelector('#response-message');

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        const email = emailInput.value.trim();

        // Clear any existing message
        responseMessage.textContent = '';

        // Validate email
        if (!email) {
            responseMessage.textContent = 'Email is required.';
            responseMessage.style.color = 'red';
            return;
        }

        // Get CSRF token from cookies
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            responseMessage.textContent = 'CSRF token missing. Please reload the page.';
            responseMessage.style.color = 'red';
            return;
        }

        // Send email via AJAX
        fetch('/newsletter/subscribe/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken // CSRF token sent in header
            },
            body: `email=${encodeURIComponent(email)}`
        })
        .then(response => response.json())
        .then(data => {
            responseMessage.textContent = data.message || data.error;
            responseMessage.style.color = data.error ? 'red' : 'green';

            // Clear input if successful
            if (!data.error) {
                emailInput.value = '';
            }
        })
        .catch((error) => {
            console.error('AJAX error:', error); // Log the error for debugging
            responseMessage.textContent = 'An error occurred. Please try again.';
            responseMessage.style.color = 'red';
        });
    });

    // Helper function to extract CSRF token from cookies
    function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : null;
}

});
