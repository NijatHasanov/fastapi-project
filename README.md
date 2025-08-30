# FastAPI Production-Ready Backend

A production-ready FastAPI backend with comprehensive features including JWT authentication, role-based access control, PostgreSQL integration, and cloud-ready configuration.

## 🌟 Features

- **Authentication & Authorization**
  - JWT authentication with access and refresh tokens
  - Role-based access control (Admin/Viewer roles)
  - Password complexity validation
  - Token refresh mechanism
  - Rate limiting for sensitive endpoints

- **Database Integration**
  - PostgreSQL with async SQLAlchemy
  - Automatic migrations with Alembic
  - Connection pooling and retry mechanisms
  - Health check monitoring

- **Cloud-Ready Configuration**
  - Environment-based configuration
  - Docker and Docker Compose setup
  - Gunicorn with Uvicorn workers
  - Health check endpoints
  - Structured JSON logging

- **Security**
  - CORS configuration
  - Password hashing with bcrypt
  - Rate limiting
  - Security headers
  - Non-root Docker user

- **Development Tools**
  - OpenAPI documentation
  - Pytest-based testing
  - Cross-platform compatibility
  - Development reload support

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/NijatHasanov/fastapi-project.git
   cd fastapi-project
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start development server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Deployment

1. **Build and start services**
   ```bash
   docker-compose up --build -d
   ```

2. **Check logs**
   ```bash
   docker-compose logs -f
   ```

3. **Access the API**
   ```
   http://localhost:8000/docs
   ```

## 🔑 Authentication

### Obtain Access Token
```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=adminpass"
```

### Refresh Token
```bash
curl -X POST http://localhost:8000/refresh-token \
  -H "Authorization: Bearer $REFRESH_TOKEN"
```

## 🛣️ API Endpoints

### Public Endpoints
- `POST /token` - Obtain access token
- `POST /refresh-token` - Refresh access token
- `GET /health` - Service health check

### Protected Endpoints
#### Room Data (Authentication Required)
- `GET /api/v1/room/{room_id}/latest` - Get latest room data
- `POST /api/v1/data` - Create room data (Admin only)
- `GET /api/v1/data/all` - List all room data

#### User Management (Admin Only)
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## ⚙️ Configuration

### Environment Variables

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=fastapi_db

# Security Settings
JWT_SECRET=your-super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Settings
CORS_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO
WORKERS_COUNT=4
```

## 🐳 Docker Configuration

### Production Setup
```yaml
services:
  web:
    build: .
    environment:
      - DB_HOST=db
    deploy:
      replicas: 2
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 📚 Development Guide

### Project Structure
```
fastapi-project/
├── app/
│   ├── models/         # Pydantic & SQLAlchemy models
│   ├── routes/         # API endpoints
│   ├── auth/          # Authentication & permissions
│   ├── config.py      # Configuration management
│   └── main.py        # Application entry point
├── migrations/        # Alembic migrations
├── tests/            # Test files
├── Dockerfile        # Production container
└── docker-compose.yaml
```

### Adding New Endpoints
1. Create route in appropriate file under `app/routes/`
2. Add required permissions in `app/auth/permissions.py`
3. Update tests in `tests/`
4. Update documentation

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔐 Security Best Practices

1. **Password Storage**
   - Passwords are hashed using bcrypt
   - Minimum complexity requirements enforced

2. **Authentication**
   - JWT with short-lived access tokens
   - Refresh token rotation
   - Rate limiting on auth endpoints

3. **Authorization**
   - Role-based access control
   - Granular permissions
   - Admin role protection

4. **API Security**
   - CORS configuration
   - Rate limiting
   - Input validation
   - SQL injection protection

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push branch (`git push origin feature/name`)
5. Create Pull Request

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 👥 Authors

- Nijat Hasanov ([@NijatHasanov](https://github.com/NijatHasanov))
# fastapi-project
