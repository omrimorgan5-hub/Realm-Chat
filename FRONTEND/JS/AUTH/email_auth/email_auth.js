// Set up needed variables to complete .js file
const verify_otp = document.getElementById("email-auth_submit");
const code = document.getElementById("otp");
const username_email = document.getElementById('username-email');

// check if all fields are filled
if (!verify_otp || !code || !username_email) {
    console.error("Missing required form elements.");
    throw new Error("Required form elements missing.");
}

verify_otp.addEventListener('click', async (event) => {
    event.preventDefault();

    // .value variables

    const payload_email = {
        code: code,
        username: username_email
    };

    if (!payload_email.code || payload_email.username) {
        console.error("Please fill in all fields.");
        return;
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/email_auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Fixed!
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Success:", data);
            alert("verification successful!");
            // Optional: redirect or clear form
        } else {
            console.error("Error:", data);
            alert(data.message || "verification failed.");
        }

    } catch (err) {
        console.error("Network error:", err);
        alert("Could not connect to server.");
    }

    
});