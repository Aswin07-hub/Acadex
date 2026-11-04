const editButton = document.getElementById("editButton");
const cancelButton = document.getElementById("cancelButton");
const profileForm = document.getElementById("profileForm");
const formActions = document.getElementById("formActions");

const editableFields = [
    "first_name",
    "last_name",
    "date_of_birth",
    "email",
    "phone",
    "address"
];

const originalValues = {};

editableFields.forEach(function (name) {
    const field = profileForm.elements[name];

    if (field) {
        originalValues[name] = field.value;
    }
});

function setEditMode(enabled) {

    editableFields.forEach(function (name) {

        const field = profileForm.elements[name];

        if (field) {
            field.readOnly = !enabled;
        }

    });

    formActions.style.display = enabled ? "flex" : "none";

    editButton.style.display = enabled ? "none" : "block";
}


editButton.addEventListener("click", function () {
    setEditMode(true);
});


cancelButton.addEventListener("click", function () {

    editableFields.forEach(function (name) {

        const field = profileForm.elements[name];

        if (field) {
            field.value = originalValues[name];
        }

    });

    setEditMode(false);

});


profileForm.addEventListener("submit", function (event) {

    event.preventDefault();

    alert("Profile page is ready. Database save integration is the next step.");

});