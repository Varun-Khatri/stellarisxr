// Lightweight scroll reveal (performance-safe)

const elements = document.querySelectorAll(".card, h2, p, h1");

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = "translateY(0)";
        }
    });
}, {
    threshold: 0.1
});

elements.forEach(el => {
    el.style.opacity = 0;
    el.style.transform = "translateY(12px)";
    el.style.transition = "0.6s ease";
    observer.observe(el);
});