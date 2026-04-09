# Tracker — Low Stock Alert: Shared Pantry Tracker

A shared web-based low-stock tracker that automatically highlights products needing replenishment when their quantity falls below a set threshold.

## Demo

<!-- Add screenshots here -->
![Product list with low-stock highlight](demo/screenshot1.png)
![Add product form](demo/screenshot2.png)

## Product Context

### End Users

- Students living in dormitories or sharing a common kitchen (3–6 people per group)
- Small office teams that share a refrigerator or pantry

### Problem

In shared living or working spaces, people frequently forget to notify others when common supplies like milk, bread, coffee, or sugar are almost gone. This leads to frustrating situations where someone goes to the store only to discover the product is already finished, or finds out late at night that there is no coffee left while the store is already closed.

### Solution

Tracker automatically highlights low-stock items in red on everyone's screen as soon as they reach a critical level, eliminating the need for verbal reminders or manual checking. Everyone can see at a glance exactly what needs to be bought, preventing unexpected shortages and saving time and frustration.

## Features

### Implemented

- View all products with current quantity and threshold level
- `+1` / `-1` buttons to adjust quantity
- Automatic red highlight when quantity ≤ threshold
- Add new product form (name, starting quantity, threshold)
- Delete product button
- No page reloads (fetch API / HTTP requests)

### Planned (Version 2)

- "Bought" button — resets quantity to max value in one click
- Separate shopping list section showing only critical items
- Real-time updates across all users
- Input validation (quantity cannot go negative)

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

### Prerequisites

- Python 3.12+
- PostgreSQL
- pip and virtualenv (or your preferred Python package manager)
- Docker & Docker Compose (optional, for containerized deployment)

### Step-by-Step Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Tracker
   ```

2. **Set up the Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the database:**
   - Install and start PostgreSQL
   - Create a database and user for the application
   - Update the database connection string in `backend/database.py`

4. **Run the backend:**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Serve the frontend:**
   - Place the `frontend/` directory behind a web server (e.g., Nginx) or serve it directly
   - Ensure the frontend is configured to point to the backend API URL

6. **(Optional) Deploy with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

7. Access the application at `http://<your-vm-ip>:8000` (or the port configured for your web server).
