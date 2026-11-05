document.addEventListener("DOMContentLoaded", function () {

    const profileView = document.getElementById("profileView");
    const profileEdit = document.getElementById("profileEdit");

    const editButton = document.getElementById("apEditButton");
    const cancelButton = document.getElementById("apCancelEdit");

    const profileForm = document.getElementById("apProfileForm");

    const fullName = document.getElementById("apFullName");
    const firstName = document.getElementById("apFirstName");
    const lastName = document.getElementById("apLastName");

    if (!profileView || !profileEdit) {
        console.error("Student Profile elements not found.");
        return;
    }

    let originalValues = {};

    // Save original form values
    function saveOriginalValues() {

        if (!profileForm) return;

        originalValues = {};

        profileForm.querySelectorAll("input, textarea").forEach(function (field) {

            if (field.type !== "file" && field.type !== "hidden") {
                originalValues[field.name || field.id] = field.value;
            }

        });

    }

    // Restore values when Cancel is clicked
    function restoreOriginalValues() {

        if (!profileForm) return;

        profileForm.querySelectorAll("input, textarea").forEach(function (field) {

            if (field.type === "file") {
                field.value = "";
                return;
            }

            if (field.type === "hidden") return;

            const key = field.name || field.id;

            if (Object.prototype.hasOwnProperty.call(originalValues, key)) {
                field.value = originalValues[key];
            }

        });

    }

    // Open edit form
    function openEditForm() {

        saveOriginalValues();

        profileView.hidden = true;
        profileEdit.hidden = false;

    }

    // Cancel editing
    function cancelEditForm() {

        restoreOriginalValues();

        profileEdit.hidden = true;
        profileView.hidden = false;

    }

    // Edit button
    if (editButton) {

        editButton.addEventListener("click", function () {
            openEditForm();
        });

    }

    // Cancel button
    if (cancelButton) {

        cancelButton.addEventListener("click", function () {
            cancelEditForm();
        });

    }

    // Prepare name fields before submitting
    if (profileForm) {

        profileForm.addEventListener("submit", function (event) {

            const name = fullName.value.trim();

            if (!name) {
                event.preventDefault();
                alert("Please enter your full name.");
                return;
            }

            const nameParts = name.split(/\s+/);

            firstName.value = nameParts[0];
            lastName.value = nameParts.slice(1).join(" ");

        });

    }

});