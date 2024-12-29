// Global API Endpoints
const API_ENDPOINTS = {
    diseases: '/disease/api/', // Endpoint for diseases
    cases: '/case/api/', // Endpoint for cases
};

document.addEventListener("DOMContentLoaded", () => {
    populateDiseaseDropdown();
    attachFormSubmitHandler();
});

// Fetch diseases and populate the disease dropdown
function populateDiseaseDropdown() {
    fetch(API_ENDPOINTS.diseases)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to fetch diseases: ${response.statusText}`);
            }
            return response.json();
        })
        .then((data) => {
            const diseaseDropdown = document.getElementById("disease");
            diseaseDropdown.innerHTML = ""; // Clear existing options
            data.forEach((disease) => {
                const option = document.createElement("option");
                option.value = disease.id;
                option.textContent = disease.name;
                diseaseDropdown.appendChild(option);
            });
        })
        .catch((error) => {
            console.error("Error fetching diseases:", error);
            alert("Error loading diseases. Please try again later.");
        });
}

// Attach event listener to handle form submission
function attachFormSubmitHandler() {
    const form = document.getElementById("manage-case-form");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.alive = document.getElementById("alive").checked;

        try {
            const response = await fetch(API_ENDPOINTS.cases, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Case submitted successfully!");
                form.reset(); // Clear the form after submission
            } else {
                const errorData = await response.json();
                console.error("Error submitting case:", errorData);
                if (errorData.hospital) {
                    alert("Error: Hospital information is missing. Please contact support.");
                } else {
                    alert("Error: " + JSON.stringify(errorData));
                }
            }
        } catch (error) {
            console.error("Unexpected error:", error);
            alert("An unexpected error occurred. Please try again later.");
        }
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
