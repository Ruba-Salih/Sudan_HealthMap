const API_BASE_URL = "/supervisor/api/diseases/"; // Update with the actual API endpoint

// Initialize and fetch all diseases on page load
document.addEventListener("DOMContentLoaded", () => {
    fetchDiseases(); // Fetch all diseases when the page loads
});

// Fetch and display all diseases
async function fetchDiseases() {
    try {
        const response = await fetch(API_BASE_URL);
        if (response.ok) {
            const diseases = await response.json();
            displayDiseases(diseases); // Display all diseases
        } else {
            console.error("Failed to fetch diseases:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Search and display diseases based on a query
async function searchDiseases(event) {
    event.preventDefault();
    const query = document.getElementById("search-query").value.toLowerCase();

    try {
        const response = await fetch(API_BASE_URL);
        if (response.ok) {
            const diseases = await response.json();
            const filteredDiseases = diseases.filter((disease) =>
                disease.name.toLowerCase().includes(query) ||
                disease.description.toLowerCase().includes(query)
            );
            displayDiseases(filteredDiseases); // Display filtered diseases
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
    list.innerHTML = ""; // Clear previous items

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
            fetchDiseases(); // Refresh the list after adding
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
            fetchDiseases(); // Refresh the list after deleting
        } else {
            console.error("Failed to delete disease:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Show update form inline
function showUpdateForm(id, currentName, currentDescription) {
    const updateForm = document.createElement("form");
    updateForm.innerHTML = `
        <label for="update-name-${id}">Disease Name:</label>
        <input type="text" id="update-name-${id}" value="${currentName}" required>
        <br>
        <label for="update-description-${id}">Description:</label>
        <textarea id="update-description-${id}" required>${currentDescription}</textarea>
        <br>
        <button onclick="updateDisease(event, ${id})">Update Disease</button>
    `;

    const listItem = [...document.getElementById("disease-list").children].find(
        (li) => li.innerHTML.includes(`onclick="deleteDisease(${id})"`)
    );

    listItem.appendChild(updateForm);
}

// Update a disease
async function updateDisease(event, id) {
    event.preventDefault();
    const name = document.getElementById(`update-name-${id}`).value;
    const description = document.getElementById(`update-description-${id}`).value;

    try {
        const response = await fetch(`${API_BASE_URL}${id}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ name, description }),
        });

        if (response.ok) {
            alert("Disease updated successfully!");
            fetchDiseases(); // Refresh the list after updating
        } else {
            const errorData = await response.json();
            alert("Error: " + JSON.stringify(errorData));
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
