const API_BASE_URL = "/supervisor/api/hospitals/"; // API for hospitals
const STATES_API_URL = "/supervisor/api/states/"; // API for fetching states

document.addEventListener("DOMContentLoaded", () => {
    fetchHospitals(); // Fetch all hospitals
    fetchStates(); // Fetch states for dropdown
});

async function fetchStates() {
    try {
        const response = await fetch(STATES_API_URL);
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

async function fetchHospitals() {
    try {
        const response = await fetch(API_BASE_URL);
        if (response.ok) {
            const hospitals = await response.json();
            displayHospitals(hospitals);
        } else {
            console.error("Failed to fetch hospitals:", response.statusText);
        }
    } catch (error) {
        console.error("Error fetching hospitals:", error);
    }
}

function displayHospitals(hospitals) {
    const list = document.getElementById("hospital-list");
    list.innerHTML = "";
    hospitals.forEach((hospital) => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${hospital.name}</strong>: ${hospital.state_name}
            <div class="actions">
                <button onclick="deleteHospital(${hospital.id})">Delete</button>
                <button onclick="showUpdateForm(${hospital.id}, '${hospital.name}', '${hospital.state}')">Edit</button>
            </div>
        `;
        list.appendChild(li);
    });
}

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

    try {
        const response = await fetch(API_BASE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ name, state, username, password }),
        });

        if (response.ok) {
            alert("Hospital added successfully!");
            fetchHospitals();
            document.getElementById("add-hospital-form").reset();
        } else {
            const errorData = await response.json();
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error("Error adding hospital:", error);
    }
}

async function deleteHospital(hospitalId) {
    try {
        const response = await fetch(`${API_BASE_URL}${hospitalId}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
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

function showUpdateForm(hospitalId, name, state, address) {
    document.getElementById("name").value = name;
    document.getElementById("state").value = state; // Ensure state dropdown uses correct value
    document.getElementById("address").value = address || ""; // Pre-fill address or use empty string

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
                    "X-CSRFToken": getCookie("csrftoken"),
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

function resetForm() {
    document.getElementById("name").value = "";
    document.getElementById("state").value = "";
    document.getElementById("address").value = "";

    document.getElementById("add-hospital-btn").style.display = "block";
    document.getElementById("update-hospital-btn").style.display = "none";
}

async function searchHospitals(event) {
    event.preventDefault();
    const query = document.getElementById("search-query").value.toLowerCase();

    try {
        const response = await fetch(API_BASE_URL);
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
