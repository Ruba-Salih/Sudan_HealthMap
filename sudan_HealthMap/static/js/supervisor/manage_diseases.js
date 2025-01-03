console.log("manage_diseases.js is executing.");
const API_BASE_URL = "/supervisor/api/diseases/"; // API for diseases

document.addEventListener("DOMContentLoaded", () => {
    if (typeof API_TOKEN === "undefined" || !API_TOKEN) {
        console.error("Authorization token is not provided.");
        alert("Authorization token is missing. Please log in again.");
        return;
    }
    console.log("DOM fully loaded and parsed.");

    fetchDiseases(); // Fetch all diseases when the page loads
});

// Helper function to get CSRF token
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].split("=");
            if (cookie[0] === "csrftoken") {
                cookieValue = decodeURIComponent(cookie[1]);
                break;
            }
        }
    }
    return cookieValue;
}

// Fetch and display all diseases
async function fetchDiseases() {
    try {
        const response = await fetch(API_BASE_URL, {
            headers: {
                Authorization: `Token ${API_TOKEN}`, // Use Token Authentication
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

    if (!diseases || diseases.length === 0) {
        list.innerHTML = "<li>No diseases found.</li>";
        return;
    }

    diseases.forEach((disease) => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>Disease Name: ${disease.name}</strong> Description: ${disease.description}
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
    const name = document.getElementById("name").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!name || !description) {
        alert("Both fields are required!");
        return;
    }

    const csrfToken = getCSRFToken();

    try {
        const response = await fetch(API_BASE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${API_TOKEN}`, // Use Token Authentication
                "X-CSRFToken": csrfToken, // Include CSRF token
            },
            body: JSON.stringify({ name, description }),
        });

        if (response.ok) {
            alert("Disease added successfully!");
            document.getElementById("add-disease-form").reset();
            fetchDiseases(); // Refresh the disease list
        } else {
            const errorData = await response.json();
            console.error("Error adding disease:", errorData);
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Delete a disease
async function deleteDisease(id) {
    if (!confirm("Are you sure you want to delete this disease?")) return;

    const csrfToken = getCSRFToken();

    try {
        const response = await fetch(`${API_BASE_URL}${id}/`, {
            method: "DELETE",
            headers: {
                Authorization: `Token ${API_TOKEN}`, // Use Token Authentication
                "X-CSRFToken": csrfToken, // Include CSRF token
            },
        });

        if (response.ok) {
            alert("Disease deleted successfully!");
            fetchDiseases(); // Refresh the disease list
        } else {
            console.error("Failed to delete disease:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Show update form for a specific disease
function showUpdateForm(diseaseId, currentName, currentDescription) {
    document.getElementById("name").value = currentName;
    document.getElementById("description").value = currentDescription;

    document.getElementById("add-disease-btn").style.display = "none";
    document.getElementById("update-disease-btn").style.display = "block";

    const updateButton = document.getElementById("update-disease-btn");
    updateButton.onclick = async (event) => {
        event.preventDefault();

        const updatedName = document.getElementById("name").value.trim();
        const updatedDescription = document.getElementById("description").value.trim();

        if (!updatedName || !updatedDescription) {
            alert("Both fields are required!");
            return;
        }

        const csrfToken = getCSRFToken();

        try {
            const response = await fetch(`${API_BASE_URL}${diseaseId}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${API_TOKEN}`, // Use Token Authentication
                    "X-CSRFToken": csrfToken, // Include CSRF token
                },
                body: JSON.stringify({ name: updatedName, description: updatedDescription }),
            });

            if (response.ok) {
                alert("Disease updated successfully!");
                fetchDiseases(); // Refresh the disease list
                resetForm();
            } else {
                const errorData = await response.json();
                console.error("Error updating disease:", errorData);
                alert("Error: " + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error("Unexpected error:", error);
        }
    };
}

// Reset the form and toggle buttons
function resetForm() {
    document.getElementById("name").value = "";
    document.getElementById("description").value = "";

    document.getElementById("add-disease-btn").style.display = "block";
    document.getElementById("update-disease-btn").style.display = "none";
}
