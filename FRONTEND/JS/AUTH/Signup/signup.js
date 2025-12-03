// New.
// Previous  was wrong i fixed and updated it.
const signupButton = document.getElementById('Sign-btn');
const usernameInput = document.getElementById('username-name');
const passwordInput = document.getElementById('password-pass');
const birthdayInput = document.getElementById('date-birth');
const displayNameInput = document.getElementById('display-name');
const emailInput = document.getElementById('email-user');

// Safety check: In JS we don't know the element types explicitly at compile time,
// but we can check if they exist before trying to add listeners or access .value.
if (!signupButton || !usernameInput || !passwordInput || !birthdayInput || !displayNameInput || !emailInput) {
    console.error("Missing required form elements.");
    // Depending on your environment (e.g., if this is a script tag in HTML),
    // you might remove the 'throw' if you want other scripts on the page to run.
    throw new Error("Required form elements missing.");
}

signupButton.addEventListener('click', async (event) => {
    event.preventDefault();

    // The .value property exists on input elements in standard JS
    const payload = {
        username: usernameInput.value.trim(),
        password: passwordInput.value,
        birthday: birthdayInput.value,
        display_name: displayNameInput.value.trim(),
        email: emailInput.value
    };

    // Basic client-side validation
    if (!payload.username || !payload.password || !payload.birthday || !payload.display_name || !payload.email) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Fixed!
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Success:", data);
            alert("Signup successful!");
            // Optional: redirect or clear form
        } else {
            console.error("Error:", data);
            alert(data.message || "Signup failed.");
        }
    } catch (err) {
        console.error("Network error:", err);
        alert("Could not connect to server.");
    }
});
