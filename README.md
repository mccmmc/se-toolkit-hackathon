# Tracker — Low Stock Alert: Shared Pantry Tracker

Author: Maksim Potushinskii
m.potushinskii@innopolis.university
CSE-03

A shared web-based low-stock tracker that automatically highlights products needing replenishment when their quantity falls below a set threshold.

## Site
http://10.93.25.144:8000/


## Demo

<!-- Add screenshots here -->
<img width="1897" height="892" alt="image" src="https://github.com/user-attachments/assets/eac4fdf7-5531-43bc-a49b-e8cbb01d2452" />
<img width="971" height="193" alt="image" src="https://github.com/user-attachments/assets/b7e5e999-9ae5-425c-93ef-dcce2c196cc1" />
<img width="956" height="273" alt="image" src="https://github.com/user-attachments/assets/2fcaf333-364e-4e10-be36-fe62431d1bd6" />


## Product Context

### End Users

- Students living in dormitories or sharing a common kitchen (3–6 people per group)
- Small office teams that share a refrigerator or pantry

### Problem

In shared living or working spaces, people frequently forget to notify others when common supplies like milk, bread, coffee, or sugar are almost gone.

### Solution

Tracker automatically highlights low-stock items in red on everyone's screen as soon as they reach a critical level, eliminating the need for verbal reminders or manual checking. Everyone can see at a glance exactly what needs to be bought, preventing unexpected shortages and saving time and frustration.

## Features

### Implemented

- View all products with current quantity and threshold level
- `+1` / `-1` buttons to adjust quantity
- Automatic red highlight when quantity ≤ threshold
- Add new product form (name, starting quantity, threshold)
- Delete product button
- "Bought" button — resets quantity to max value in one click
- Separate shopping list section showing only critical items
- Real-time updates across all users
- Input validation (quantity cannot go negative)

### Implemented

- Audentification system for different rooms


## Usage

1. Open the web application in your browser.
2. View the list of tracked products, their current quantities, and threshold levels.
3. Use the `+1` and `-1` buttons to adjust quantities as items are consumed or restocked.
4. Products highlighted in red indicate low stock and need replenishment.
5. Add new products using the form at the top of the page.
6. Remove unnecessary products using the delete button next to each item.

## Deployment

### OS

Ubuntu 24.04 LTS

### Requirements

| Component | Version |
|-----------|---------|
| OS | Ubuntu 24.04 LTS (or any modern Linux) |
| Python | 3.12+ |
| PostgreSQL | 16+ |
| Docker | latest (optional, for containerized deployment) |

---

### Option 1: Docker Compose

The fastest way to get up and running — PostgreSQL and the backend start together.

```bash
docker-compose up -d
```

The app will be available at `http://localhost:8000`.

**Environment variables**:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@db:5432/tracker` |

---

### Option 2: Manual Setup

#### 1. Clone & install dependencies

```bash
git clone <repository-url>
cd Tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Set up PostgreSQL

```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql -c "CREATE DATABASE tracker;"
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

The default connection string is `postgresql://postgres:postgres@localhost:5432/tracker`.
To use different credentials, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/tracker
```

#### 3. Run the backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. Serve the frontend

Open `frontend/index.html` in a browser, or serve it with any static file server (Nginx, Caddy, Python's `http.server`, etc.). Make sure the frontend's API calls point to the correct backend URL.

#### 5. Access the app

Open `http://<your-ip>:8000` in your browser.
