document.addEventListener("DOMContentLoaded", async () => {
    const API_ENDPOINTS = {
        diseases: "/disease/api/",
        reports: "/hospital/api/hospital/reports/",
    };

    const diseaseSelect = document.getElementById("disease-select");
    const reportTableBody = document.querySelector("#report-table tbody");
    const downloadButton = document.getElementById("download-report");

    // Fetch and populate diseases in the dropdown
    async function fetchDiseases() {
        try {
            const response = await fetch(API_ENDPOINTS.diseases, {
                headers: { Authorization: `Token ${API_TOKEN}` },
            });

            if (!response.ok) throw new Error("Failed to fetch diseases.");

            const diseases = await response.json();
            diseaseSelect.innerHTML = "";
            diseases.forEach((disease, index) => {
                const option = document.createElement("option");
                option.value = disease.id;
                option.textContent = disease.name;
                if (index === 0) option.selected = true; 
                diseaseSelect.appendChild(option);
            });

            if (diseases.length > 0) {
                fetchReports(diseases[0].id);
            }
        } catch (error) {
            console.error("Error fetching diseases:", error);
            alert("Failed to load diseases.");
        }
    }

    // Fetch cases for the selected disease
    async function fetchReports(diseaseId) {
        try {
            const response = await fetch(`${API_ENDPOINTS.reports}?disease_id=${diseaseId}`, {
                headers: { Authorization: `Token ${API_TOKEN}` },
            });

            if (!response.ok) throw new Error("Failed to fetch reports.");

            const cases = await response.json();
            displayReports(cases);
        } catch (error) {
            console.error("Error fetching reports:", error);
            alert("Failed to load reports.");
        }
    }

    function displayReports(cases) {
        reportTableBody.innerHTML = "";
        cases.forEach((caseItem) => {
            const row = `
                <tr>
                    <td>${caseItem.patient_number}</td>
                    <td>${caseItem.patient_age}</td>
                    <td>${caseItem.patient_sex}</td>
                    <td>${caseItem.patient_blood_type}</td>
                    <td>${caseItem.patient_status}</td>
                    <td>${caseItem.main_symptom_causing_death || "-"}</td>
                    <td>${caseItem.season}</td>
                </tr>
            `;
            reportTableBody.insertAdjacentHTML("beforeend", row);
        });

        downloadButton.style.display = cases.length > 0 ? "block" : "none";
    }

    // Download the report
    downloadButton.addEventListener("click", () => {
        const rows = Array.from(reportTableBody.querySelectorAll("tr"));
        const csvContent = [
            ["Patient Number", "Age", "Sex", "Blood Type", "Status", "Symptom", "Season"],
            ...rows.map((row) =>
                Array.from(row.querySelectorAll("td")).map((td) => td.textContent)
            ),
        ]
            .map((row) => row.join(","))
            .join("\n");

        const blob = new Blob([csvContent], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "hospital_report.csv";
        a.click();
    });

    // Handle disease change
    diseaseSelect.addEventListener("change", (event) => {
        const diseaseId = event.target.value;
        if (diseaseId) fetchReports(diseaseId);
    });

    await fetchDiseases();
});
