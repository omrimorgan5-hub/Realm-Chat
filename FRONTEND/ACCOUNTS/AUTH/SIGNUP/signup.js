// signup.js

const signupButton = document.getElementById('Sign-btn');
const usernameInput = document.getElementById('username-name');
const passwordInput = document.getElementById('password-pass');
const birthdayInput = document.getElementById('date-birth');
const displayNameInput = document.getElementById('display-name');
const emailInput = document.getElementById('email-user');

// Safety check to ensure HTML elements exist
if (!signupButton || !usernameInput || !passwordInput || !birthdayInput || !displayNameInput || !emailInput) {
    console.error("Missing required form elements in HTML.");
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

            // Clear inputs
            usernameInput.value = "";
            passwordInput.value = "";
            emailInput.value = "";
            birthdayInput.value = "";
            displayNameInput.value = "";
        

            
        } else {
            // 3. Handle Server Logic Errors (400, 409, 500, etc.)
            console.error("Signup logic error:", response.status, data);
            alert(data.message || `Error ${response.status}: Signup failed.`);
        }
    } catch (err) {
        console.error("Network error:", err);
        alert("Could not connect to server.");
    }

    usernameInput = ""
    passwordInput = ""
    emailInput = ""
    birthdayInput = ""
    displayNameInput = ""
});
