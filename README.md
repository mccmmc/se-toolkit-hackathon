# Tracker
# Low Stock Alert — Shared Pantry Tracker

## Project Description (1 sentence)

A shared web-based low-stock tracker that automatically highlights products needing replenishment when their quantity falls below a set threshold.

---

## What problem does it solve? (A key feature)

The key feature is the automatic visual alert that highlights a product in red the moment its quantity drops below or equal to the set threshold. The problem this solves is that in shared living or working spaces, people frequently forget to notify others when common supplies like milk, bread, coffee, or sugar are almost gone. This leads to frustrating situations where someone goes to the store only to discover the product is already finished, or finds out late at night that there is no coffee left while the store is already closed. By automatically turning the product red on everyone's screen as soon as it reaches a critical level, the product eliminates the need for verbal reminders or manual checking. Everyone can see at a glance exactly what needs to be bought, preventing unexpected shortages and saving time and frustration.

---

## End User

The primary end users are students living in a dormitory or sharing a common kitchen with three to six people per group, as well as small office teams that share a refrigerator or pantry. These users typically share the responsibility of buying groceries and household supplies, but they often forget to notify others when something is running low. They need a simple, visual way to see at a glance what needs to be bought without relying on verbal communication or messy shared notes. The product solves this by automatically highlighting low-stock items, making it clear to everyone exactly what is missing.

---

## Main Features

The product allows users to view a complete list of all tracked products along with their current quantity and defined threshold level. Each product has simple one-click buttons to increase or decrease its quantity by one. When the quantity of any product falls below or equal to its threshold, that product is immediately highlighted in red to draw attention and indicate that it needs to be replenished. Users can easily add new products to the list by filling out a simple form with the product name, starting quantity, and threshold value. Unnecessary products can be removed with a delete button. In Version 2, a dedicated "Bought" button resets the product quantity back to its maximum value in one click, and a separate shopping list section automatically displays all products that have reached or fallen below their threshold. All actions happen without page reloads, providing a smooth and responsive user experience.

---

## Implementation Details

**Backend:** FastAPI (Python) — used to build REST API endpoints with automatic documentation (Swagger) and async support for better performance.

**Database:** PostgreSQL — used to store products with reliable data persistence; supports concurrent users; can be hosted locally or on the cloud (e.g., Neon or Supabase).

**Client:** Flutter (web or mobile) — cross-platform UI (web app, iOS, Android); reactive interface with real-time updates.

---

## Version Plan

### Version 1 (Core working product)

- View all products with quantity and threshold
- `+1` / `-1` buttons to adjust quantity
- Automatic red highlight when quantity ≤ threshold
- Add new product form
- Delete product button
- No page reload (fetch API / HTTP requests)

### Version 2 (Improvements + TA feedback)

- "Bought" button — resets quantity to max value in one click
- Separate shopping list section showing only critical items
- Real-time updates across all users
- Input validation (quantity cannot go negative)
- Optional: room support for different groups
- Deployment to cloud (Render + Supabase + Netlify)
