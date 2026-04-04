# Development Plan — Low Stock Alert Tracker

---

## Version 1: Core Product ✅ COMPLETE

**Status:** Implemented and ready for testing  
**Goal:** Deliver a working low-stock tracker with essential features

### Features Implemented

#### 1. View All Products
- Display complete list of tracked products
- Show current quantity for each product
- Show threshold level for each product
- Pull-to-refresh to reload data

#### 2. Quantity Adjustment
- `+1` button to increase quantity by one
- `-1` button to decrease quantity by one
- Input validation prevents negative quantities
- Instant visual feedback on update

#### 3. Automatic Low Stock Alert
- Products automatically highlighted in red when quantity ≤ threshold
- "LOW STOCK" badge appears on critical items
- Red border and background for visual emphasis
- Works without page reload

#### 4. Add New Product
- Simple dialog form with three fields:
  - Product name (required)
  - Initial quantity (required, non-negative)
  - Threshold value (required, minimum 1)
- Form validation prevents invalid input
- Success confirmation on add

#### 5. Delete Product
- Delete button on each product card
- Confirmation dialog before deletion
- Removes product from database and UI
- Success notification after deletion

#### 6. No Page Reload
- All actions use HTTP fetch API
- State management via Provider pattern
- Smooth, responsive user experience
- Real-time UI updates

### Technical Stack
- **Backend:** FastAPI (Python) with async support
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Frontend:** Flutter Web with Material Design 3
- **State Management:** Provider pattern
- **API Communication:** REST with JSON

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products |
| POST | `/api/products` | Create new product |
| PUT | `/api/products/{id}` | Update product quantity |
| DELETE | `/api/products/{id}` | Delete product |

### Files Structure
```
backend/
├── main.py              # FastAPI app + CRUD endpoints
├── models.py            # SQLAlchemy Product model
├── schemas.py           # Pydantic validation schemas
├── database.py          # Database connection + session
├── requirements.txt     # Python dependencies
└── .env.example         # Environment template

frontend/lib/
├── main.dart                        # App entry + theme
├── models/product.dart              # Product data class
├── providers/product_provider.dart  # State management
├── services/api_service.dart        # HTTP client
├── screens/product_list_screen.dart # Main screen
└── widgets/
    ├── product_card.dart            # Product card UI
    └── add_product_dialog.dart      # Add product form
```

---

## Version 2: Enhanced Features 🚧 PLANNED

**Goal:** Improve usability, add real-time sync, and deploy to cloud

### New Features to Implement

#### 1. "Bought" Button
- One-click button to reset product quantity to maximum value
- Represents: "I bought more of this product"
- Sets quantity back to a predefined max level (stored in database)
- Visual distinction from +1/-1 buttons (different color/icon)
- **Database change:** Add `max_quantity` field to products table

**Implementation:**
- Update database schema to store `max_quantity`
- Add new PUT endpoint or modify existing one
- Add prominent button in UI (green color, shopping cart icon)
- Update product card layout to accommodate new button

#### 2. Shopping List Section
- Separate section showing ONLY products at or below threshold
- Appears at top of product list when items are low
- Can be collapsed/expanded
- Shows count of items needing attention (e.g., "3 items need restocking")
- **No backend changes needed** (filtered from existing data)

**Implementation:**
- Filter products where `quantity <= threshold`
- Create new widget: `ShoppingListSection`
- Add to top of `ProductListScreen`
- Only show when low-stock items exist

#### 3. Real-Time Updates Across All Users
- When one user changes quantity, all other users see update instantly
- No manual refresh needed
- Uses WebSocket or Server-Sent Events (SSE)
- **Backend change:** Add WebSocket endpoint

**Implementation Options:**

**Option A: WebSocket (Recommended)**
- FastAPI supports WebSockets natively
- Broadcast changes to all connected clients
- Flutter listens via `web_socket_channel` package
- More efficient, true bidirectional communication

**Option B: Polling (Fallback)**
- Frontend polls API every 5-10 seconds
- Simpler to implement but less efficient
- No WebSocket support needed

**Recommended approach:** WebSocket with polling fallback

#### 4. Input Validation Enhancements
- Quantity cannot go below zero (already implemented)
- Prevent quantity exceeding max_quantity (when "Bought" feature added)
- Validate product name uniqueness (optional, configurable)
- Show inline error messages for failed updates
- Disable buttons during API calls to prevent double-submission

**Implementation:**
- Add loading state to buttons
- Add max quantity check
- Improve error messages in UI
- Add backend validation for duplicate names (optional)

#### 5. Room/Group Support (Optional)
- Multiple groups can use the same app independently
- Each group has its own product list
- Users select or create a "room" on first use
- Room code or link for sharing
- **Database change:** Add `room_id` to products table, create `rooms` table

**Implementation:**
- Create `Room` model (id, name, code)
- Add `room_id` foreign key to `Product` model
- Add room selection screen to Flutter app
- Filter all API queries by room
- Generate shareable room codes

#### 6. Cloud Deployment
- Deploy backend to **Render** (free tier)
- Use **Supabase** or **Neon** for PostgreSQL database
- Deploy frontend to **Netlify** or **Vercel**
- Configure CORS for cross-origin requests
- Set up environment variables for production
- Add HTTPS support
- Configure custom domain (optional)

**Deployment Steps:**

**Backend (Render):**
- Create `render.yaml` configuration
- Set `DATABASE_URL` environment variable
- Connect GitHub repository
- Auto-deploy on push

**Database (Supabase/Neon):**
- Create free account
- Create new project/database
- Get connection string
- Update backend `DATABASE_URL`

**Frontend (Netlify):**
- Build web app: `flutter build web`
- Connect GitHub repository
- Set build command: `cd frontend && flutter build web`
- Set publish directory: `frontend/build/web`

---

## Version 2 Priority Order

1. **"Bought" button** (high impact, easy to implement)
2. **Shopping list section** (high impact, easy to implement)
3. **Input validation enhancements** (medium impact, improves UX)
4. **Real-time updates** (high impact, moderate complexity)
5. **Cloud deployment** (required for production use)
6. **Room/group support** (nice-to-have, adds complexity)

---

## Database Schema Changes (Version 2)

### Current Schema (Version 1)
```sql
products
├── id (Integer, Primary Key)
├── name (String 100)
├── quantity (Integer)
└── threshold (Integer)
```

### Updated Schema (Version 2)
```sql
products
├── id (Integer, Primary Key)
├── name (String 100)
├── quantity (Integer)
├── threshold (Integer)
├── max_quantity (Integer)          -- NEW: for "Bought" button
└── room_id (Integer, Foreign Key)  -- NEW: for room support (optional)

rooms (optional)
├── id (Integer, Primary Key)
├── name (String 100)
└── code (String 20, Unique)
```

---

## Estimated Complexity

| Feature | Complexity | Estimated Effort |
|---------|-----------|------------------|
| "Bought" button | Low | 1-2 hours |
| Shopping list section | Low | 1-2 hours |
| Input validation | Low-Medium | 1-2 hours |
| Real-time updates | Medium-High | 4-6 hours |
| Room support | Medium | 3-4 hours |
| Cloud deployment | Medium | 2-3 hours |

---

## Testing Strategy

### Version 1 (Current)
- Manual testing of all CRUD operations
- Test red highlight triggers correctly
- Test form validation
- Test delete confirmation

### Version 2 (Planned)
- Unit tests for Provider state management
- Integration tests for API endpoints
- WebSocket connection tests
- Cross-browser testing (Chrome, Firefox, Safari)
- Mobile responsive testing (if using mobile Flutter)

---

## Future Versions (Beyond V2)

### Version 3 Ideas
- User authentication (login/signup)
- Push notifications for low stock
- Product categories (dairy, snacks, beverages)
- History log (who changed what and when)
- Export shopping list as text/PDF
- Barcode scanning for adding products
- Image upload for products
- Multi-language support

### Version 4+ Ideas
- Mobile apps (iOS/Android native)
- Integration with grocery delivery APIs
- Smart suggestions based on usage patterns
- Automatic reorder reminders
- Analytics dashboard (consumption rates)

---

## Notes

- Version 1 is **feature-complete** and ready for TA feedback
- Version 2 features are prioritized by impact and complexity
- Room support is optional and can be skipped if not needed
- Cloud deployment should happen after core features are stable
- All Version 2 features can be implemented incrementally
