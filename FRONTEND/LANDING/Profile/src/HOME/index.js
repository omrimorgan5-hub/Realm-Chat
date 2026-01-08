const settings_button = document.getElementById("settings_btn");
const home_btn = document.getElementById("home_btn");
const notification_btn = document.getElementById("notification_btn");

settings_button.addEventListener('click', async(event) => {
    const settings_page = "settings.html"
    window.location.replace(settings_page);
    console.log("If you see this please check your network settings.");
    console.log(`You should have been redirected to ${settings_page}`);
});

home_btn.addEventListener('click', async(event) => {
    const home_page = "index.html"
    window.location.replace(home_page);
    console.log("If you see this please check your network settings.");
    console.log(`You should have been redirected to ${home_page}`);
});

notification_btn.addEventListener('click', async(event) => {
    const notification_page = "notifications.html"
    window.location.replace(notification_page);
    console.log("If you see this please check your network settings.");
    console.log(`You should have been redirected to ${notification_page}`);
});

