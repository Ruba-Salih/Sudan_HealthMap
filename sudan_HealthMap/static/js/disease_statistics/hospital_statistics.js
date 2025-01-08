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

    const recoveredTableBody = document.querySelector("#recovered-diseases-table tbody");
    recoveredTableBody.innerHTML = "";
    data.recovered_disease.forEach(disease => {
        const row = `<tr>
                        <td>${disease.disease__name}</td>
                        <td>${disease.total_recovered}</td>
                    </tr>`;
        recoveredTableBody.insertAdjacentHTML("beforeend", row);
    });

    const deathTableBody = document.querySelector("#death-diseases-table tbody");
    deathTableBody.innerHTML = "";
    data.death_disease.forEach(disease => {
        const row = `<tr>
                        <td>${disease.disease__name}</td>
                        <td>${disease.total_deaths}</td>
                    </tr>`;
        deathTableBody.insertAdjacentHTML("beforeend", row);
    });

    updateCharts(data);
}

function updateCharts(data) {
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

    const deathCtx = document.getElementById("death-donut-chart").getContext("2d");
    new Chart(deathCtx, {
        type: "doughnut",
        data: {
            labels: data.death_disease.map(d => d.disease__name),
            datasets: [{
                data: data.death_disease.map(d => d.total_deaths),
                backgroundColor: ["#988067", "#e1866b", "#41beb4", "#e7b04b", "#d3d5c3"],
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

    const lineCtx = document.getElementById("rate-line-chart").getContext("2d");

    const diseases = Array.from(new Set(data.daily_stats.map(stat => stat.disease__name)));
    const allDates = getAllDates(data.daily_stats.map(stat => stat.date_reported));

    const datasets = diseases.map(disease => {
        const diseaseData = fillMissingData(data.daily_stats, disease, allDates);
        return {
            label: disease,
            data: diseaseData.map(stat => stat.total_cases || 0),
            borderColor: randomColor(),
            tension: 0.3,
            fill: false,
        };
    });

    new Chart(lineCtx, {
        type: "line",
        data: {
            labels: allDates,
            datasets: datasets,
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
                        text: "Total Cases",
                    },
                },
            },
        },
    });
}

// Utility function to get all dates in the data range
function getAllDates(dates) {
    const uniqueDates = Array.from(new Set(dates)).map(date => new Date(date));
    uniqueDates.sort((a, b) => a - b);

    const allDates = [];
    let currentDate = uniqueDates[0];
    const endDate = uniqueDates[uniqueDates.length - 1];

    while (currentDate <= endDate) {
        allDates.push(currentDate.toISOString().split("T")[0]);
        currentDate.setDate(currentDate.getDate() + 1);
    }

    return allDates;
}

// Utility function to fill missing data for a disease
function fillMissingData(dailyStats, disease, allDates) {
    const diseaseData = dailyStats.filter(stat => stat.disease__name === disease);
    const filledData = allDates.map(date => {
        const existingStat = diseaseData.find(stat => stat.date_reported === date);
        return existingStat || { date_reported: date, total_cases: 0 };
    });
    return filledData;
}

// Utility function for random colors
function randomColor() {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return `rgba(${r}, ${g}, ${b}, 1)`;
}
