document.addEventListener('DOMContentLoaded', function () {
    const diseaseDropdown = document.getElementById('disease-dropdown');
    const filterCategory = document.getElementById('filter-category');
    const filterButton = document.getElementById('filter-button');
    const filteredDataChartCtx = document.getElementById('filteredDataChart').getContext('2d');
    let filteredDataChart;

    // Function to dynamically update the histogram based on the selected filter
    function updateCustomHistogram(disease, category) {
        if (!disease || !category) {
            alert("Please select both a disease and a filter category.");
            return;
        }

        fetch(`/statistics/api/cases/?disease=${disease}&filter=${category}`)
            .then(response => response.json())
            .then(filteredData => {
                if (filteredData.length === 0) {
                    alert("No data available for the selected filters.");
                    return;
                }

                let labels = [];
                let values = [];

                // Determine X (labels) and Y (values) based on the selected category
                switch (category) {
                    case 'age':
                        labels = Array.from(new Set(filteredData.map(item => item.label))).sort((a, b) => a - b);
                        values = labels.map(label => filteredData.filter(item => item.label === label).length);
                        break;
                    case 'sex':
                        labels = ['Male', 'Female'];
                        values = labels.map(label => filteredData.filter(item => item.label === label).length);
                        break;
                    case 'season':
                        labels = Array.from(new Set(filteredData.map(item => item.label)));
                        values = labels.map(label => filteredData.filter(item => item.label === label).length);
                        break;
                    case 'blood_type':
                        labels = Array.from(new Set(filteredData.map(item => item.label)));
                        values = labels.map(label => filteredData.filter(item => item.label === label).length);
                        break;
                    case 'main_symptom':
                        labels = Array.from(new Set(filteredData.map(item => item.label)));
                        values = labels.map(label => filteredData.filter(item => item.label === label).length);
                        break;
                    default:
                        alert("Invalid filter category.");
                        return;
                }

                // Adjust Y-axis increments to be multiples of 5
                const maxValue = Math.max(...values);
                const yMax = Math.ceil(maxValue / 5) * 5;

                // Update the chart
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
                                    stepSize: 5,
                                    max: yMax
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching filtered data:', error));
    }

    // Add event listener to the button
    filterButton.addEventListener('click', function () {
        const selectedDisease = diseaseDropdown.value;
        const selectedCategory = filterCategory.value;
        updateCustomHistogram(selectedDisease, selectedCategory);
    });
});
