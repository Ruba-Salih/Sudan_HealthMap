const API_BASE_URL = "/supervisor/api/hospitals/";
const STATES_API_URL = "/supervisor/api/states/";

document.addEventListener("DOMContentLoaded", () => {
    if (typeof API_TOKEN === "undefined" || !API_TOKEN) {
        console.error("Authorization token is not provided.");
        alert("Authorization token is missing. Please log in again.");
        return;
    }

    window.addHospital = addHospital;
    window.deleteHospital = deleteHospital;
    window.showUpdateForm = showUpdateForm;
    window.searchHospitals = searchHospitals;

    fetchAndDisplayHospitals();
    fetchStates();
});

// Utility to get CSRF token
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

// Fetch and display hospitals
async function fetchAndDisplayHospitals(query = "") {
    try {
        const response = await fetch(API_BASE_URL, {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch hospitals: ${response.statusText}`);
        }

        const hospitals = await response.json();
        const filteredHospitals = hospitals.filter(
            (hospital) =>
                hospital.name.toLowerCase().includes(query.toLowerCase()) ||
                hospital.state_name.toLowerCase().includes(query.toLowerCase())
        );

        const tableBody = document.getElementById("hospital-table-body");
        if (!tableBody) {
            console.error("Hospital table body element is missing.");
            return;
        }

        tableBody.innerHTML = "";

        if (filteredHospitals.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="4">No hospitals found.</td></tr>`;
            return;
        }

        filteredHospitals.forEach((hospital) => {
            const row = `
                <tr>
                    <td>${hospital.name || "N/A"}</td>
                    <td>${hospital.state_name || "N/A"}</td>
                    <td>${hospital.email || "N/A"}</td>
                    <td>
                        <button  class='btn-secondary' onclick="deleteHospital(${hospital.id})">Delete</button>
                        <button class='btn-primary' onclick="showUpdateForm(${hospital.id}, '${hospital.name}', '${hospital.state}', '${hospital.email}')">Edit</button>
                    </td>
                </tr>
            `;
            tableBody.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        console.error("Error fetching hospitals:", error);
        alert("Error fetching hospitals. Please check your connection.");
    }
}

// Search hospitals
function searchHospitals(event) {
    event.preventDefault();
    const query = document.getElementById("search-query").value.trim();
    fetchAndDisplayHospitals(query);
}
// Add hospital
async function addHospital(event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const state = document.getElementById("state").value;
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !state || !email || !password) {
        alert("All fields are required!");
        return;
    }

    const csrfToken = getCSRFToken();

    try {
        const response = await fetch(API_BASE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                Authorization: `Token ${API_TOKEN}`,
            },
            body: JSON.stringify({
                name,
                state: parseInt(state, 10),
                email,
                password,
            }),
        });

        if (response.ok) {
            alert("Hospital added successfully!");
            document.getElementById("add-hospital-form").reset();
            fetchAndDisplayHospitals();
        } else {
            const errorData = await response.json();
            console.error("Error adding hospital:", errorData);
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Error adding hospital:", error);
    }
}

// Fetch and populate state dropdown
async function fetchStates() {
    try {
        const response = await fetch(STATES_API_URL, {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });

        if (response.ok) {
            const states = await response.json();
            const stateDropdown = document.getElementById("state");

            if (!stateDropdown) {
                console.error("State dropdown not found.");
                return;
            }

            stateDropdown.innerHTML = "<option value=''>Select State</option>";

            states.forEach((state) => {
                const option = document.createElement("option");
                option.value = state.id;
                option.textContent = state.name;
                stateDropdown.appendChild(option);
            });
        } else {
            console.error("Failed to fetch states:", response.statusText);
        }
    } catch (error) {
        console.error("Error fetching states:", error);
    }
}


// Delete a hospital
async function deleteHospital(hospitalId) {
    if (!confirm("Are you sure you want to delete this hospital?")) return;

    const csrfToken = getCSRFToken();

    try {
        const response = await fetch(`${API_BASE_URL}${hospitalId}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken,
                Authorization: `Token ${API_TOKEN}`,
            },
        });

        if (response.ok) {
            alert("Hospital deleted successfully!");
            resetForm()
            fetchAndDisplayHospitals();
        } else {
            console.error("Failed to delete hospital:", response.statusText);
        }
    } catch (error) {
        console.error("Error deleting hospital:", error);
    }
}

// Show update form
function showUpdateForm(hospitalId, currentName, currentState) {
    const nameField = document.getElementById("name");
    const stateField = document.getElementById("state");

    if (!nameField || !stateField) {
        console.error("Name or state field is missing.");
        return;
    }

    nameField.value = currentName;
    stateField.value = currentState;

    document.getElementById("add-hospital-btn").style.display = "none";
    document.getElementById("update-hospital-btn").style.display = "block";

    const updateButton = document.getElementById("update-hospital-btn");
    updateButton.onclick = async (event) => {
        event.preventDefault();

        const updatedName = nameField.value.trim();
        const updatedState = stateField.value;

        if (!updatedName || !updatedState) {
            alert("Name and state are required!");
            return;
        }

        const csrfToken = getCSRFToken();

        try {
            const response = await fetch(`${API_BASE_URL}${hospitalId}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                    Authorization: `Token ${API_TOKEN}`,
                },
                body: JSON.stringify({
                    name: updatedName,
                    state: updatedState,
                }),
            });

            if (response.ok) {
                alert("Hospital updated successfully!");
                fetchAndDisplayHospitals();
                resetForm();
            } else {
                const errorData = await response.json();
                console.error("Error updating hospital:", errorData);
                alert("Error: " + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error("Error updating hospital:", error);
        }
    };
}

// Reset the form and toggle buttons
function resetForm() {
    document.getElementById("name").value = "";
    document.getElementById("state").value = "";

    document.getElementById("add-hospital-btn").style.display = "block";
    document.getElementById("update-hospital-btn").style.display = "none";
}
