const API_BASE_URL = "/supervisor/api/diseases/";

document.addEventListener("DOMContentLoaded", () => {
    if (typeof API_TOKEN === "undefined" || !API_TOKEN) {
        console.error("Authorization token is not provided.");
        alert("Authorization token is missing. Please log in again.");
        return;
    }

    fetchAndDisplayDiseases();
});

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

// Fetch and display diseases
async function fetchAndDisplayDiseases(query = "") {
    try {
        const response = await fetch(API_BASE_URL, {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch diseases: ${response.statusText}`);
        }

        const diseases = await response.json();
        const filteredDiseases = diseases.filter(
            (disease) =>
                disease.name.toLowerCase().includes(query.toLowerCase()) ||
                disease.description.toLowerCase().includes(query.toLowerCase())
        );

        const tableBody = document.getElementById("disease-table-body");
        tableBody.innerHTML = "";

        if (filteredDiseases.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="3">No diseases found.</td></tr>`;
            return;
        }

        filteredDiseases.forEach((disease) => {
            const row = `
                <tr>
                    <td>${disease.name || "N/A"}</td>
                    <td>${disease.description || "N/A"}</td>
                    <td>
                        <button class='btn-secondary' onclick="showUpdateForm(${disease.id}, '${disease.name}', '${disease.description}')">Edit</button>
                        <button class='btn-primary' onclick="deleteDisease(${disease.id})">Delete</button>
                    </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        console.error("Error fetching diseases:", error);
    }
}

// Search diseases
function searchDiseases(event) {
    event.preventDefault();
    const query = document.getElementById("search-query").value.trim();
    fetchAndDisplayDiseases(query);
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
                Authorization: `Token ${API_TOKEN}`,
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ name, description }),
        });

        if (response.ok) {
            alert("Disease added successfully!");
            document.getElementById("add-disease-form").reset();
            fetchAndDisplayDiseases();
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
                Authorization: `Token ${API_TOKEN}`,
                "X-CSRFToken": csrfToken,
            },
        });

        if (response.ok) {
            alert("Disease deleted successfully!");
            fetchAndDisplayDiseases();
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
                    Authorization: `Token ${API_TOKEN}`,
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ name: updatedName, description: updatedDescription }),
            });

            if (response.ok) {
                alert("Disease updated successfully!");
                fetchAndDisplayDiseases();
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

// Reset the form and buttons
function resetForm() {
    document.getElementById("name").value = "";
    document.getElementById("description").value = "";

    document.getElementById("add-disease-btn").style.display = "block";
    document.getElementById("update-disease-btn").style.display = "none";
}
