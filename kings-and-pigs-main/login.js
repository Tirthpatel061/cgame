function handleLogin(event) {
    event.preventDefault(); // Prevent the default form submission

    // Perform any validation or login logic here
    const form = document.getElementById('loginForm');
    const username = form.mail.value;
    const password = form.pass.value;

    // Example validation (you can replace this with actual logic)
    if (username && password) {
        // Redirect to index.html if validation passes
        window.location.href = 'index.html';
    } else {
        alert('Please enter both username and password.');
    }
} 