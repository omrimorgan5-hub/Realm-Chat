// Set up needed variables to complete .js file
const verify_otp = document.getElementById("email-auth_submit");
const username = document.getElementById("username-otp");
const code = document.getElementById("otp");

// check if all fields are filled
if (!code || !username) {
    console.error("Missing required form elements.");
    throw new Error("Required form elements missing.");
}

verify_otp.addEventListener('click', async (event) => {
    event.preventDefault();

    // .value variables

    const payload_email = {
        otp: code.value.trim(),
        username: username.value
    };

    if (!code.value.trim() || !username) {
        console.error("Please fill in all fields.");
        return;
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/verify-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Fixed!
            },
            body: JSON.stringify(payload_email)
        });

        const data = await response.json();

        if (response.status === 200) {
            console.log("Success:", data);
            alert("verification successful!");
            window.location.replace("../LOGIN/login.html");
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