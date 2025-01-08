console.log("API Token successfully loaded.");
document.addEventListener("DOMContentLoaded", () => {
    const stateDropdown = document.getElementById("state");
    const stateReportTable = document.getElementById("state-report-table").querySelector("tbody");
    const defaultStateName = "Khartoum";

    // Fetch and populate states
    fetch("/supervisor/api/states/", {
        headers: { Authorization: `Token ${API_TOKEN}` },
    })
        .then((response) => response.json())
        .then((states) => {
            let defaultStateId = null;

            states.forEach((state) => {
                const option = document.createElement("option");
                option.value = state.id;
                option.textContent = state.name;
                stateDropdown.appendChild(option);

                if (state.name.toLowerCase() === defaultStateName.toLowerCase()) {
                    defaultStateId = state.id;
                }
            });

            if (defaultStateId) {
                stateDropdown.value = defaultStateId;

                fetchStateReport(defaultStateId);
            }
        });

    document.getElementById("state-report-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const stateId = stateDropdown.value;
        if (!stateId) {
            alert("Please select a state.");
            return;
        }

        fetchStateReport(stateId);
    });

    // Function to fetch state report
    function fetchStateReport(stateId) {
        fetch(`/supervisor/api/reports/state/${stateId}/`, {
            headers: { Authorization: `Token ${API_TOKEN}` },
        })
            .then((response) => response.json())
            .then((data) => {
                stateReportTable.innerHTML = data
                    .map((row) => `<tr><td>${row.hospital__name}</td><td>${row.disease__name}</td><td>${row.cases}</td></tr>`)
                    .join("");
            })
            .catch((error) => {
                console.error("Error fetching state report:", error);
                stateReportTable.innerHTML = "<tr><td colspan='3'>No data available</td></tr>";
            });
    }

    // For downloading the report
    document.getElementById("download-state-report").addEventListener("click", () => {
        const stateId = stateDropdown.value;
        if (!stateId) {
            alert("Please select a state.");
            return;
        }
        window.location.href = `/supervisor/reports/state/${stateId}/download/`;
    });
});
