const API_BASE_URL = "/supervisor/api/diseases/";

// Initialize and fetch all diseases on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchDiseases(); // Fetch all diseases when the page loads
});

// Fetch and display all diseases
async function fetchDiseases() {
    try {
        const response = await fetch(API_BASE_URL, {
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });
        if (response.ok) {
            const diseases = await response.json();
            displayDiseases(diseases);
        } else {
            console.error("Failed to fetch diseases:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Display diseases in the disease list
function displayDiseases(diseases) {
    const list = document.getElementById("disease-list");
    list.innerHTML = "";

    if (diseases.length === 0) {
        list.innerHTML = "<li>No diseases found.</li>";
        return;
    }

    diseases.forEach((disease) => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${disease.name}</strong>: ${disease.description}
            <div class="actions">
                <button onclick="deleteDisease(${disease.id})">Delete</button>
                <button onclick="showUpdateForm(${disease.id}, '${disease.name}', '${disease.description}')">Edit</button>
            </div>
        `;
        list.appendChild(li);
    });
}

// Add a new disease
async function addDisease(event) {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    try {
        const response = await fetch(API_BASE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ name, description }),
        });

        if (response.ok) {
            alert("Disease added successfully!");
            document.getElementById("add-disease-form").reset();
            fetchDiseases();
        } else {
            const errorData = await response.json();
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Delete a disease
async function deleteDisease(id) {
    if (!confirm("Are you sure you want to delete this disease?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}${id}/`, {
            method: "DELETE",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
        });

        if (response.ok) {
            alert("Disease deleted successfully!");
            fetchDiseases();
        } else {
            console.error("Failed to delete disease:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
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
