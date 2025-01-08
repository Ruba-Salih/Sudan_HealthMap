



// not working







console.log("manage_hospitals.js is executing.");
const API_BASE_URL = "/supervisor/api/hospitals/"; // API for hospitals
const STATES_API_URL = "/supervisor/api/states/"; // API for fetching states

console.log("Script is loaded and executing.");
document.addEventListener("DOMContentLoaded", () => {
    if (typeof API_TOKEN === "undefined" || !API_TOKEN) {
        console.error("Authorization token is not provided.");
        alert("Authorization token is missing. Please log in again.");
        return;
    }
    console.log("DOM fully loaded and parsed.");

    fetchHospitals();
    fetchStates();
});

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

// Display hospitals in the hospital list
function displayHospitals(hospitals) {
    const list = document.getElementById("hospital-list");
    list.innerHTML = "";

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
                <button onclick="showUpdateForm(${hospital.id}, '${hospital.name}', '${hospital.state}', '${hospital.address || ""}')">Edit</button>
            </div>
        `;
        list.appendChild(li);
    });
}

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

// Add hospital
async function addHospital(event) {
    event.preventDefault();
    const name = document.getElementById("name").value.trim();
    const state = document.getElementById("state").value;
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !state || !username || !password) {
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
            body: JSON.stringify({ name, state, username, password }),
        });

        if (response.ok) {
            alert("Hospital added successfully!");
            document.getElementById("add-hospital-form").reset();
            fetchHospitals();
        } else {
            const errorData = await response.json();
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Error adding hospital:", error);
    }
}


// Delete a hospital
async function deleteHospital(hospitalId) {
    if (!confirm("Are you sure you want to delete this hospital?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}${hospitalId}/`, {
            method: "DELETE",
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });

        if (response.ok) {
            alert("Hospital deleted successfully!");
            fetchHospitals();
        } else {
            console.error("Failed to delete hospital:", response.statusText);
        }
    } catch (error) {
        console.error("Error deleting hospital:", error);
    }
}

// Show update form for a specific hospital
function showUpdateForm(hospitalId, currentName, currentState, currentAddress) {
    document.getElementById("name").value = currentName;
    document.getElementById("state").value = currentState;
    document.getElementById("address").value = currentAddress || "";

    document.getElementById("add-hospital-btn").style.display = "none";
    document.getElementById("update-hospital-btn").style.display = "block";

    const updateButton = document.getElementById("update-hospital-btn");
    updateButton.onclick = async (event) => {
        event.preventDefault();

        const updatedName = document.getElementById("name").value.trim();
        const updatedState = document.getElementById("state").value;
        const updatedAddress = document.getElementById("address").value.trim();

        if (!updatedName || !updatedState) {
            alert("Name and state are required!");
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}${hospitalId}/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Token ${API_TOKEN}`,
                },
                body: JSON.stringify({
                    name: updatedName,
                    state: updatedState,
                    address: updatedAddress,
                }),
            });

            if (response.ok) {
                alert("Hospital updated successfully!");
                fetchHospitals();
                resetForm();
            } else {
                const errorData = await response.json();
                alert("Error: " + JSON.stringify(errorData));
            }
        } catch (error) {
            console.error("Error updating hospital:", error);
        }
    };
}

// Reset the form and buttons
function resetForm() {
    document.getElementById("name").value = "";
    document.getElementById("state").value = "";
    document.getElementById("address").value = "";

    document.getElementById("add-hospital-btn").style.display = "block";
    document.getElementById("update-hospital-btn").style.display = "none";
}

// Search hospitals
async function searchHospitals(event) {
    event.preventDefault();
    const query = document.getElementById("search-query").value.toLowerCase();

    try {
        const response = await fetch(API_BASE_URL, {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });
        if (response.ok) {
            const hospitals = await response.json();
            const filteredHospitals = hospitals.filter((hospital) =>
                hospital.name.toLowerCase().includes(query) ||
                hospital.state.toLowerCase().includes(query) ||
                (hospital.address && hospital.address.toLowerCase().includes(query))
            );

            displayHospitals(filteredHospitals);
        } else {
            console.error("Failed to fetch hospitals:", response.statusText);
        }
    } catch (error) {
        console.error("Error searching hospitals:", error);
    }
}
