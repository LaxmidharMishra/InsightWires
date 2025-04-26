# Insight Wires News API

A powerful FastAPI-based news search and metadata management system that provides comprehensive news analytics and filtering capabilities.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database](#database)
- [Development](#development)
- [Data Files](#data-files)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Features

[Previous features section remains the same...]

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- PostgreSQL database
- Git
- gcc compiler (for building dependencies)
- libpq-dev (PostgreSQL development files)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd InsightWires
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y gcc libpq-dev
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory with the following variables:
```env
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
POSTGRES_HOST=your_database_host
POSTGRES_PORT=5432
POSTGRES_DB=your_database_name
```

2. Alternative Database URL Configuration:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
```

## Database

### Connection
The application uses SQLAlchemy with asyncpg for asynchronous database operations. The database connection is configured in `util/database.py`.

### Testing Database Connection
You can test the database connection using the provided utility:
```bash
python util/test_db_con.py
```

### Database Schema
The application uses several metadata tables:
- BusinessEventsMetadata
- CompaniesMetadata
- IndustriesMetadata
- LanguageMetadata
- LocationsMetadata
- NewsMetadata
- SourcesMetadata
- ThemesMetadata
- TopicsMetadata
- CustomTopicsMetadata
- TypeOfContentMetadata

## Data Files
The project includes sample data files in the `util` directory:
- `ms_sample.csv`: Microsoft news sample data
- `google_sample.csv`: Google news sample data
- `GS_sample.csv`: Goldman Sachs news sample data

## Development

### Project Structure

# InsightWires

InsightWires/
├── api/
│ ├── endpoints.py # API route definitions
│ ├── models/ # Database models
│ ├── init.py
│ ├── routers/
│ │   ├── __init__.py
│ │   ├── news.py
│ │   ├── companies.py
│ │   ├── metadata.py
│ │   └── business_events.py
│ ├── core/
│ │   ├── __init__.py
│ │   ├── security.py
│ │   ├── config.py
│ │   ├── dependencies.py
│ │   └── cache.py
│ ├── middleware/
│ │   ├── __init__.py
│ │   ├── rate_limit.py
│ │   └── compression.py
│ └── services/
│     ├── __init__.py
│     └── metadata_service.py
├── util/
│ ├── database.py # Database configuration
│ ├── test_db_con.py # Database connection test
│ └── sample data files
├── docker-compose.yml # Docker composition
├── Dockerfile # Docker build instructions
├── main.py # Application entry point
├── requirements.txt # Python dependencies
└── .env # Environment variables

# Clone repository
git clone <repository-url>
cd InsightWires

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black isort flake8

# Build and start containers
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Format code
black .
isort .

# Lint code
flake8

### Code Style
The project follows PEP 8 guidelines. We recommend using:
- black for code formatting
- isort for import sorting
- flake8 for linting

```bash
# Install development tools
pip install black isort flake8

# Format code
black .
isort .

# Check code quality
flake8
```

## Deployment

### Docker Deployment
1. Build and start services:
```bash
docker-compose up --build
```

2. For production deployment:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment
1. Set up a PostgreSQL database
2. Configure environment variables
3. Install dependencies
4. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Considerations
- Development: Uses reload mode for hot reloading
- Production: Disable reload and debug modes
- Consider using a process manager (e.g., Supervisor, PM2)

## Monitoring and Logging

### Logging Configuration
The application uses Python's built-in logging module:
- Log Level: DEBUG (configurable)
- Format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
- Logger Name: "InsightWiresFastApi"

### Monitoring
- Access logs through Docker:
```bash
docker-compose logs -f
```
- Application logs:
```bash
docker-compose logs -f app
```

## Performance Optimization

### Database Optimization
- Use appropriate indexes for frequently queried fields
- Monitor query performance
- Configure connection pooling

### Application Settings
- Adjust worker count based on available resources
- Configure connection timeouts
- Set appropriate pagination limits

## Security Considerations

1. **Environment Variables**
   - Never commit `.env` files
   - Use secure passwords
   - Rotate credentials regularly

2. **API Security**
   - Consider implementing rate limiting
   - Add authentication if needed
   - Review CORS settings

3. **Database Security**
   - Use least privilege access
   - Regular security updates
   - Backup strategy

## Troubleshooting

[Previous troubleshooting section remains the same...]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
[Add appropriate license information]
