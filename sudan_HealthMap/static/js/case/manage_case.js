const API_ENDPOINTS = {
    diseases: "/disease/api/",
    cases: "/case/api/",
};

if (typeof API_TOKEN === "undefined") {
    const API_TOKEN = "{{ token }}";
}

document.addEventListener("DOMContentLoaded", () => {
    if (!API_TOKEN || API_TOKEN === "{{ token }}") {
        console.error("API Token is missing or invalid.");
        alert("Authorization token is not provided. Please log in again.");
        return;
    }

    const caseTableBody = document.getElementById("case-list");

    populateDiseaseDropdown();
    fetchAndDisplayCases();
    attachFormSubmitHandler();
    attachSearchHandler();

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
            data.disease = parseInt(data.disease);
            

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
                    fetchAndDisplayCases();
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
                caseTableBody.innerHTML = "";

                if (cases.length === 0) {
                    caseTableBody.innerHTML = "<tr><td colspan='9'>No cases found.</td></tr>";
                    return;
                }

                cases
                    .filter(
                        (c) =>
                            c.patient_number.toString().includes(query) ||
                            c.disease_name.toLowerCase().includes(query.toLowerCase())
                    )
                    .forEach((caseItem) => {
                        const row = `
                            <tr>
                                <td>${caseItem.disease_name || "-"}</td>
                                <td>${caseItem.patient_number || "-"}</td>
                                <td>${caseItem.patient_age || "-"}</td>
                                <td>${caseItem.patient_sex || "-"}</td>
                                <td>${caseItem.patient_blood_type || "-"}</td>
                                <td>${caseItem.patient_status || "-"}</td>
                                <td>${caseItem.main_symptom_causing_death || "-"}</td>
                                <td>${caseItem.season || "-"}</td>
                                <td>
                                    <button class="edit-button btn-secondary" data-id="${caseItem.id}">Edit</button>
                                    <button class="delete-button btn-primary" data-id="${caseItem.id}">Delete</button>
                                </td>
                            </tr>
                        `;
                        caseTableBody.insertAdjacentHTML("beforeend", row);
                    });

                // Attach event listeners to buttons after rendering
                document.querySelectorAll(".edit-button").forEach((button) =>
                    button.addEventListener("click", () => {
                        const caseId = button.dataset.id;
                        updateCase(caseId);
                    })
                );

                document.querySelectorAll(".delete-button").forEach((button) =>
                    button.addEventListener("click", () => {
                        const caseId = button.dataset.id;
                        deleteCase(caseId);
                    })
                );
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

    // Update a case
    function updateCase(caseId) {
    
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
});
