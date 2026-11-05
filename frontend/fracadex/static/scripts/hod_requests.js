
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("requestForm");
    const deadline = document.getElementById("deadline");
    const submitBtn = document.getElementById("submitBtn");

    if (!form || !deadline || !submitBtn) {
        return;
    }

    // Prevent selecting a past deadline
    const today = new Date();
    const localToday = new Date(
        today.getTime() - today.getTimezoneOffset() * 60000
    ).toISOString().split("T")[0];

    deadline.min = localToday;

    form.addEventListener("submit", function (event) {

        if (deadline.value < localToday) {
            event.preventDefault();
            alert("Please select today or a future deadline.");
            return;
        }

        const confirmed = confirm(
            "Are you sure you want to create this submission request?"
        );

        if (!confirmed) {
            event.preventDefault();
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = "Creating Request...";

    });

});
