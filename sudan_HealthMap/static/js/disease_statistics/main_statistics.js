document.addEventListener('DOMContentLoaded', function () {

    const diseaseDropdown = document.getElementById('disease-dropdown');
    const filterCategory = document.getElementById('filter-category');
    const filterButton = document.getElementById('filter-button');
    const filteredDataChartCtx = document.getElementById('filteredDataChart').getContext('2d');
    let filteredDataChart;

    fetch('/statistics/api/statistics/', {
        headers: {
            'Authorization': `Token ${API_TOKEN}`
        }
    })
    
        .then(response => response.json())
        .then(data => {

            // Validate data structure
            if (!data.common_diseases || !data.unique_states) {
                console.error("Invalid data structure received.");
                alert("Error loading data. Please try again later.");
                return;
            }

            updateSeasonalChart(data.seasonal_stats);

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
                        backgroundColor: ["#41beb4", "#e7b04b", "#d3d5c3", "#e1866b", "#988067"]
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

            // Populate Filter Disease Dropdown
            data.common_diseases.forEach(disease => {
                const option = document.createElement('option');
                option.value = disease.disease__name;
                option.textContent = disease.disease__name;
                diseaseDropdown.appendChild(option);
            });

            // Set Default Filter Disease and Filter Category
            if (data.common_diseases.length > 0) {
                diseaseDropdown.value = data.common_diseases[0].disease__name;
            }
            filterCategory.value = 'age';

            // Populate State Dropdown and Set Default State
            const stateDropdown = document.getElementById('state-dropdown');
            const defaultState = "khartoum";

            data.unique_states.forEach(state => {
                const option = document.createElement('option');
                option.value = state.name;
                option.textContent = state.name;
                if (state.name.toLowerCase() === defaultState.toLowerCase()) {
                    option.selected = true;
                }
                stateDropdown.appendChild(option);
            });

            // Set default state
            const defaultStateOption = [...stateDropdown.options].find(
                option => option.value.toLowerCase() === defaultState.toLowerCase()
            );
            if (defaultStateOption) {
                defaultStateOption.selected = true;
                loadStateStatistics(defaultStateOption.value);
            } else {
                    console.warn(`Default state "${defaultState}" not found in the dropdown.`);
            }

            // State Selection
            stateDropdown.addEventListener('change', function () {
                loadStateStatistics(this.value);
            });

            // Function to Load State Statistics
            function loadStateStatistics(selectedState) {
                const stateDiseaseStatsTable = document.getElementById('state-disease-stats-table');
                stateDiseaseStatsTable.innerHTML = `
                    <tr>
                        <th>Disease</th>
                        <th>Total Cases</th>
                        <th>Total Deaths</th>
                    </tr>
                `;

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

            // Populate Disease Dropdown for Pie Chart and Set Default Disease
            const diseasePieDropdown = document.getElementById('disease-pie-dropdown');
            const uniqueDiseases = Array.from(new Set(data.state_disease_stats.map(stat => stat.disease__name)));
            const defaultDisease = uniqueDiseases[0];

            uniqueDiseases.forEach(disease => {
                const option = document.createElement('option');
                option.value = disease;
                option.textContent = disease;
                if (disease === defaultDisease) {
                    option.selected = true;
                }
                diseasePieDropdown.appendChild(option);
            });

            // Create and Update Pie Chart
            const pieChartCtx = document.getElementById('diseasePieChart').getContext('2d');
            let pieChart;

            function updatePieChart(disease) {
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
                            backgroundColor: ['#ffdb80', '#41beb4', '#ee7a44', '#ce8a4b', '#9966FF'],
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

            updatePieChart(defaultDisease);

            diseasePieDropdown.addEventListener('change', function () {
                updatePieChart(this.value);
            });


            function updateFilteredChart(disease, category) {
                if (!disease || !category) {
                    alert("Please select both a disease and a filter category.");
                    return;
                }

                fetch(`/statistics/api/cases/?disease=${disease}&filter=${category}`)
                    .then(response => response.json())
                    .then(filteredData => {
                        if (!filteredData || filteredData.length === 0) {
                            alert("No data available for the selected disease and filter.");
                            return;
                        }

                        // Prepare Data
                        const labels = filteredData.map(item => item.label);
                        const values = filteredData.map(item => item.count);

                        if (filteredDataChart) {
                            filteredDataChart.destroy();
                        }

                        filteredDataChart = new Chart(filteredDataChartCtx, {
                            type: 'bar',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: `Distribution of ${category} for ${disease}`,
                                    data: values,
                                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: { display: true, position: 'top' }
                                },
                                scales: {
                                    x: {
                                        title: {
                                            display: true,
                                            text: category.charAt(0).toUpperCase() + category.slice(1)
                                        }
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: 'Frequency'
                                        },
                                        beginAtZero: true,
                                        ticks: {
                                            stepSize: 1,
                                            precision: 0
                                        }
                                    }
                                }
                            }
                        });
                    })
                    .catch(error => console.error('Error fetching filtered data:', error));
            }

            function updateSeasonalChart(seasonalStats) {
                const labels = Object.keys(seasonalStats);
                const datasets = [];

                const allDiseases = [...new Set(labels.flatMap(season => seasonalStats[season].map(item => item.disease)))];

                allDiseases.forEach(disease => {
                    const data = labels.map(season => {
                        const entry = seasonalStats[season].find(item => item.disease === disease);
                        return entry ? entry.total_cases : 0;
                    });

                    datasets.push({
                        label: disease,
                        data: data,
                        backgroundColor: randomColor(),
                        borderColor: randomColor(),
                        borderWidth: 1
                    });
                });

                const seasonalChartCtx = document.getElementById("seasonalChart").getContext("2d");
                new Chart(seasonalChartCtx, {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: datasets
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: "top"
                            },
                            tooltip: {
                                callbacks: {
                                    label: function (context) {
                                        return `${context.dataset.label}: ${context.raw} cases`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: "Season"
                                }
                            },
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: "Number of Cases"
                                }
                            }
                        }
                    }
                });
            }

            // Utility for random colors (=
            function randomColor() {
                const r = Math.floor(Math.random() * 255);
                const g = Math.floor(Math.random() * 255);
                const b = Math.floor(Math.random() * 255);
                return `rgba(${r}, ${g}, ${b}, 0.6)`;
            }

            // Add Event Listener for Filter and Disease Selection
            filterButton.addEventListener('click', function () {
                const selectedDisease = diseaseDropdown.value;
                const selectedCategory = filterCategory.value;
                updateFilteredChart(selectedDisease, selectedCategory);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
