
<<<<<<< HEAD
// ======================================
// 1. Show and Hide Password
// ======================================
=======
// ========================================
// 1. GET HTML ELEMENTS
// ========================================
>>>>>>> bd4a0030db424e0b74989f15dec3197df1795904

const loginForm = document.getElementById("loginForm");
const roleInput = document.getElementById("role");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

const togglePassword = document.getElementById("togglePassword");
const message = document.getElementById("message");


// ========================================
// 2. SHOW / HIDE PASSWORD
// ========================================

togglePassword.addEventListener("click", function () {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        togglePassword.textContent = "Hide";

        togglePassword.setAttribute(
            "aria-label",
            "Hide password"
        );

    } else {

        passwordInput.type = "password";

        togglePassword.textContent = "Show";

        togglePassword.setAttribute(
            "aria-label",
            "Show password"
        );

    }

});


<<<<<<< HEAD
// ======================================
// 2. Login Form Validation
// ======================================

const loginForm = document.getElementById("loginForm");

const message = document.getElementById("message");

loginForm.addEventListener("submit", function (event) {

    const role = document.getElementById("role").value;

    const username = document.getElementById("username").value.trim();

    const password = passwordInput.value;

    if (
        role === "" ||
        username === "" ||
        password === ""
    ) {

        event.preventDefault();

        message.textContent = "Please fill in all fields.";

        message.style.color = "red";

    }

=======
// ========================================
// 3. DISPLAY MESSAGE
// ========================================

function showMessage(text, type) {

    message.textContent = text;

    message.className = "message " + type;

}


// ========================================
// 4. LOGIN FORM VALIDATION
// ========================================

loginForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const role = roleInput.value;
    const username = usernameInput.value.trim();
    const password = passwordInput.value;


    // Check role

    if (!role) {

        showMessage(
            "Please select your login role.",
            "error"
        );

        roleInput.focus();

        return;

    }


    // Check username

    if (username === "") {

        showMessage(
            "Please enter your username or register number.",
            "error"
        );

        usernameInput.focus();

        return;

    }


    // Check password

    if (password.trim() === "") {

        showMessage(
            "Please enter your password.",
            "error"
        );

        passwordInput.focus();

        return;

    }


    // Basic password length validation

    if (password.length < 6) {

        showMessage(
            "Password must contain at least 6 characters.",
            "error"
        );

        passwordInput.focus();

        return;

    }


    // Frontend validation completed

    showMessage(
        "Form validated. Connecting to Acadex...",
        "success"
    );

});


// ========================================
// 5. FORGOT PASSWORD LINK
// ========================================

const forgotLink = document.querySelector(".forgot-link");

forgotLink.addEventListener("click", function (event) {

    event.preventDefault();

    showMessage(
        "Please contact your administrator to reset your password.",
        "error"
    );

});


// ========================================
// 6. CLEAR MESSAGE WHEN USER TYPES
// ========================================

[roleInput, usernameInput, passwordInput].forEach(input => {

    input.addEventListener("input", function () {

        message.textContent = "";

        message.className = "message";

    });

>>>>>>> bd4a0030db424e0b74989f15dec3197df1795904
});


// ======================================
// 3. Login Submission
// ======================================

// The browser submits the form using POST.
// Frontend Django views.py receives the request.
// Python requests performs GET and POST
// communication with the backend API.
