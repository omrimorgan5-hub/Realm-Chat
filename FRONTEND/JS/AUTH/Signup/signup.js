// signup.js

const signupButton = document.getElementById('Sign-btn');
const usernameInput = document.getElementById('username-name');
const passwordInput = document.getElementById('password-pass');
const birthdayInput = document.getElementById('date-birth');
const displayNameInput = document.getElementById('display-name');
const emailInput = document.getElementById('email-user');
const formContainer = document.getElementById('form-container'); // wrapper div around your form
const messageBox = document.getElementById('message-box'); // add a <div id="message-box"></div> in HTML

// Utility to show messages inline
function showMessage(msg, isError = false) {
    messageBox.textContent = msg;
    messageBox.style.color = isError ? "red" : "green";
}

// Safety check
if (!signupButton || !usernameInput || !passwordInput || !birthdayInput || !displayNameInput || !emailInput || !formContainer || !messageBox) {
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
        showMessage("Please fill in all fields.", true);
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Signup started:", data);
            showMessage("Signup started. Please verify OTP.");

            // Swap out signup form for OTP form
            formContainer.innerHTML = `
                <form id="otp-form">
                    <input type="text" id="otp-code" placeholder="Enter OTP" required>
                    <button type="submit">Verify</button>
                </form>
            `;

            // Attach OTP form handler
            const otpForm = document.getElementById('otp-form');
            otpForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const otpPayload = {
                    username: payload.username,
                    otp: document.getElementById('otp-code').value.trim()
                };

                try {
                    const verifyRes = await fetch('http://127.0.0.1:5000/verify-otp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(otpPayload)
                    });

                    const verifyData = await verifyRes.json();

                    if (verifyRes.ok) {
                        showMessage("Account verified!");
                        console.log("Verification success:", verifyData);
                        // Optional: redirect to dashboard or login page
                        // window.location.href = "/dashboard.html";
                    } else {
                        showMessage(verifyData.message || "OTP verification failed.", true);
                        console.error("Verification error:", verifyData);
                    }
                } catch (err) {
                    console.error("Network error during OTP verification:", err);
                    showMessage("Could not connect to server for OTP verification.", true);
                }
            });
        } else {
            console.error("Signup error:", data);
            showMessage(data.message || "Signup failed.", true);
        }
    } catch (err) {
        console.error("Network error:", err);
        showMessage("Could not connect to server.", true);
    }
});

