document.addEventListener("DOMContentLoaded", (event) => {
    const navContent = document.querySelector(".nav-content")
    const menuToggle = document.createElement("button")
    menuToggle.textContent = "Menú"
    menuToggle.classList.add("menu-toggle")

    const logo = document.querySelector(".logo")
    logo.parentNode.insertBefore(menuToggle, logo.nextSibling)

    menuToggle.addEventListener("click", () => {
        navContent.classList.toggle("show")
    })

  // Close menu when clicking outside
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".nav-container")) {
        navContent.classList.remove("show")
        }
    })

  // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
        e.preventDefault()
        document.querySelector(this.getAttribute("href")).scrollIntoView({
            behavior: "smooth",
        })
        })
    })

  // Form submission (if you decide to add a form later)
    const form = document.querySelector("form")
    if (form) {
        form.addEventListener("submit", (e) => {
        e.preventDefault()
        const email = document.getElementById("email-address").value
        // Here you would typically send this to your server or newsletter service
        console.log(`Subscribing email: ${email}`)
        alert("Thanks for subscribing!")
        form.reset()
        })
    }
})

