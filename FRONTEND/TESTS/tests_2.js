// 1. Select the ELEMENTS, not the values, at the top
const messageEl = document.getElementById("message");
const recipientEl = document.getElementById("recipitent"); // Check HTML for this spelling
const senderEl = document.getElementById("sender");
const sendBtn = document.getElementById("send_btn");

sendBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    // 2. Read the VALUES here, inside the function
    const message = messageEl.value.trim();
    const recipient = recipientEl.value.trim();
    const sender = senderEl.value.trim();

    // 3. Log them to see exactly what the script sees
    console.log("Current values:", { message, recipient, sender });

    if (!message || !recipient || !sender) {
        alert("Validation failed: One or more fields are still empty.");
        return;
    }

    // ... continue with fetch
});
