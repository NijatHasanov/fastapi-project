# FastAPI MVP Backend

A production-ready FastAPI backend with JWT authentication, PostgreSQL database, and structured logging.

## Features

- FastAPI with OpenAPI documentation
- JWT authentication with role-based access
- PostgreSQL database with async SQLAlchemy
- Structured JSON logging
- Docker and Docker Compose setup
- Pytest-based testing
- CORS support
- Cross-platform compatibility (macOS, Windows, Linux)

## Quick Start

### 1. Clone the repository

```bash
# Using HTTPS
git clone https://github.com/YOUR_USERNAME/fastapi-project.git

# Using SSH
git clone git@github.com:YOUR_USERNAME/fastapi-project.git

cd fastapi-project
```

### 2. Set up Virtual Environment

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### On Windows:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Command Prompt)
venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
# On all platforms
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
# On macOS/Linux
cp .env.example .env

# On Windows (PowerShell)
Copy-Item .env.example .env

# On Windows (Command Prompt)
copy .env.example .env
```

5. Run the development server:

```bash
# Basic usage (all platforms)
uvicorn app.main:app --reload

# To specify host and port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# For better performance on multi-core systems
uvicorn app.main:app --workers 2 --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for the OpenAPI documentation.

## Docker Setup

### Prerequisites

- Docker Desktop for Windows/Mac
- Docker Engine for Linux

### Running with Docker Compose

```bash
# Build and start services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Endpoints

- `GET /` - Root endpoint (requires authentication)
- `POST /api/v1/data` - Create room data (requires admin role)
- `GET /api/v1/data/all` - Get all room data (requires authentication)

## Testing

Run the tests with:

```bash
pytest
```

## Development

1. The project uses FastAPI with async endpoints
2. Authentication is handled via JWT tokens
3. Logging is structured in JSON format
4. CORS is configured via environment variables

## Environment Variables

- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `DB_URL` - PostgreSQL connection URL
- `JWT_SECRET` - Secret key for JWT tokens
- `LOG_LEVEL` - Logging level (default: INFO)

## License

MIT
# fastapi-project
