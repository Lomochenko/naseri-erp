# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a comprehensive ERP (Enterprise Resource Planning) system for Naseri Hardware Store, built as a Persian (Farsi) RTL application. The system manages products, inventory, sales, purchases, accounting, and provides comprehensive reporting capabilities.

**Technology Stack:**
- **Backend**: Django 5.0.7 + Django REST Framework (Python-based RESTful API)
- **Frontend**: Vue.js 3 + Tailwind CSS + Headless UI (modern, responsive UI)
- **Database**: PostgreSQL (production) / SQLite (development fallback)
- **Authentication**: Token-based authentication with Django REST Framework

## Development Commands

### Backend (Django)
```powershell
# Navigate to backend directory
cd backend

# Set up Python virtual environment
python -m venv venv
.\\venv\\Scripts\\Activate.ps1  # PowerShell
# venv\\Scripts\\activate       # CMD

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test products
python manage.py test inventory
python manage.py test sales

# Run comprehensive end-to-end tests
python manage.py test users.tests_e2e

# Create sample data for development
python create_sample_data.py
python populate_erp_data.py

# Check data integrity
python check_data.py
```

### Frontend (Vue.js)
```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint and fix code issues
npm run lint

# Format code
npm run format
```

### Full System Setup
```powershell
# Quick setup for development (Windows batch script)
backend\\setup_and_run.bat
```

### Testing Commands
```powershell
# Backend API testing
cd backend
python test_api.py
python test_api_endpoints.py
python test_direct_api.py
python test_inventory.py
python test_products_api.py
python test_sale_api.py

# Root-level comprehensive tests
python comprehensive_test.py
python final_test.py
python simple_test.py
python test_erp_system.py
python test_frontend_backend.py
python test_inventory_system.py
```

## Architecture Overview

### Backend Architecture (Django)

The backend follows Django's modular app structure with clear separation of concerns:

**Core Apps:**
- `users/` - Custom user authentication with phone number as username, role-based access control (RBAC)
- `products/` - Product management with categories, units, pricing, and soft delete capability
- `inventory/` - Inventory tracking with transaction-based stock management
- `sales/` - Sales management including customers, invoices, and payments
- `purchases/` - Purchase management with suppliers and purchase orders
- `accounting/` - Financial management with journal transactions and account management
- `reporting/` - Business intelligence and report generation
- `audit/` - Audit trail and change tracking for compliance

**Key Patterns:**
- **Soft Delete**: Users and products use `is_deleted` flag instead of hard deletion
- **Audit Trail**: Models include `created_at`, `updated_at`, `created_by`, `updated_by` fields
- **Custom Managers**: ProductManager and UserManager filter out soft-deleted records by default
- **Token Authentication**: REST API uses token-based authentication for frontend communication
- **CORS Enabled**: Configured for frontend-backend communication
- **API Documentation**: Auto-generated Swagger/OpenAPI docs at `/swagger/` and `/redoc/`

**Database Design:**
- PostgreSQL primary database with custom user model using phone numbers
- Persian timezone (Asia/Tehran) and language configuration
- RESTful API endpoints under `/api/` namespace
- Token authentication with session fallback

### Frontend Architecture (Vue.js)

Modern Vue.js 3 application with composition API and RTL support:

**Tech Stack:**
- Vue.js 3 with Composition API
- Pinia for state management
- Vue Router for navigation
- Tailwind CSS + Headless UI for styling (no Materio/Vuetify)
- Vite for build tooling and hot reloading

**Key Features:**
- RTL (Right-to-Left) layout optimized for Persian language
- Responsive design for mobile, tablet, and desktop
- Persian date picker integration
- ApexCharts for data visualization
- Modern ES6+ JavaScript with component-based architecture
- Custom composables for reusable logic (`useSidebar.js`)

**Project Structure:**
- `src/main.js` - Application entry point with plugin setup
- `src/App.vue` - Root component
- `src/router/` - Vue Router configuration
- `src/composables/` - Reusable composition functions
- `src/icons/` - Custom SVG icon components

### System Integration

**API Communication:**
- Frontend communicates with backend via RESTful APIs
- Base API URL configured through `VITE_API_URL` environment variable
- Token-based authentication stored and managed by frontend
- CORS configured to allow frontend-backend communication

**Development Workflow:**
- Backend runs on `localhost:8000` (Django dev server)
- Frontend runs on `localhost:5173` (Vite dev server)
- Hot reloading enabled for both frontend and backend development
- Comprehensive test suites for both layers

## Development Guidelines

### Authentication & Users
- Custom user model uses phone numbers instead of usernames
- Role-based permissions (regular users, managers, admins)
- Token authentication for API access
- Default admin: phone `09122173180`, password `Admin@123`
- Default manager: phone `09123456788`, password `Manager@123`

### Business Logic
- All monetary values stored as decimals without decimal places (Iranian Rial)
- Stock management through transaction-based inventory system
- Soft delete pattern for maintaining data integrity
- Comprehensive audit trail for all business-critical operations
- Persian calendar support with Tehran timezone

### Code Standards
- Follow Django REST Framework conventions for API endpoints
- Use Vue.js 3 Composition API pattern for frontend components
- Persian/Farsi language support throughout the application
- Consistent error handling and validation
- Comprehensive test coverage for business logic

### Environment Setup
- Backend requires Python 3.8+ and PostgreSQL
- Frontend requires Node.js 16+ and npm 8+
- Environment variables managed through `.env` files
- Local development uses SQLite, production uses PostgreSQL

## API Documentation

When backend is running, access comprehensive API documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **OpenAPI JSON**: `http://127.0.0.1:8000/swagger.json/`
- **OpenAPI YAML**: `http://127.0.0.1:8000/swagger.yaml/`

Main API endpoints available under `/api/`:
- `/api/users/` - User management and authentication
- `/api/products/` - Product and category management
- `/api/inventory/` - Inventory and stock management
- `/api/sales/` - Sales, customers, and invoices
- `/api/purchases/` - Purchase orders and suppliers
- `/api/accounting/` - Financial transactions
- `/api/reports/` - Business reports and analytics
- `/api/audit/` - Audit trail and system logs

## Regional Settings

- **Language**: Persian (fa-ir)
- **Timezone**: Asia/Tehran
- **Date Format**: Persian calendar (jYYYY/jMM/jDD)
- **Currency**: Iranian Rial (stored as integers)
- **Text Direction**: Right-to-Left (RTL)
- **Default Font**: Vazir