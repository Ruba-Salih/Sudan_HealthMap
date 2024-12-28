// Example JavaScript for Supervisor Dashboard

// Fetch and log diseases (Optional dynamic handling for diseases)
async function fetchDiseases() {
    try {
        const response = await fetch("/api/diseases/");
        if (response.ok) {
            const diseases = await response.json();
            console.log("Diseases:", diseases); // Log diseases for testing
        } else {
            console.error("Error fetching diseases:", response.statusText);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
}

// Call fetchDiseases if needed
// fetchDiseases();
