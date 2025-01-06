document.addEventListener("DOMContentLoaded", () => {
    if (!API_TOKEN || !USER_TYPE) {
        console.error("API Token or User Type is missing.");
        alert("Authorization token or user type is not provided. Please log in again.");
        return;
    }

    // Toggle password visibility
    document.querySelectorAll(".toggle-password").forEach((button) => {
        button.addEventListener("click", () => {
            const target = document.getElementById(button.dataset.target);
            if (target.type === "password") {
                target.type = "text";
                button.textContent = "Hide";
            } else {
                target.type = "password";
                button.textContent = "Show";
            }
        });
    });

    // Handle form submission
    document.getElementById("change-password-form").addEventListener("submit", (event) => {
        event.preventDefault();

        const oldPassword = document.getElementById("old-password").value;
        const newPassword = document.getElementById("new-password").value;
        const confirmNewPassword = document.getElementById("confirm-new-password").value;

        if (newPassword !== confirmNewPassword) {
            alert("New password and confirmation do not match.");
            return;
        }

        const endpoint =
            USER_TYPE === "hospital"
                ? "/hospital/api/change-password/"
                : "/supervisor/api/change-password/";

        fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${API_TOKEN}`,
            },
            body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
        })
            .then((response) => {
                if (response.ok) {
                    alert("Password changed successfully.");
                    resetForm()
                } else {
                    return response.json().then((data) => {
                        alert(`Failed to change password: ${data.error || "Unknown error"}`);
                    });
                }
            })
            .catch((error) => {
                console.error("Error changing password:", error);
                alert("An unexpected error occurred.");
            });
    });
});

function resetForm() {
    document.getElementById("old-password").value = "";
    document.getElementById("new-password").value = "";
    document.getElementById("confirm-new-password").value = "";
}