# Star Wars API Platform

A production-ready REST API that provides enhanced access to Star Wars universe data with authentication, caching, filtering, and analytics.

## 🚀 Features

- **Complete Star Wars Data**: Access to characters, films, starships, planets, vehicles, and species
- **Advanced Filtering**: Filter by multiple parameters (gender, homeworld, climate, etc.)
- **Sorting & Pagination**: Order results and paginate for performance
- **Correlated Queries**: Get characters in a film, pilots of a starship, etc.
- **Statistics & Comparison**: Aggregate stats and compare entities
- **Firebase Authentication**: Secure endpoints with JWT tokens
- **Smart Caching**: Two-tier caching for optimal performance
- **OpenAPI Documentation**: Interactive Swagger UI

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **HTTP Client**: httpx (async)
- **Auth**: Firebase Auth
- **Cache**: Firestore
- **Deployment**: GCP Cloud Functions + API Gateway

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/starwars-api.git
cd starwars-api

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
copy .env.example .env
# Edit .env with your configuration
```

## 🏃 Running Locally

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --port 8000

# Open API docs
# http://localhost:8000/docs
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_people_service.py -v
```

## 📚 API Endpoints

### People
- `GET /api/v1/people` - List all characters
- `GET /api/v1/people/{id}` - Get character by ID
- `GET /api/v1/people/{id}/films` - Get character's films
- `GET /api/v1/people/{id}/starships` - Get character's starships

### Films
- `GET /api/v1/films` - List all films
- `GET /api/v1/films/{id}` - Get film by ID
- `GET /api/v1/films/{id}/characters` - Get film's characters

### Starships
- `GET /api/v1/starships` - List all starships
- `GET /api/v1/starships/{id}` - Get starship by ID
- `GET /api/v1/starships/compare` - Compare starships

### Planets
- `GET /api/v1/planets` - List all planets
- `GET /api/v1/planets/{id}` - Get planet by ID
- `GET /api/v1/planets/{id}/residents` - Get planet's residents

### Statistics
- `GET /api/v1/statistics/overview` - Universe statistics
- `GET /api/v1/statistics/films` - Film statistics

## 🔒 Authentication

The API uses Firebase Authentication. Include the JWT token in requests:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/people
```

## 📝 License

MIT License
