console.log("manage_hospitals.js  executing.");
const API_BASE_URL = "/supervisor/api/hospitals/";
const STATES_API_URL = "/supervisor/api/states/";

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed.");

    // Check for API_TOKEN
    if (typeof API_TOKEN === "undefined" || !API_TOKEN) {
        console.error("Authorization token is not provided.");
        alert("Authorization token is missing. Please log in again.");
        return;
    }

    // Attach functions to the global window object
    window.addHospital = addHospital;
    window.deleteHospital = deleteHospital;
    window.showUpdateForm = showUpdateForm;

    fetchHospitals(); // Fetch all hospitals
    fetchStates(); // Fetch states for dropdown
});

// Helper function to get the CSRF token from cookies
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

// Add a new hospital
async function addHospital(event) {
    event.preventDefault();
    console.log("addHospital function called.");

    const nameField = document.getElementById("name");
    const stateField = document.getElementById("state");
    const emailField = document.getElementById("email");
    const passwordField = document.getElementById("password");

    // Debugging checks for fields
    if (!nameField) {
        console.error("Name input field is missing.");
        alert("Name field is not found. Please check your HTML.");
        return;
    }
    if (!stateField) {
        console.error("State dropdown is missing.");
        alert("State dropdown is not found. Please check your HTML.");
        return;
    }
    if (!emailField) {
        console.error("email input field is missing.");
        alert("email field is not found. Please check your HTML.");
        return;
    }
    if (!passwordField) {
        console.error("Password input field is missing.");
        alert("Password field is not found. Please check your HTML.");
        return;
    }

    const name = nameField.value.trim();
    const state = stateField.value;
    const email = emailField.value.trim();
    const password = passwordField.value.trim();

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
            fetchHospitals(); // Refresh hospital list
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

// Fetch and display all hospitals
async function fetchHospitals() {
    try {
        const response = await fetch(API_BASE_URL, {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });
        if (response.ok) {
            const hospitals = await response.json();
            console.log("Fetched hospitals:", hospitals);
            displayHospitals(hospitals);
        } else {
            console.error("Failed to fetch hospitals:", response.statusText);
        }
    } catch (error) {
        console.error("Error fetching hospitals:", error);
    }
}

// Display hospitals in the list
function displayHospitals(hospitals) {
    const list = document.getElementById("hospital-list");
    if (!list) {
        console.error("Hospital list element is missing.");
        return;
    }

    list.innerHTML = ""; // Clear the previous list

    if (!hospitals || hospitals.length === 0) {
        list.innerHTML = "<li>No hospitals found.</li>";
        return;
    }

    hospitals.forEach((hospital) => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>Hospital Name: ${hospital.name}</strong>State: ${hospital.state_name || "N/A"}
            <div class="actions">
                <button onclick="deleteHospital(${hospital.id})">Delete</button>
                <button onclick="showUpdateForm(${hospital.id}, '${hospital.name}', '${hospital.state}')">Edit</button>
            </div>
        `;
        list.appendChild(li);
    });
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
            fetchHospitals();
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
                fetchHospitals();
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
    const nameField = document.getElementById("name").value = "";
    const stateField = document.getElementById("state").value = "";

    if (nameField) nameField.value = "";
    if (stateField) stateField.value = "";

    document.getElementById("add-hospital-btn").style.display = "block";
    document.getElementById("update-hospital-btn").style.display = "none";
}
