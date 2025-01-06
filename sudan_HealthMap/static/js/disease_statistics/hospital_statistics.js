const API_ENDPOINT = "/statistics/api/hospital/statistics/";
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch(API_ENDPOINT, {
            headers: {
                Authorization: `Token ${API_TOKEN}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();

        populateChartsAndTables(data);
    } catch (error) {
        console.error("Error fetching hospital statistics:", error);
        alert("Failed to load hospital statistics. Please try again later.");
    }
});

function populateChartsAndTables(data) {
    if (!data) {
        console.error("No data received.");
        return;
    }

    const commonTableBody = document.querySelector("#common-diseases-table tbody");
    commonTableBody.innerHTML = "";
    data.common_disease.forEach(disease => {
        const row = `<tr>
                        <td>${disease.disease__name}</td>
                        <td>${disease.total_cases}</td>
                    </tr>`;
        commonTableBody.insertAdjacentHTML("beforeend", row);
    });

    // Populate Recovered Diseases Table
    const recoveredTableBody = document.querySelector("#recovered-diseases-table tbody");
    recoveredTableBody.innerHTML = "";
    data.recovered_disease.forEach(disease => {
        const row = `<tr>
                        <td>${disease.disease__name}</td>
                        <td>${disease.total_recovered}</td>
                    </tr>`;
        recoveredTableBody.insertAdjacentHTML("beforeend", row);
    });

    // Populate Deaths Diseases Table
    const deathTableBody = document.querySelector("#death-diseases-table tbody");
    deathTableBody.innerHTML = "";
    data.death_disease.forEach(disease => {
        const row = `<tr>
                        <td>${disease.disease__name}</td>
                        <td>${disease.total_deaths}</td>
                    </tr>`;
        deathTableBody.insertAdjacentHTML("beforeend", row);
    });

    // Populate Rate of Disease Spread Table
    const dailyStatsTableBody = document.querySelector("#daily-stats-table tbody");
    dailyStatsTableBody.innerHTML = "";
    data.daily_stats.forEach(stat => {
        const row = `<tr>
                        <td>${stat.date_reported}</td>
                        <td>${stat.disease__name}</td>
                        <td>${stat.daily_change * -1|| "-"}</td>
                        <td>${stat.rate_of_change ? stat.rate_of_change.toFixed(2) : "-"}</td>
                    </tr>`;
        dailyStatsTableBody.insertAdjacentHTML("beforeend", row);
    });

    // Update Charts (if applicable)
    updateCharts(data);
}

function updateCharts(data) {
    // Recovery Donut Chart
    const recoveryCtx = document.getElementById("recovery-donut-chart").getContext("2d");
    new Chart(recoveryCtx, {
        type: "doughnut",
        data: {
            labels: data.recovered_disease.map(d => d.disease__name),
            datasets: [{
                data: data.recovered_disease.map(d => d.total_recovered),
                backgroundColor: ['#ffdb80', '#41beb4', '#ee7a44', '#ce8a4b', '#9966FF'],
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
            },
        },
    });

    // Death Donut Chart
    const deathCtx = document.getElementById("death-donut-chart").getContext("2d");
    new Chart(deathCtx, {
        type: "doughnut",
        data: {
            labels: data.death_disease.map(d => d.disease__name),
            datasets: [{
                data: data.death_disease.map(d => d.total_deaths),
                backgroundColor: [ "#988067", "#e1866b", "#41beb4", "#e7b04b", "#d3d5c3"],
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
            },
        },
    });

    // Rate of Disease Spread Line Chart
    const rateCtx = document.getElementById("rate-line-chart").getContext("2d");
    new Chart(rateCtx, {
        type: "line",
        data: {
            labels: data.daily_stats.map(stat => stat.date_reported),
            datasets: [{
                label: "New Cases",
                data: data.daily_stats.map(stat => stat.daily_change),
                borderColor: "#42a5f5",
                fill: true,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Date",
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: "New Cases",
                    },
                },
            },
        },
    });
}
