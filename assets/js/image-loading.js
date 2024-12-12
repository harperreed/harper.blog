document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll("img");

    images.forEach((img) => {
        img.onload = () => {
            img.classList.add("loaded");
        };

        // If the image is already in cache and loads before the event listener is set
        if (img.complete) {
            img.classList.add("loaded");
        }
    });
});
