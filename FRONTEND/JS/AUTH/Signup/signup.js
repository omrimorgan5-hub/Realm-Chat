// signup.js

const signupButton = document.getElementById('Sign-btn');
const usernameInput = document.getElementById('username-name');
const passwordInput = document.getElementById('password-pass');
const birthdayInput = document.getElementById('date-birth');
const displayNameInput = document.getElementById('display-name');
const emailInput = document.getElementById('email-user');

// Safety check
if (!signupButton || !usernameInput || !passwordInput || !birthdayInput || !displayNameInput || !emailInput) {
    console.error("Missing required form elements.");
    throw new Error("Required form elements missing.");
}

signupButton.addEventListener('click', async (event) => {
    event.preventDefault();

    const payload = {
        username: usernameInput.value.trim(),
        password: passwordInput.value,
        birthday: birthdayInput.value,
        display_name: displayNameInput.value.trim(),
        email: emailInput.value
    };

    if (!payload.username || !payload.password || !payload.birthday || !payload.display_name || !payload.email) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.status === 201) {
            console.log("Signup successful:", data);
            alert("Signup successful! You can now verify OTP.");
        } else {
            console.error("Signup error:", data);
            alert(data.message || "Signup failed.");
        }
    } catch (err) {
        console.error("Network error:", err);
        alert("Could not connect to server.");
    }
});


