document.addEventListener("DOMContentLoaded", function () {

    // MARK SINGLE NOTIFICATION AS READ
    document.querySelectorAll(".mark-read-btn").forEach(button => {
        button.addEventListener("click", async function () {

            const notificationId = this.dataset.id;

            try {
                const response = await fetch(`/notifications/read/${notificationId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                if (response.ok) {
                    const notification = this.closest(".notification-item");

                    notification.classList.remove("unread");
                    this.remove();
                }

            } catch (error) {
                console.error("Unable to mark notification as read:", error);
            }
        });
    });


    // MARK ALL NOTIFICATIONS AS READ
    const markAllButton = document.querySelector("#markAllRead");

    if (markAllButton) {
        markAllButton.addEventListener("click", async function () {

            try {
                const response = await fetch("/notifications/read-all/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                if (response.ok) {
                    document.querySelectorAll(".notification-item").forEach(item => {
                        item.classList.remove("unread");
                    });

                    document.querySelectorAll(".mark-read-btn").forEach(button => {
                        button.remove();
                    });
                }

            } catch (error) {
                console.error("Unable to mark all notifications as read:", error);
            }
        });
    }


    // DELETE NOTIFICATION
    document.querySelectorAll(".delete-notification-btn").forEach(button => {
        button.addEventListener("click", async function () {

            const notificationId = this.dataset.id;

            if (!confirm("Are you sure you want to delete this notification?")) {
                return;
            }

            try {
                const response = await fetch(`/notifications/delete/${notificationId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                if (response.ok) {
                    this.closest(".notification-item").remove();
                }

            } catch (error) {
                console.error("Unable to delete notification:", error);
            }
        });
    });


    // FILTER NOTIFICATIONS
    const filterButtons = document.querySelectorAll(".notification-filter");

    filterButtons.forEach(button => {
        button.addEventListener("click", function () {

            const filter = this.dataset.filter;

            filterButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            document.querySelectorAll(".notification-item").forEach(item => {

                if (filter === "all") {
                    item.style.display = "flex";
                }
                else if (filter === "unread") {
                    item.style.display = item.classList.contains("unread") ? "flex" : "none";
                }
                else if (filter === "read") {
                    item.style.display = !item.classList.contains("unread") ? "flex" : "none";
                }

            });
        });
    });


    // CSRF TOKEN
    function getCSRFToken() {
        const cookie = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="));

        return cookie ? decodeURIComponent(cookie.split("=")[1]) : "";
    }

});