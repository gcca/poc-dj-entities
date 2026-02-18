# Campaigns API

A Django REST API for managing event sales campaigns and their configurations.

## Features

- ✅ **JWT Authentication** - Secure API with JSON Web Tokens
- ✅ **Campaign Management** - Create and manage event sales campaigns
- ✅ **Settings Configuration** - Customizable settings for each campaign
- ✅ **OpenAPI Documentation** - Interactive docs with Swagger UI and Redoc
- ✅ **Comprehensive Testing** - Full test suite with 29 tests
- ✅ **Test Data** - Sample data for development and testing

## Quick Start

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt
# or with pdm
pdm install

# Run migrations
python manage.py migrate

# Create test data
python create_test_data.py
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Run Server
```bash
python manage.py runserver
```

### 4. Access API

**Documentation:**
- Swagger UI: http://localhost:8000/api/docs/
- Redoc: http://localhost:8000/api/redoc/

**API Endpoints:**
- `POST /api/token/` - Get JWT tokens
- `GET /api/campaigns/campaign/` - List campaigns
- `GET /api/campaigns/setting/` - List settings

## API Usage

### Authentication
```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "youruser", "password": "yourpass"}'

# Use token in requests
curl http://localhost:8000/api/campaigns/campaign/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Sample Data
The `create_test_data.py` script creates:
- **5 Campaigns**: Music Festival, Tech Conference, Food & Wine Expo, etc.
- **9 Settings**: Various pricing configurations

## Testing

```bash
# Run all tests
python manage.py test campaigns

# Run specific test class
python manage.py test campaigns.tests.CampaignModelTest
```

## Project Structure

```
campaigns/
├── models.py          # Campaign and Setting models
├── serializers.py     # DRF serializers
├── views.py          # API ViewSets
├── urls.py           # URL routing
├── tests.py          # Comprehensive test suite
├── AGENTS.md         # AI Agent documentation
└── admin.py          # Django admin configuration

create_test_data.py   # Test data creation script
```

## Technologies

- **Django 6.0** - Web framework
- **Django REST Framework** - API framework
- **Simple JWT** - JWT authentication
- **DRF Spectacular** - OpenAPI documentation
- **SQLite** - Database (configurable)
