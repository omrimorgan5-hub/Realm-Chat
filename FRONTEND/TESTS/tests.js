// 1. Select the elements once when the script loads
const messageInput = document.getElementById("message");
const recipientInput = document.getElementById("recipitent"); // Matches your HTML typo
const senderInput = document.getElementById("sender");
const sendBtn = document.getElementById("send_btn");

// 2. Add the event listener to the button
sendBtn.addEventListener("click", async (event) => {
    // Stop the page from refreshing
    event.preventDefault();

    // 3. Defensive Check: Ensure all elements were actually found in the DOM
    if (!messageInput || !recipientInput || !senderInput) {
        console.error("Critical Error: One or more input fields were not found in the HTML.");
        alert("System error: Form fields are missing. Check your HTML IDs.");
        return;
    }

    // 4. Extract and clean the values
    const messageValue = messageInput.value.trim();
    const recipientValue = recipientInput.value.trim();
    const senderValue = senderInput.value.trim();

    // 5. Validation: Don't send if any field is empty
    if (!messageValue || !recipientValue || !senderValue) {
        alert("Please fill in all fields before sending.");
        return;
    }

    // 6. Prepare the data for the backend
    const payload = {
        message: messageValue,
        recipitent: recipientValue, // Matches your original typo for backend compatibility
        sender: senderValue
    };

    try {
        // 7. Send the request to your Flask backend
        const response = await fetch('http://127.0.0.1:5000/send_msg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // 8. Handle the server's response
        const data = await response.json();

        if (response.ok) { // Status codes 200-299
            console.log("Success:", data);
            alert("Message sent successfully!");
            
            // Optional: Clear the message field after success
            messageInput.value = "";
        } else {
            // Handle server-side errors (400, 500, etc.)
            console.error("Server Error:", response.status, data);
            alert(data.message || `Error ${response.status}: Failed to send message.`);
        }

    } catch (err) {
        // 9. Handle network errors (Server is offline, CORS issues, etc.)
        console.error("Network/Connection Error:", err);
        alert("Could not connect to the server. Please ensure your backend is running.");
    }
});
