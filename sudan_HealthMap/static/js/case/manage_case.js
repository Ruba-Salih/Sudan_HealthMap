// Global API Endpoints
const API_ENDPOINTS = {
    diseases: "/disease/api/", // Endpoint to fetch diseases
    cases: "/case/api/", // Endpoint to manage cases
};

// Authorization Token
if (typeof API_TOKEN === "undefined") {
    const API_TOKEN = "{{ token }}"; // Replace dynamically from backend template
}

document.addEventListener("DOMContentLoaded", () => {
    if (!API_TOKEN || API_TOKEN === "{{ token }}") {
        console.error("API Token is missing or invalid.");
        alert("Authorization token is not provided. Please log in again.");
        return;
    }

    populateDiseaseDropdown();
    fetchAndDisplayCases();
    attachFormSubmitHandler();
    attachSearchHandler();
});

// Populate disease dropdown
function populateDiseaseDropdown() {
    fetch(API_ENDPOINTS.diseases, {
        headers: {
            Authorization: `Token ${API_TOKEN}`,
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to fetch diseases: ${response.statusText}`);
            }
            return response.json();
        })
        .then((data) => {
            const diseaseDropdown = document.getElementById("disease");
            diseaseDropdown.innerHTML = "";
            data.forEach((disease) => {
                const option = document.createElement("option");
                option.value = disease.id;
                option.textContent = disease.name;
                diseaseDropdown.appendChild(option);
            });
        })
        .catch((error) => {
            console.error("Error fetching diseases:", error);
            alert("Error fetching diseases. Please check your connection.");
        });
}

// Add or Update a case
function attachFormSubmitHandler() {
    const form = document.getElementById("manage-case-form");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        data.disease = parseInt(data.disease); // Send disease ID
        data.alive = document.getElementById("alive").checked;

        const method = form.dataset.editing ? "PUT" : "POST";
        const endpoint =
            method === "PUT"
                ? `${API_ENDPOINTS.cases}${form.dataset.caseId}/`
                : API_ENDPOINTS.cases;

        try {
            const response = await fetch(endpoint, {
                method,
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${API_TOKEN}`,
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Case submitted successfully!");
                form.reset();
                delete form.dataset.editing;
                delete form.dataset.caseId;
                fetchAndDisplayCases(); // Refresh the list of cases
            } else {
                const errorData = await response.json();
                console.error("Error submitting case:", errorData);
                alert("Error: " + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error("Unexpected error:", error);
            alert("An unexpected error occurred while submitting the case.");
        }
    });
}

// Fetch and display cases
function fetchAndDisplayCases(query = "") {
    fetch(API_ENDPOINTS.cases, {
        headers: {
            Authorization: `Token ${API_TOKEN}`,
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to fetch cases: ${response.statusText}`);
            }
            return response.json();
        })
        .then((cases) => {
            const caseList = document.getElementById("case-list");
            caseList.innerHTML = "";

            if (cases.length === 0) {
                caseList.innerHTML = "<li>No cases found.</li>";
                return;
            }

            cases
                .filter(
                    (c) =>
                        c.patient_number.toString().includes(query) ||
                        c.disease_name.toLowerCase().includes(query.toLowerCase())
                )
                .forEach((caseItem) => {
                    const listItem = document.createElement("li");
                    listItem.innerHTML = `
                        Patient Number: ${caseItem.patient_number}, 
                        Disease Name: ${caseItem.disease_name || "N/A"}, 
                        Status: ${caseItem.patient_status}
                        <button onclick="editCase(${caseItem.id})">Edit</button>
                        <button onclick="deleteCase(${caseItem.id})">Delete</button>
                    `;
                    caseList.appendChild(listItem);
                });
        })
        .catch((error) => {
            console.error("Error fetching cases:", error);
            alert("Error fetching cases. Please check your connection.");
        });
}

// Search cases
function attachSearchHandler() {
    const searchForm = document.getElementById("search-case-form");
    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const query = document.getElementById("search-query").value;
        fetchAndDisplayCases(query);
    });
}

// Delete a case
function deleteCase(caseId) {
    if (!confirm("Are you sure you want to delete this case?")) return;

    fetch(`${API_ENDPOINTS.cases}${caseId}/`, {
        method: "DELETE",
        headers: {
            Authorization: `Token ${API_TOKEN}`,
        },
    })
        .then((response) => {
            if (response.ok) {
                alert("Case deleted successfully!");
                fetchAndDisplayCases();
            } else {
                console.error("Error deleting case");
                alert("Failed to delete the case. Please try again.");
            }
        })
        .catch((error) => {
            console.error("Unexpected error:", error);
            alert("An unexpected error occurred while deleting the case.");
        });
}

// Edit a case
function editCase(caseId) {
    fetch(`${API_ENDPOINTS.cases}${caseId}/`, {
        headers: {
            Authorization: `Token ${API_TOKEN}`,
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to fetch case: ${response.statusText}`);
            }
            return response.json();
        })
        .then((caseData) => {
            const form = document.getElementById("manage-case-form");
            Object.keys(caseData).forEach((key) => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = caseData[key];
            });
            form.dataset.editing = true;
            form.dataset.caseId = caseId;
        })
        .catch((error) => {
            console.error("Error fetching case:", error);
            alert("Failed to fetch case for editing. Please try again.");
        });
}
