# Naseri Hardware Store ERP

A full-stack ERP system for a hardware store (یراق آلات ناصری), built with Django REST Framework and Vue.js 3.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.0.7 + Django REST Framework |
| Frontend | Vue.js 3 + Tailwind CSS + Pinia |
| Database | PostgreSQL |
| Auth | Token-based (DRF TokenAuthentication) |
| Static files | WhiteNoise |
| Web server | Nginx (production) |
| App server | Gunicorn (production) |

---

## Project Structure

```
naseri/
├── backend/                  # Django project
│   ├── naseri_erp/           # Project settings, urls, wsgi
│   ├── users/                # Custom user model (phone number login)
│   ├── products/             # Products, categories, units
│   ├── inventory/            # Warehouses, stock transactions, adjustments
│   ├── sales/                # Customers, sales, invoices, payments
│   ├── purchases/            # Suppliers, purchase orders, supplier payments
│   ├── accounting/           # Chart of accounts, journal entries, expenses
│   ├── reporting/            # Reports module
│   ├── audit/                # Activity log, notifications
│   ├── requirements.txt      # Dev dependencies
│   ├── requirements-prod.txt # Prod dependencies (includes gunicorn)
│   └── .env.example          # Environment variables template
├── frontend/                 # Vue.js 3 project
│   ├── src/
│   │   ├── views/            # Pages (Dashboard, Products, Sales, Customers, Inventory, Reports)
│   │   ├── components/       # Reusable components
│   │   ├── stores/           # Pinia stores (auth, products, sales, inventory, notifications)
│   │   ├── services/api.js   # Axios API client
│   │   └── router/index.js   # Vue Router
│   └── .env                  # Frontend env (VITE_API_BASE_URL)
├── nginx.conf                # Nginx config for VPS
└── naseri-erp.service        # Systemd service for Gunicorn
```

---

## Modules & Features

### Working Features
- **Authentication** — Phone number login, token-based auth, role-based access (admin/manager)
- **Products** — CRUD, categories, units, min/max stock, soft delete, product history
- **Inventory** — Warehouses, stock transactions (purchase/sale/adjustment/return), low stock alerts
- **Sales** — Customers, sales orders (draft→confirmed→completed), invoices, payments, auto stock deduction
- **Purchases** — Suppliers, purchase orders, receiving, supplier invoices, supplier payments
- **Accounting** — Chart of accounts, journal entries, fiscal years, expense tracking
- **Audit Log** — Activity tracking with priority levels and notification system
- **Dashboard** — Sales metrics, inventory overview, recent activity
- **Reports** — Sales reports (daily/weekly/monthly), sales by product

### Key Business Logic
- Stock is deducted **only** when a sale moves from `draft` → `confirmed` or `completed`
- Cancelling a confirmed sale **restores** stock via a `return_from_customer` inventory transaction
- Stock levels are calculated from inventory transactions (not a stored field)
- Soft delete on users and products (data is never permanently lost)
- Auto-generated customer codes (`CUST000001`) and invoice numbers (`INV-20250101-0001`)

---

## Local Development Setup

### Prerequisites
- Python 3.12
- PostgreSQL
- Node.js 18+

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows CMD

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and fill in your local PostgreSQL credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

### Frontend

```bash
cd frontend

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env

# Install and run
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`, backend on `http://localhost:8000`.

---

## Environment Variables

Create `backend/.env` based on `backend/.env.example`:

```env
SECRET_KEY=your-50-char-random-secret-key
DEBUG=True                          # False in production
ALLOWED_HOSTS=localhost,127.0.0.1   # your-domain.com in production
DB_NAME=naseri_erp_db
DB_USER=naseri_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:5173   # https://your-domain.com in production
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## VPS Deployment

### Server Requirements
- Ubuntu 22.04 LTS
- 1GB RAM minimum
- PostgreSQL, Python 3.12, Node.js 18, Nginx

### 1. Install System Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3-pip postgresql postgresql-contrib nginx git
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Setup PostgreSQL

```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE naseri_erp_db;
CREATE USER naseri_user WITH PASSWORD 'your-strong-password';
GRANT ALL PRIVILEGES ON DATABASE naseri_erp_db TO naseri_user;
\q
```

### 3. Clone & Setup Backend

```bash
git clone https://github.com/your-username/naseri.git /home/user/naseri
cd /home/user/naseri/backend

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt

# Create .env with production values
cp .env.example .env
nano .env
# Set: DEBUG=False, ALLOWED_HOSTS=your-domain.com, DB credentials, CORS_ALLOWED_ORIGINS
```

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 4. Build Frontend

```bash
cd /home/user/naseri/frontend
npm install
# Set production API URL
echo "VITE_API_BASE_URL=https://your-domain.com/api" > .env.production
npm run build
# Output is in frontend/dist/
```

### 5. Configure Nginx

Edit `nginx.conf` (already in repo root) — replace `your-domain.com` and `/home/user/` with your actual values:

```bash
sudo cp /home/user/naseri/nginx.conf /etc/nginx/sites-available/naseri
sudo ln -s /etc/nginx/sites-available/naseri /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

The `nginx.conf` serves:
- `/` → Vue.js frontend (`frontend/dist/`)
- `/api/` → Gunicorn (Django)
- `/admin/`, `/swagger/`, `/redoc/` → Gunicorn (Django)
- `/media/` → Django media files

### 6. Setup Gunicorn as a Service

Edit `naseri-erp.service` (already in repo root) — replace `user` with your actual Linux username:

```bash
sudo cp /home/user/naseri/naseri-erp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable naseri-erp
sudo systemctl start naseri-erp

# Check status
sudo systemctl status naseri-erp
```

### 7. SSL with Let's Encrypt (recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## API Documentation

After starting the backend server:

| URL | Description |
|-----|-------------|
| `/swagger/` | Swagger UI (interactive) |
| `/redoc/` | ReDoc documentation |
| `/swagger.json/` | OpenAPI JSON schema |
| `/admin/` | Django admin panel |

---

## API Endpoints Summary

```
POST   /api/users/login/              # Login → returns token
POST   /api/users/logout/             # Logout

GET    /api/products/products/        # List products
GET    /api/inventory/stock-levels/   # All product stock levels
GET    /api/inventory/low-stock/      # Products below min stock

GET    /api/sales/customers/          # List customers
GET    /api/sales/sales/              # List sales
PATCH  /api/sales/sales/{id}/update-status/  # Change sale status

GET    /api/purchases/purchases/      # List purchases
GET    /api/accounting/accounts/      # Chart of accounts

GET    /api/sales/sales-report/       # Sales report (daily/weekly/monthly)
GET    /api/sales/sales-by-product/   # Sales grouped by product
```

All endpoints require `Authorization: Token <your-token>` header except login.

---

## Running Tests

```bash
cd backend
python manage.py test users.tests_e2e -v 2
```

The E2E test covers the full business cycle: supplier → purchase → receive stock → sell → payment → inventory check → soft delete.

---

## Default Users (after running createsuperuser or create_test_users command)

```bash
# Create test users with predefined credentials
python manage.py create_test_users
```

| Role | Phone | Password |
|------|-------|----------|
| Admin | 09122173180 | Admin@123 |
| Manager | 09123456788 | Manager@123 |

---

## Troubleshooting

**Backend won't start — `No module named 'whitenoise'`**
```bash
pip install -r requirements.txt
```

**Frontend can't reach backend (CORS error)**
- Check `CORS_ALLOWED_ORIGINS` in `backend/.env` matches your frontend URL exactly

**Stock not updating after sale confirmation**
- Make sure you use the `PATCH /api/sales/sales/{id}/update-status/` endpoint to change status, not a direct PATCH to the sale object

**Nginx 502 Bad Gateway**
- Check Gunicorn is running: `sudo systemctl status naseri-erp`
- Check logs: `sudo journalctl -u naseri-erp -n 50`

**Static files not loading in production**
```bash
python manage.py collectstatic --noinput
```
