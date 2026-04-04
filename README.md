# Low Stock Alert — Shared Pantry Tracker

## Quick Start

### Prerequisites

- **Python 3.10+** (for backend)
- **PostgreSQL 14+** (for database)
- **Flutter SDK 3.0+** (for frontend)

---

## Backend Setup

### 1. Install PostgreSQL

**Windows:**
- Download from: https://www.postgresql.org/download/windows/
- Install and remember your postgres password

**Create the database:**
```bash
psql -U postgres
CREATE DATABASE tracker;
\q
```

### 2. Set up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env
# Edit .env with your PostgreSQL credentials
```

Edit `.env` file:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/tracker
```

### 3. Run Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend will be available at: `http://localhost:8000`
API Documentation (Swagger): `http://localhost:8000/docs`

---

## Frontend Setup

### 1. Install Flutter

**Windows:**
```bash
# Download Flutter SDK from https://docs.flutter.dev/get-started/install
# Extract to C:\src\flutter
# Add C:\src\flutter\bin to your PATH
```

### 2. Set up Frontend

```bash
cd frontend

# Get dependencies
flutter pub get

# Enable web support (if not enabled)
flutter config --enable-web
```

### 3. Run Frontend

```bash
cd frontend
flutter run -d chrome
```

Or for web build:
```bash
flutter build web
```

---

## Usage

1. **Start the backend** (FastAPI server on port 8000)
2. **Start the frontend** (Flutter web app)
3. **Add products** using the "Add Product" button
4. **Track stock levels** with +1/-1 buttons
5. **Watch for red highlights** when quantity ≤ threshold

---

## Project Structure

```
Tracker/
├── backend/
│   ├── main.py              # FastAPI app with CRUD endpoints
│   ├── models.py            # SQLAlchemy Product model
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment template
└── frontend/
    └── lib/
        ├── main.dart                    # App entry point
        ├── models/
        │   └── product.dart             # Product model
        ├── providers/
        │   └── product_provider.dart    # State management
        ├── services/
        │   └── api_service.dart         # HTTP API calls
        ├── screens/
        │   └── product_list_screen.dart # Main screen
        └── widgets/
            ├── product_card.dart        # Product card UI
            └── add_product_dialog.dart  # Add product form
```

---

## Version 1 Features

✅ View all products with quantity and threshold  
✅ +1/-1 buttons to adjust quantity  
✅ Automatic red highlight when quantity ≤ threshold  
✅ Add new product form  
✅ Delete product button  
✅ No page reload (fetch API)  

---

## API Endpoints

- `GET /api/products` - Get all products
- `POST /api/products` - Create new product
- `PUT /api/products/{id}` - Update product quantity
- `DELETE /api/products/{id}` - Delete product

---

## Troubleshooting

**Backend won't start:**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env file
- Check all dependencies installed: `pip install -r requirements.txt`

**Frontend can't connect:**
- Ensure backend is running on port 8000
- Check CORS settings if deploying to different domain

**Flutter not found:**
- Add Flutter to PATH
- Run `flutter doctor` to check setup
