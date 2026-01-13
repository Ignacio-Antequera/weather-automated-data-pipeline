# Weather Data ELT Pipeline

An automated ELT (Extract, Load, Transform) pipeline that ingests live weather data from an API and creates a near-realtime dashboard for data visualization and analysis.

## 📋 Project Overview

This project demonstrates a complete data engineering workflow using modern tools and best practices. The pipeline automatically:
1. **Extracts** weather data from [Weatherstack API](https://weatherstack.com/)
2. **Loads** raw data into a PostgreSQL database
3. **Transforms** data using dbt for analytics
4. **Visualizes** insights through Apache Superset dashboards

The entire pipeline is orchestrated by Apache Airflow, running every minute to provide near-realtime weather analytics.

**API Provider**: This project uses the [Weatherstack API](https://weatherstack.com/) free tier (100 API calls/month).

## 🏗️ Architecture

```
Weather API → Airflow DAG → PostgreSQL (Raw) → dbt (Transform) → PostgreSQL (Staging/Marts) → Superset Dashboard
```

**Data Flow:**
1. **Airflow** triggers the orchestration DAG on a schedule (every 1 minute)
2. **Python script** fetches weather data from the API
3. **Raw data** is inserted into PostgreSQL `raw_weather_data` table
4. **dbt** transforms raw data into staging and mart layers
5. **Superset** connects to the transformed data for visualization

## 🛠️ Technologies Used

| Tool | Version | Purpose |
|------|---------|---------|
| **Apache Airflow** | 3.0.0 | Workflow orchestration and scheduling |
| **dbt** | 1.9.0 | Data transformation and modeling |
| **PostgreSQL** | 15.15 | Relational database |
| **Apache Superset** | 3.0.0 | Business intelligence and visualization |
| **Docker** | Latest | Containerization |
| **Docker Compose** | Latest | Multi-container orchestration |
| **Python** | 3.10+ | API requests and data ingestion |
| **Redis** | 7.4.7 | Caching for Superset |

## 📦 Prerequisites

### System Requirements
- **OS**: Windows with WSL2 (Ubuntu 24.04) or Linux
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: At least 10GB free

### Required Software
- [Docker](https://docs.docker.com/get-docker/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0+)
- WSL2 (for Windows users)
- [Weatherstack API Key](https://weatherstack.com/product) (Free tier available)

### Verify Installation
```bash
docker --version
docker-compose --version
```

### API Setup
1. Sign up for a free account at [Weatherstack](https://weatherstack.com/signup/free)
2. Get your API key from the dashboard
3. Update the API key in `api-request/api_request.py`

**Note**: The free tier provides 100 API calls per month. With the default 1-minute schedule, the free quota will be consumed in ~1.5 hours. Consider adjusting the schedule in `airflow/dags/orchestrator.py` to a longer interval (e.g., every 15 minutes or hourly).

## 🚀 Getting Started

### 1. Clone the Repository
```bash
cd ~/repos
git clone https://github.com/Ignacio-Antequera/weather-automated-data-pipeline.git weather-data-project
cd weather-data-project
```

### 2. Start All Services
```bash
docker-compose up
```

This will start:
- ✅ PostgreSQL database (port 5000)
- ✅ Airflow webserver & scheduler (port 8000)
- ✅ dbt container (on-demand)
- ✅ Superset (port 8088)
- ✅ Redis cache

**Note**: First startup may take 5-10 minutes to pull images and initialize databases.

### 3. Access the Applications

#### Airflow Web UI
- **URL**: http://localhost:8000
- **Username**: `admin`
- **Password**: Check the terminal logs on first startup (looks like: `Password for user 'admin': XXXXXXXXXX`)

#### Superset Dashboard
- **URL**: http://localhost:8088
- **Username**: `admin`
- **Password**: `admin`

### 4. Trigger the Pipeline

**Option A: Automatic (Recommended)**
The DAG is scheduled to run every 1 minute automatically.

**Option B: Manual Trigger**
1. Navigate to Airflow UI (http://localhost:8000)
2. Find the `weather-api-dbt-orchestrator` DAG
3. Toggle it **ON** if disabled
4. Click the **Play** button to trigger manually

### 5. Run dbt Transformations

dbt runs automatically as part of the Airflow DAG. To run manually:
```bash
docker-compose exec dbt dbt run
```

## 📁 Project Structure

```
weather-data-project/
├── docker-compose.yaml          # Multi-container configuration
├── README.md                    # This file
│
├── airflow/
│   └── dags/
│       └── orchestrator.py      # Main DAG definition
│
├── api-request/
│   ├── api_request.py          # Weather API client
│   └── insert_records.py       # Database insertion logic
│
├── dbt/
│   ├── profiles.yml            # dbt connection config
│   └── my_project/
│       ├── dbt_project.yml     # dbt project config
│       └── models/
│           ├── sources/
│           │   └── sources.yml # Raw data sources
│           └── staging/
│               └── staging.sql # Staging transformations
│
└── postgres/
    ├── airflow_init.sql        # Airflow DB initialization
    ├── superset_init.sql       # Superset DB initialization
    └── data/                   # PostgreSQL data directory (created on startup)
```

## 🎯 Usage

### Monitor the Pipeline
1. **Airflow**: View DAG runs, logs, and task status
2. **Superset**: Create charts and dashboards from transformed data
3. **PostgreSQL**: Query data directly if needed

### Stop Services
```bash
docker-compose down
```

### Stop and Remove All Data (Clean Slate)
```bash
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs airflow_container
docker-compose logs postgres_container
```

## 🔧 Configuration

### Database Connection (PostgreSQL)
- **Host**: `localhost` (from host machine) or `db` (from containers)
- **Port**: `5000`
- **Database**: `db`
- **User**: `db_user`
- **Password**: `db_password`

### Airflow Database
- **Database**: `airflow_db`
- **User**: `airflow`
- **Password**: `airflow`

### Superset Database
- **Database**: `superset_db`
- **User**: `superset`
- **Password**: `superset`

## 📊 Data Models

### Raw Layer
- **Table**: `raw_weather_data`
- **Schema**: Contains raw API response data

### Staging Layer
- **Table**: `stg_weather_data`
- **Purpose**: Cleaned and typed data

### Mart Layer
- **Tables**: Business-specific aggregations and metrics

## 🐛 Troubleshooting

### Issue: Containers won't start
```bash
# Check Docker is running
docker ps

# Restart Docker daemon (WSL)
sudo service docker restart
```

### Issue: Port already in use
```bash
# Check what's using the port
sudo lsof -i :8000  # or :5000, :8088

# Stop the process or change ports in docker-compose.yaml
```

### Issue: Permission denied on postgres/data
```bash
sudo rm -rf postgres/data
docker-compose down -v
docker-compose up
```

### Issue: Can't see Airflow password
```bash
docker logs airflow_container 2>&1 | grep "password"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

For questions or feedback, please open an issue in the repository.

---

**Built with** ❤️ **using modern data engineering tools**
