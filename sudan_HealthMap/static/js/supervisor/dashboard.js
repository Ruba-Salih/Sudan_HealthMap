if (typeof API_TOKEN === 'undefined' || !API_TOKEN || API_TOKEN === "{{ token }}") {
    console.error("API Token is missing or invalid.");
    alert("Authorization token is not provided. Please log in again.");
} else {
    console.log("API Token successfully loaded.");
    fetchDiseases();
}

// Fetch and log diseases
async function fetchDiseases() {
    try {
        const response = await fetch("/supervisor/api/diseases/", {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });
        if (response.ok) {
            const diseases = await response.json();
            console.log("Diseases:", diseases);
        } else {
            console.error("Error fetching diseases:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}
