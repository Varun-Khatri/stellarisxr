// ===============================
// STELLARIS XR STUDIOS
// Main JavaScript
// ===============================

document.documentElement.classList.add("js");

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// --------------------------------
// BACKGROUND VIDEOS
// Autoplay muted loops only when motion is welcome and they are on screen.
// --------------------------------

const loopVideos = document.querySelectorAll("video[data-loop]");

if (!reduceMotion && "IntersectionObserver" in window) {
    const videoObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            const video = entry.target;

            if (entry.isIntersecting) {
                video.play().catch(() => { });
            } else {
                video.pause();
            }
        });
    }, { threshold: 0.2 });

    loopVideos.forEach(video => videoObserver.observe(video));
}

// --------------------------------
// GALLERIES
// Arrow buttons page the card row; they dim at either end.
// --------------------------------

document.querySelectorAll("[data-gallery]").forEach(wrap => {
    const track = wrap.querySelector(".gallery");
    const prev = wrap.querySelector(".g-btn.prev");
    const next = wrap.querySelector(".g-btn.next");

    if (!track || !prev || !next) return;

    function step() {
        const card = track.querySelector(".g-card");
        return card ? card.getBoundingClientRect().width + 20 : track.clientWidth * 0.8;
    }

    function update() {
        const max = track.scrollWidth - track.clientWidth - 2;
        prev.disabled = track.scrollLeft <= 2;
        next.disabled = track.scrollLeft >= max;
    }

    prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: reduceMotion ? "auto" : "smooth" }));
    next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: reduceMotion ? "auto" : "smooth" }));
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
});

// --------------------------------
// SERVICES DROPDOWN (keyboard and touch)
// --------------------------------

document.querySelectorAll(".dropdown").forEach(dropdown => {
    const toggle = dropdown.querySelector(".dropdown-toggle");

    if (!toggle) return;

    toggle.addEventListener("click", () => {
        const open = dropdown.classList.toggle("open");
        toggle.setAttribute("aria-expanded", String(open));
    });

    dropdown.addEventListener("keydown", e => {
        if (e.key === "Escape") {
            dropdown.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
            toggle.focus();
        }
    });

    document.addEventListener("click", e => {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
        }
    });

    dropdown.addEventListener("focusout", e => {
        if (!dropdown.contains(e.relatedTarget)) {
            dropdown.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
        }
    });
});

// --------------------------------
// MOBILE MENU
// --------------------------------

const mobileMenuButton = document.querySelector(".mobile-menu-button");
const mobileMenu = document.querySelector(".mobile-menu");
const mobileClose = document.querySelector(".mobile-close");

if (mobileMenuButton && mobileMenu && mobileClose) {
    function setMenu(open) {
        mobileMenu.classList.toggle("active", open);
        mobileMenu.setAttribute("aria-hidden", String(!open));
        mobileMenuButton.setAttribute("aria-expanded", String(open));
        document.body.style.overflow = open ? "hidden" : "";

        if (open) mobileClose.focus();
        else mobileMenuButton.focus();
    }

    mobileMenuButton.addEventListener("click", () => setMenu(true));
    mobileClose.addEventListener("click", () => setMenu(false));

    mobileMenu.addEventListener("keydown", e => {
        if (e.key === "Escape") setMenu(false);
    });

    mobileMenu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            mobileMenu.classList.remove("active");
            document.body.style.overflow = "";
        });
    });
}

// --------------------------------
// SCHEDULE A CALL
// --------------------------------

document.querySelectorAll("[data-schedule]").forEach(link => {
    link.addEventListener("click", e => {
        if (window.Calendly) {
            e.preventDefault();
            Calendly.initPopupWidget({ url: "https://cal.com/stellarisxr/consultation" });
        }
    });
});

// --------------------------------
// SECTION ENTRANCES
// Tiles rise into place once as they enter.
// --------------------------------

const revealGroups = document.querySelectorAll("[data-reveal]");

if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -5% 0px" });

    revealGroups.forEach(group => revealObserver.observe(group));
} else {
    revealGroups.forEach(group => group.classList.add("visible"));
}

// --------------------------------
// CONTACT FORM
// --------------------------------

const contactForm = document.querySelector(".contact-form");

if (contactForm) {
    const status = contactForm.querySelector(".form-status");

    contactForm.addEventListener("submit", async e => {
        e.preventDefault();

        const button = contactForm.querySelector("button[type='submit']");
        const label = button ? button.textContent : "";

        if (button) {
            button.textContent = "Sending";
            button.disabled = true;
        }

        if (status) {
            status.textContent = "";
            status.className = "form-status";
        }

        const scriptURL = "https://script.google.com/macros/s/AKfycbxsgovwSaeiaxtRvvmDFyD_86bLhSQ8bxa76gi3pwTH11SCMx8oJVrwlOJ3K33anKbU2Q/exec";

        try {
            await fetch(scriptURL, {
                method: "POST",
                body: new FormData(contactForm)
            });

            contactForm.reset();

            if (status) {
                status.textContent = "Demo request sent. We'll reply by email.";
                status.classList.add("ok");
            }
        } catch (error) {
            console.error(error);

            if (status) {
                status.textContent = "Your request didn't send. Check your connection and try again, or email varun@stellarisxr.com.";
                status.classList.add("error");
            }
        }

        if (button) {
            button.textContent = label;
            button.disabled = false;
        }
    });
}
