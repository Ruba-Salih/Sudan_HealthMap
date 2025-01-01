document.addEventListener('DOMContentLoaded', function () {
    fetch('/statistics/api/statistics/')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Data:", data);

            // Validate data structure
            if (!data.common_diseases || !data.unique_states) {
                console.error("Invalid data structure received.");
                alert("Error loading data. Please try again later.");
                return;
            }

            // Populate Common Diseases Table
            const commonDiseasesTableBody = document.querySelector('#common-diseases-table tbody');
            const diseaseLabels = [];
            const diseaseCases = [];
            let totalCases = 0;

            data.common_diseases.slice(0, 10).forEach(disease => {
                diseaseLabels.push(disease.disease__name);
                diseaseCases.push(disease.total_cases);
                totalCases += disease.total_cases;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${disease.disease__name}</td>
                    <td>${disease.total_cases}</td>
                `;
                commonDiseasesTableBody.appendChild(row);
            });

            // Donut Chart
            const ctx = document.getElementById('diseaseDonutChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: diseaseLabels,
                    datasets: [{
                        data: diseaseCases.map(cases => ((cases / totalCases) * 100).toFixed(2)),
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true, position: 'top' },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw;
                                    return `${context.label}: ${value}%`;
                                }
                            }
                        }
                    }
                }
            });

            // Populate State Dropdown
            const stateDropdown = document.getElementById('state-dropdown');
            data.unique_states.forEach(state => {
                const option = document.createElement('option');
                option.value = state.name;
                option.textContent = state.name;
                stateDropdown.appendChild(option);
            });

            // Handle State Selection
            stateDropdown.addEventListener('change', function () {
                const stateDiseaseStatsTable = document.getElementById('state-disease-stats-table');
                stateDiseaseStatsTable.innerHTML = `
                    <tr>
                        <th>Disease</th>
                        <th>Total Cases</th>
                        <th>Total Deaths</th>
                    </tr>
                `;

                const selectedState = this.value;
                if (selectedState) {
                    const filteredData = data.state_disease_stats.filter(
                        stat => stat.hospital__state__name === selectedState
                    );

                    if (filteredData.length === 0) {
                        const noDataRow = document.createElement('tr');
                        noDataRow.innerHTML = `<td colspan="3">No data available for the selected state</td>`;
                        stateDiseaseStatsTable.appendChild(noDataRow);
                    } else {
                        filteredData.forEach(stat => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${stat.disease__name}</td>
                                <td>${stat.total_cases}</td>
                                <td>${stat.total_deaths}</td>
                            `;
                            stateDiseaseStatsTable.appendChild(row);
                        });
                    }
                }
            });

            // Populate Disease Dropdown for Pie Chart
            const diseasePieDropdown = document.getElementById('disease-pie-dropdown');
            const uniqueDiseases = Array.from(new Set(data.state_disease_stats.map(stat => stat.disease__name)));
            uniqueDiseases.forEach(disease => {
                const option = document.createElement('option');
                option.value = disease;
                option.textContent = disease;
                diseasePieDropdown.appendChild(option);
            });

            // Create and Update Pie Chart
            const pieChartCtx = document.getElementById('diseasePieChart').getContext('2d');
            let pieChart;

            function updatePieChart(disease) {
                if (!disease) {
                    alert("Please select a disease.");
                    return;
                }

                // Filter data by selected disease
                const filteredData = data.state_disease_stats.filter(stat => stat.disease__name === disease);

                if (filteredData.length === 0) {
                    alert("No data available for the selected disease.");
                    return;
                }

                // Prepare data for pie chart
                const stateLabels = filteredData.map(stat => stat.hospital__state__name);
                const caseCounts = filteredData.map(stat => stat.total_cases);

                // Update or create the chart
                if (pieChart) {
                    pieChart.destroy();
                }

                pieChart = new Chart(pieChartCtx, {
                    type: 'pie',
                    data: {
                        labels: stateLabels,
                        datasets: [{
                            label: `Distribution of ${disease} cases by state`,
                            data: caseCounts,
                            backgroundColor: [
                                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
                                '#E8A798', '#ADCEFA', '#B8E986', '#9B59B6'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: true, position: 'top' },
                            tooltip: { enabled: true }
                        }
                    }
                });
            }

            // Add Event Listener for Disease Pie Dropdown
            diseasePieDropdown.addEventListener('change', function () {
                const selectedDisease = this.value;
                updatePieChart(selectedDisease);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
