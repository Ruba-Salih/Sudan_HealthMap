console.log("API Token successfully loaded.");
document.addEventListener("DOMContentLoaded", () => {
    const hospitalDropdown = document.getElementById("hospital");
    const simpleReportTable = document.getElementById("simple-report-table").querySelector("tbody");
    const detailedReportTable = document.getElementById("detailed-report-table").querySelector("tbody");

    let defaultHospitalId = null;

    // Fetch and populate hospitals
    fetch("/supervisor/api/hospitals/", {
        headers: { Authorization: `Token ${API_TOKEN}` },
    })
        .then((response) => {
            if (!response.ok) throw new Error("Failed to fetch hospitals");
            return response.json();
        })
        .then((hospitals) => {
            if (hospitals.length === 0) {
                alert("No hospitals available.");
                return;
            }

            // Populate the dropdown and set the default hospital
            hospitals.forEach((hospital, index) => {
                const option = document.createElement("option");
                option.value = hospital.id;
                option.textContent = hospital.name;
                hospitalDropdown.appendChild(option);

                if (index === 0) {
                    defaultHospitalId = hospital.id;
                }
            });

            // Automatically load the default hospital's report
            if (defaultHospitalId) {
                loadHospitalReports(defaultHospitalId);
            }
        })
        .catch((error) => {
            console.error("Error fetching hospitals:", error);
            alert("Failed to load hospitals. Please try again later.");
        });

    // Fetch and display hospital reports
    document.getElementById("hospital-report-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const hospitalId = hospitalDropdown.value || defaultHospitalId;
        if (!hospitalId) {
            alert("Please select a hospital.");
            return;
        }
        loadHospitalReports(hospitalId);
    });

    // Load hospital reports
    function loadHospitalReports(hospitalId) {
        // Fetch simple report
        fetch(`/supervisor/api/reports/hospital/${hospitalId}/simple/`, {
            headers: { Authorization: `Token ${API_TOKEN}` },
        })
            .then((response) => {
                if (!response.ok) throw new Error(`Failed to fetch simple report: ${response.status}`);
                return response.json();
            })
            .then((data) => {
                simpleReportTable.innerHTML = data
                    .map((row) => `<tr><td>${row.disease__name}</td><td>${row.cases}</td></tr>`)
                    .join("");
            })
            .catch((error) => {
                console.error("Error fetching simple report:", error);
                simpleReportTable.innerHTML = "<tr><td colspan='2'>No data available</td></tr>";
            });

        // Fetch detailed report
        fetch(`/supervisor/api/reports/hospital/${hospitalId}/detailed/`, {
            headers: { Authorization: `Token ${API_TOKEN}` },
        })
            .then((response) => {
                if (!response.ok) throw new Error("Failed to fetch detailed report");
                return response.json();
            })
            .then((data) => {
                detailedReportTable.innerHTML = data
                    .map(
                        (row) =>
                            `<tr>
                                <td>${row.patient_number}</td>
                                <td>${row.patient_age}</td>
                                <td>${row.patient_sex}</td>
                                <td>${row.patient_blood_type || "-"}</td>
                                <td>${row.disease__name}</td>
                                <td>${row.patient_status}</td>
                                <td>${row.main_symptom_causing_death || "-"}</td>
                                <td>${row.season}</td>
                                <td>${row.date_reported}</td>
                            </tr>`
                    )
                    .join("");
            })
            .catch((error) => {
                console.error("Error fetching detailed report:", error);
                detailedReportTable.innerHTML =
                    "<tr><td colspan='9'>No data available</td></tr>";
            });
    }

    // Download simple report
    document.getElementById("download-simple-report").addEventListener("click", () => {
        const hospitalId = hospitalDropdown.value || defaultHospitalId;
        if (!hospitalId) {
            alert("Please select a hospital.");
            return;
        }
        window.location.href = `/supervisor/reports/hospital/${hospitalId}/simple/download/`;
    });

    // Download detailed report
    document.getElementById("download-detailed-report").addEventListener("click", () => {
        const hospitalId = hospitalDropdown.value || defaultHospitalId;
        if (!hospitalId) {
            alert("Please select a hospital.");
            return;
        }
        window.location.href = `/supervisor/reports/hospital/${hospitalId}/detailed/download/`;
    });
});
