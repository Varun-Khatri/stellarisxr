// ===============================
// STELLARIS XR STUDIOS
// Main JavaScript
// ===============================

// --------------------------------
// HERO SHOWCASE ROTATION
// --------------------------------

const heroData = [
    {
        title: "Built for\nImmersion.",
        text: "We design spatial experiences that inspire, educate and entertain.",
        bg: "linear-gradient(120deg, #eaf8ff 0%, #ffffff 45%, #dbefff 100%)"
    },
    {
        title: "XR Experiences\nfor Enterprise.",
        text: "Immersive solutions for automotive, tourism and real estate industries.",
        bg: "linear-gradient(120deg, #020617 0%, #0f172a 50%, #000000 100%)"
    },
    {
        title: "Games That\nFeel Alive.",
        text: "Interactive worlds crafted with cinematic storytelling and immersive gameplay.",
        bg: "linear-gradient(120deg, #0a0f1f 0%, #081120 45%, #000000 100%)"
    },
    {
        title: "Visualize.\nInteract.\nExperience.",
        text: "Premium XR systems designed for the next generation of digital experiences.",
        bg: "linear-gradient(120deg, #ffffff 0%, #eef7ff 45%, #d8f3ff 100%)"
    }
];

const heroTitle = document.querySelector(".hero-title");
const heroText = document.querySelector(".hero-text");
const heroBg = document.querySelector(".hero-bg");
const dots = document.querySelectorAll(".showcase-dots span");

let currentHero = 0;

function updateHero(index) {
    if (!heroTitle || !heroText || !heroBg) return;

    heroTitle.innerHTML = heroData[index].title.replace(/\n/g, "<br>");
    heroText.textContent = heroData[index].text;
    heroBg.style.background = heroData[index].bg;

    dots.forEach(dot => dot.classList.remove("active"));

    if (dots[index]) {
        dots[index].classList.add("active");
    }

    const isDark =
        index === 1 ||
        index === 2;

    if (isDark) {
        heroTitle.style.color = "#ffffff";
        heroText.style.color = "rgba(255,255,255,0.72)";
    } else {
        heroTitle.style.color = "#000000";
        heroText.style.color = "rgba(0,0,0,0.72)";
    }
}

function rotateHero() {
    currentHero++;

    if (currentHero >= heroData.length) {
        currentHero = 0;
    }

    updateHero(currentHero);
}

setInterval(rotateHero, 5000);

updateHero(currentHero);

// --------------------------------
// MOBILE MENU
// --------------------------------

const mobileMenuButton =
    document.querySelector(".mobile-menu-button");

const mobileMenu =
    document.querySelector(".mobile-menu");

const mobileClose =
    document.querySelector(".mobile-close");

if (
    mobileMenuButton &&
    mobileMenu &&
    mobileClose
) {

    mobileMenuButton.addEventListener("click", () => {
        mobileMenu.classList.add("active");
        document.body.style.overflow = "hidden";
    });

    mobileClose.addEventListener("click", () => {
        mobileMenu.classList.remove("active");
        document.body.style.overflow = "";
    });

}

// --------------------------------
// SMOOTH SCROLL
// --------------------------------

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {
            target.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});

// --------------------------------
// NAVBAR BACKGROUND ON SCROLL
// --------------------------------

const header = document.querySelector(".site-header");

window.addEventListener("scroll", () => {
    if (!header) return;

    if (window.scrollY > 40) {
        header.style.background = "rgba(0,0,0,0.78)";
        header.style.borderBottom = "1px solid rgba(255,255,255,0.12)";
    } else {
        header.style.background = "rgba(0,0,0,0.38)";
        header.style.borderBottom = "1px solid rgba(255,255,255,0.08)";
    }
});

// --------------------------------
// FADE-IN ANIMATION
// --------------------------------

const observer = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    },
    {
        threshold: 0.15
    }
);

document.querySelectorAll(".fade-in").forEach(el => {
    observer.observe(el);
});

// --------------------------------
// SERVICE CARD HOVER GLOW
// --------------------------------

const cards = document.querySelectorAll(".service-card");

cards.forEach(card => {
    card.addEventListener("mousemove", e => {
        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        card.style.background = `
      radial-gradient(
        circle at ${x}px ${y}px,
        rgba(71,209,254,0.16),
        rgba(0,0,0,0.92) 45%
      )
    `;
    });

    card.addEventListener("mouseleave", () => {
        card.style.background = `
      linear-gradient(
        to bottom,
        rgba(255,255,255,0.08),
        rgba(255,255,255,0.02)
      ),
      #090909
    `;
    });
});

// --------------------------------
// CONTACT FORM
// --------------------------------

const contactForm = document.querySelector(".contact-form");

if (contactForm) {
    contactForm.addEventListener("submit", async e => {
        e.preventDefault();

        const button = contactForm.querySelector("button");

        if (button) {
            button.textContent = "Sending...";
            button.disabled = true;
        }

        // REPLACE WITH YOUR GOOGLE APPS SCRIPT URL
        const scriptURL = "https://script.google.com/macros/s/AKfycbxsgovwSaeiaxtRvvmDFyD_86bLhSQ8bxa76gi3pwTH11SCMx8oJVrwlOJ3K33anKbU2Q/exec";

        const formData = new FormData(contactForm);

        try {
            await fetch(scriptURL, {
                method: "POST",
                body: formData
            });

            alert("Demo request submitted successfully.");

            contactForm.reset();
        } catch (error) {
            console.error(error);

            alert("Something went wrong. Please try again.");
        }

        if (button) {
            button.textContent = "Request Demo";
            button.disabled = false;
        }
    });
}

// --------------------------------
// PARALLAX EFFECT
// --------------------------------

const parallaxItems = document.querySelectorAll(".parallax");

window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;

    parallaxItems.forEach(item => {
        const speed = item.dataset.speed || 0.2;

        item.style.transform = `translateY(${scrollY * speed}px)`;
    });
});

// --------------------------------
// LIGHT/DARK SECTION DETECTION
// --------------------------------
/*
const sections = document.querySelectorAll(".section");

window.addEventListener("scroll", () => {
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();

        if (
            rect.top <= window.innerHeight / 2 &&
            rect.bottom >= window.innerHeight / 2
        ) {
            const isLight = section.classList.contains("light");

            if (isLight) {
                header.style.color = "#000";
            } else {
                header.style.color = "#fff";
            }
        }
    });
});
*/
// --------------------------------
// PRELOADER
// --------------------------------

window.addEventListener("load", () => {
    const loader = document.querySelector(".preloader");

    if (loader) {
        loader.classList.add("hide");

        setTimeout(() => {
            loader.remove();
        }, 800);
    }
});