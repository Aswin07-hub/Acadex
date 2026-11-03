
// ========================================
// 1. GET HTML ELEMENTS
// ========================================

const uploadModal = document.getElementById("uploadModal");

const openUpload = document.getElementById("openUpload");

const closeUpload = document.getElementById("closeUpload");

const cancelUpload = document.getElementById("cancelUpload");

const documentFile = document.getElementById("documentFile");

const documentType = document.getElementById("documentType");

const dashboardSearch = document.getElementById("dashboardSearch");

const documentTable = document.getElementById("documentTable");


// ========================================
// 2. OPEN UPLOAD MODAL
// ========================================

if (openUpload && uploadModal) {

    openUpload.addEventListener("click", function () {

        uploadModal.showModal();

    });

}


// ========================================
// 3. CLOSE UPLOAD MODAL
// ========================================

if (closeUpload) {

    closeUpload.addEventListener("click", function () {

        uploadModal.close();

    });

}


if (cancelUpload) {

    cancelUpload.addEventListener("click", function () {

        uploadModal.close();

    });

}


// ========================================
// 4. CLOSE MODAL WHEN CLICKING OUTSIDE
// ========================================

if (uploadModal) {

    uploadModal.addEventListener("click", function (event) {

        if (event.target === uploadModal) {

            uploadModal.close();

        }

    });

}


// ========================================
// 5. DOCUMENT FILE VALIDATION
// ========================================

if (documentFile) {

    documentFile.addEventListener("change", function () {

        const file = documentFile.files[0];

        if (!file) {
            return;
        }

        const allowedTypes = [
            "application/pdf",
            "image/jpeg",
            "image/png"
        ];

        const maxSize = 10 * 1024 * 1024; // 10 MB


        // Check file type

        if (!allowedTypes.includes(file.type)) {

            alert("Please select a PDF, JPG or PNG file.");

            documentFile.value = "";

            return;

        }


        // Check file size

        if (file.size > maxSize) {

            alert("File size must be less than 10 MB.");

            documentFile.value = "";

            return;

        }

    });

}


// ========================================
// 6. VALIDATE DOCUMENT FORM
// ========================================

const uploadForm = uploadModal
    ? uploadModal.querySelector("form")
    : null;

if (uploadForm) {

    uploadForm.addEventListener("submit", function (event) {

        const selectedType = documentType.value;

        const selectedFile = documentFile.files[0];


        if (!selectedType) {

            event.preventDefault();

            alert("Please select a document type.");

            documentType.focus();

            return;

        }


        if (!selectedFile) {

            event.preventDefault();

            alert("Please select a document file.");

            documentFile.focus();

            return;

        }


        const allowedTypes = [
            "application/pdf",
            "image/jpeg",
            "image/png"
        ];


        if (!allowedTypes.includes(selectedFile.type)) {

            event.preventDefault();

            alert("Only PDF, JPG and PNG files are allowed.");

            documentFile.value = "";

            return;

        }


        if (selectedFile.size > 10 * 1024 * 1024) {

            event.preventDefault();

            alert("File size must be less than 10 MB.");

            documentFile.value = "";

            return;

        }


        // Allow normal Django form submission.
        // Django receives the uploaded file through POST.

    });

}


// ========================================
// 7. SEARCH DOCUMENTS
// ========================================

if (dashboardSearch && documentTable) {

    dashboardSearch.addEventListener("input", function () {

        const searchValue = dashboardSearch.value
            .toLowerCase()
            .trim();

        const rows = documentTable.querySelectorAll(
            ".document-row"
        );

        rows.forEach(function (row) {

            const documentName = row.textContent.toLowerCase();

            if (documentName.includes(searchValue)) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        });

    });

}


// ========================================
// 8. SIDEBAR ACTIVE SECTION
// ========================================

const navigationLinks = document.querySelectorAll(
    ".sidebar-nav .nav-link"
);

navigationLinks.forEach(function (link) {

    link.addEventListener("click", function () {

        navigationLinks.forEach(function (item) {

            item.classList.remove("active");

        });

        link.classList.add("active");

    });

});


// ========================================
// 9. LOGOUT CONFIRMATION
// ========================================

const logoutForm = document.querySelector(
    ".sidebar-bottom form"
);

if (logoutForm) {

    logoutForm.addEventListener("submit", function (event) {

        const confirmLogout = confirm(
            "Are you sure you want to logout?"
        );

        if (!confirmLogout) {

            event.preventDefault();

        }

    });

}


// ========================================
// 10. DOCUMENT UPLOAD FEEDBACK
// ========================================

if (uploadForm) {

    uploadForm.addEventListener("submit", function () {

        const submitButton = uploadForm.querySelector(
            'button[type="submit"]'
        );

        if (submitButton) {

            submitButton.textContent = "Uploading...";

            submitButton.disabled = true;

        }

    });

}


// ========================================
// 11. INITIALIZATION
// ========================================

console.log("Acadex Student Dashboard loaded successfully.");
