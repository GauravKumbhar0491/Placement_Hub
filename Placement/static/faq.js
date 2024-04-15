document.addEventListener("DOMContentLoaded", function() {
    const accordionItems = document.querySelectorAll(".accordion-item");

    accordionItems.forEach(item => {
        item.addEventListener("click", function() {
            // Toggle active class on the clicked item
            this.classList.toggle("active");

            // Close other accordion items
            accordionItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains("active")) {
                    otherItem.classList.remove("active");
                }
            });
        });
    });
});
