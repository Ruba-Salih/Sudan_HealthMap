# Sudan Health Map

## Overview

**Sudan Health Map** is a health management and disease tracking system designed to provide a comprehensive view of health statistics across different states of Sudan. The platform supports supervisors and hospitals with features such as disease tracking, state statistics, and hospital statistics.


### Features

## User Roles and Accounts
- **Supervisor Account**:
  - **Manage Hospitals**: Add, update, and manage hospitals under their supervision.
  - **Supervisory Reports**: Access summary reports of hospitals and diseases, including detailed case tracking in supervised hospitals.
  - **State Reports**: Monitor and compare statistics across states, track hospital performance, and analyze disease trends within each state.

- **Hospital Account**:
  - **Manage Cases**: Log, update, and track individual cases with comprehensive details such as patient demographics, symptoms, and outcomes.
  - **Hospital Reports**: Generate summaries of cases specific to the hospital, including recoveries, deaths, and active cases.

### Disease Tracking
- Record cases with detailed attributes, including:
  - Patient demographics (age, sex, etc.).
  - Symptoms and severity.
  - Diagnosis and treatment outcomes.
- Monitor disease spread across hospitals and states.

### State Statistics
- Visualize the prevalence and trends of diseases in each state.
- Analyze and compare health trends across multiple states using interactive reports.

### Hospital Statistics
- View summaries of the most common diseases, recoveries, deaths, and active cases.
- Interactive charts such as bar charts, line charts, and pie charts for insightful visualizations.
- Breakdown of cases by disease and date to track hospital-specific trends.

### Reporting and Analytics
- **Supervisory Reports**: Detailed insights into state-wide hospital performance and disease management.
- **Hospital-Specific Reports**: Focused summaries for individual hospitals, showcasing case trends and outcomes.
- **State and Disease Reports**: Cross-hospital comparisons and state-wide disease tracking.

### Dashboard Visualizations
- Graphical representations of:
  - Disease prevalence and recovery rates.
  - State-wide comparisons and trends.
  - Hospital-specific insights for effective decision-making.

### User-Friendly Management
- Centralized dashboard for managing hospitals, cases, and reports.
- Real-time updates and insights for better health data management.
- Designed for both supervisors and hospitals to streamline operations and improve decision-making.


## Technologies Used

- **Backend**: python Django, Django REST Framework
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker

---

## Deployment

1. **Install Docker Desktop **:
Ensure Docker Desktop is installed on your system:
[Download Here](https://www.docker.com/products/docker-desktop)

2. **Clone the Repository**:

```bash
git clone https://github.com/Ruba-Salih/Sudan_HealthMap.git
```

```bash
cd Sudan_HealthMap
```

3. **Start the Containers**: 
```bash
    docker compose up --build
```

4. **Apply Database Migrations**:
```bash
    docker compose exec web python manage.py migrate
```

- **Load Default Data (Optional)**:
```bash
    docker compose exec web python manage.py loaddata data.json
```

5. **Access the Application**:
- http://localhost:8000

### Authors
- Ruba Salih Adam - [GitHub](https://github.com/Ruba-Salih)
