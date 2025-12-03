// New.
// Previous  was wrong i fixed and updated it.
const loginButton = document.getElementById('Log-In-btn');
const usernameInput = document.getElementById('username-name-log');
const passwordInput = document.getElementById('password-pass-log');


// Safety check: In JS we don't know the element types explicitly at compile time,
// but we can check if they exist before trying to add listeners or access .value.
if (!loginButton || !usernameInput || !passwordInput) {
    console.error("Missing required form elements.");
    // Depending on your environment (e.g., if this is a script tag in HTML),
    // you might remove the 'throw' if you want other scripts on the page to run.
    throw new Error("Required form elements missing.");
}

loginButton.addEventListener('click', async (event) => {
    event.preventDefault();

    // The .value property exists on input elements in standard JS
    const payload_log = {
        username_log: usernameInput.value.trim(),
        password_log: passwordInput.value,
    };

    // Basic client-side validation
    if (!payload_log.username || !payload_log.password ) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Fixed!
            },
            body: JSON.stringify(payload_log)
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Success:", data);
            alert("Login successful!");
            // Optional: redirect or clear form
        } else {
            console.error("Error:", data);
            alert(data.message || "Login failed.");
        }
    } catch (err) {
        console.error("Network error:", err);
        alert("Could not connect to server.");
    }
    usernameInput.value = "";
    passwordInput.value = "";

});
