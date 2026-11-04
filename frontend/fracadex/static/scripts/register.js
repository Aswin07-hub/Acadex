document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");
    const phone = document.getElementById("phone");
    const message = document.getElementById("formMessage");
    const submitButton = form?.querySelector(".register-button");
 
    if (!form) return;

    // Show and hide passwords
    document.querySelectorAll(".toggle-password").forEach(function (button) {

        button.addEventListener("click", function () {

            const targetId = button.dataset.target;
            const input = document.getElementById(targetId);

            if (!input) return;

            if (input.type === "password") {
                input.type = "text";
                button.textContent = "Hide";
            } else {
                input.type = "password";
                button.textContent = "Show";
            }

        });

    });

    // Display validation messages
    function showMessage(text, type = "error") {
        if (!message) return;

        message.textContent = text;
        message.className = "form-message " + type;
    }

    function clearMessage() {
        if (!message) return;

        message.textContent = "";
        message.className = "form-message";
    }

    // Confirm password while typing
    confirmPassword?.addEventListener("input", function () {

        clearMessage();

        if (confirmPassword.value && password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity("Passwords do not match.");
        } else {
            confirmPassword.setCustomValidity("");
        }

    });

    password?.addEventListener("input", function () {

        clearMessage();

        if (confirmPassword.value) {
            confirmPassword.setCustomValidity(
                password.value === confirmPassword.value
                    ? ""
                    : "Passwords do not match."
            );
        }

    });

    // Phone number validation
    phone?.addEventListener("input", function () {

        phone.value = phone.value.replace(/[^\d+\-\s()]/g, "");
        clearMessage();

    });

    // Date of birth: prevent future dates
    const dob = document.getElementById("date_of_birth");

    if (dob) {
        const today = new Date();
        const localToday = [
            today.getFullYear(),
            String(today.getMonth() + 1).padStart(2, "0"),
            String(today.getDate()).padStart(2, "0")
        ].join("-");

        dob.max = localToday;
    }

    // Form submission validation
    form.addEventListener("submit", function (event) {

        clearMessage();

        // Check all HTML required fields
        if (!form.checkValidity()) {
            event.preventDefault();
            form.reportValidity();
            return;
        }

        // Password length
        if (password.value.length < 8) {
            event.preventDefault();
            showMessage("Password must contain at least 8 characters.");
            password.focus();
            return;
        }

        // Password match
        if (password.value !== confirmPassword.value) {
            event.preventDefault();
            showMessage("Password and confirm password do not match.");
            confirmPassword.focus();
            return;
        }

        // Phone validation
        const phoneDigits = phone.value.replace(/\D/g, "");

        if (phoneDigits.length < 10 || phoneDigits.length > 15) {
            event.preventDefault();
            showMessage("Enter a valid phone number (10 to 15 digits).");
            phone.focus();
            return;
        }

        // Allow the normal POST request to Django
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = "Creating Account...";
        }

    });

});