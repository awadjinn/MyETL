## Project Overview

This project implements a simple **ETL** for customer churn data.

**Workflow:**

1. **Ingest** – CSV files are loaded into a **Postgres** staging database.  
2. **Transform** – Data is cleaned, missing values filled, then stored in a **DuckDB** file for analytics.  
3. **Load / Visualization** – Transformed data is visualized using **Streamlit** dashboards.

**Tools Used:**

- **Python** – scripting the ETL process  
- **Postgres** – staging database for raw CSV data  
- **DuckDB** – lightweight OLAP database for analytics  
- **Airflow** – orchestrator 
- **Streamlit** – interactive dashboards for reporting  
- **Docker / Docker Compose** – containerization for reproducible setup


## How to Run

### Prerequisites
- Install **Git**, **Docker** and **Docker Compose**  

### Clone the repository
Clone the project repository (for demonstration purposes, the CSV and env files are included in the repo):

```bash
git clone https://github.com/awadjinn/myetl.git
cd myetl
```

### Start the services
Build and start all containers:

```bash
docker compose up -d --build
```

### Open Streamlit
In your browser, go to http://localhost:8501