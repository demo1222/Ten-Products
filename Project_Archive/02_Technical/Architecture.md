# TenProducts - System Architecture

## Architecture Overview

TenProducts uses a modern, modular three-tier architecture with clear separation between presentation, business logic, and data layers.

```
┌─────────────────────────────────────────────────────┐
│            Presentation Layer                        │
│        (React/Next.js Frontend @ :3000)              │
│  ┌──────────────────────────────────────────────┐   │
│  │  Pages | Components | Styles | Utils         │   │
│  └──────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/JSON (REST API)
┌─────────────────┴────────────────────────────────────┐
│         API Layer / Application Server               │
│      (FastAPI Backend @ http://127.0.0.1:8000)       │
│  ┌──────────────────────────────────────────────┐   │
│  │  Routers (API Endpoints)                     │   │
│  │  - /auth, /products, /cart, /orders, etc.    │   │
│  └──────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │  Services (Business Logic)                   │   │
│  │  - auth_service, product_service, etc.       │   │
│  └──────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │  Schemas (Data Validation - Pydantic)        │   │
│  │  - Request/Response models                   │   │
│  └──────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │  Utils (Authentication, Security)            │   │
│  │  - deps.py, security.py                      │   │
│  └──────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────┘
                 │ SQL Queries (SQLAlchemy ORM)
┌─────────────────┴────────────────────────────────────┐
│         Data Access Layer / Database                 │
│           (SQLite - Development)                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  SQLAlchemy ORM Mapping                      │   │
│  │  ├── Users                                   │   │
│  │  ├── Products                                │   │
│  │  ├── Orders                                  │   │
│  │  ├── Cart Items                              │   │
│  │  ├── Courier Locations                       │   │
│  │  └── Feedback                                │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Frontend Architecture (Next.js)

```
ten-prod-front/
│
├── src/
│   ├── app/                          # Pages (Next.js App Router)
│   │   ├── page.jsx                  # Home page
│   │   ├── layout.jsx                # Root layout
│   │   ├── globals.css               # Global styles
│   │   ├── auth/page.jsx             # Authentication page
│   │   ├── store/page.jsx            # Products store
│   │   ├── checkout/page.jsx         # Checkout flow
│   │   ├── orders/page.jsx           # Order history
│   │   ├── admin/page.jsx            # Admin dashboard
│   │   ├── farmer/page.jsx           # Farmer dashboard
│   │   └── courier/page.jsx          # Courier dashboard
│   │
│   ├── components/                   # Reusable UI components
│   │   ├── Header/
│   │   ├── Footer/
│   │   ├── ProductCard/              # Product display
│   │   ├── ProductModal/             # Product details modal
│   │   ├── CartSidebar/              # Shopping cart sidebar
│   │   ├── FiltersSidebar/           # Product filters
│   │   ├── FloatingCartBar/          # Sticky cart bar
│   │   └── Admin/                    # Admin components
│   │
│   ├── utils/                        # Utility functions
│   │   ├── api.js                    # API client
│   │   ├── storage.js                # LocalStorage helpers
│   │   ├── formatCurrency.js         # Format utilities
│   │   └── scrollToAnchor.js         # Navigation helpers
│   │
│   ├── data/                         # Mock/static data
│   │   └── smartGoals.js             # SMART goals data
│   │
│   └── styles/                       # Global styles
│       └── globals.scss              # SCSS variables & mixins
│
├── package.json
├── next.config.mjs
└── eslint.config.mjs
```

### Backend Architecture (FastAPI)

```
ten-prod-back/
│
├── app/
│   ├── __init__.py
│   │
│   ├── config.py                     # Configuration (DB URL, SECRET_KEY)
│   ├── database.py                   # Database connection setup
│   ├── main.py                       # FastAPI app initialization
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py                 # SQLAlchemy ORM models
│   │       ├── User
│   │       ├── Product
│   │       ├── Order
│   │       ├── CartItem
│   │       ├── Feedback
│   │       └── CourierLocation
│   │
│   ├── routers/                      # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py                   # Auth endpoints
│   │   ├── products.py               # Product endpoints
│   │   ├── categories.py             # Category endpoints
│   │   ├── cart.py                   # Cart endpoints
│   │   ├── orders.py                 # Order endpoints
│   │   ├── courier.py                # Courier endpoints
│   │   ├── farmer.py                 # Farmer endpoints
│   │   └── admin.py                  # Admin endpoints
│   │
│   ├── services/                     # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py           # Authentication logic
│   │   ├── product_service.py        # Product operations
│   │   ├── cart_service.py           # Cart operations
│   │   ├── order_service.py          # Order operations
│   │   ├── courier_service.py        # Courier operations
│   │   └── admin_service.py          # Admin operations
│   │
│   ├── schemas/                      # Pydantic validation models
│   │   ├── __init__.py
│   │   └── schemas.py
│   │       ├── UserSchema
│   │       ├── ProductSchema
│   │       ├── OrderSchema
│   │       └── ...
│   │
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       ├── deps.py                   # Dependency injection
│       └── security.py               # JWT, password hashing
│
├── requirements.txt
├── seed.py                           # Database seeding
├── README.md
└── fresh_groceries.db               # SQLite database (generated)
```

---

## Data Flow Diagram

### User Registration Flow
```
User fills form (Frontend)
       ↓
POST /auth/register
       ↓
AuthService.register_user()
       ↓
Validate email & password (Pydantic)
       ↓
Hash password (bcrypt)
       ↓
Create User record (Database)
       ↓
Return success response
       ↓
Store JWT token (localStorage)
```

### Product Purchase Flow
```
User browses products (Frontend)
       ↓
GET /products (API)
       ↓
ProductService.get_all_products()
       ↓
Database query
       ↓
Return JSON response
       ↓
Display in ProductCard component
       ↓
User adds to cart
       ↓
POST /cart/add (with auth token)
       ↓
CartService.add_item()
       ↓
Save CartItem to database
       ↓
Update UI state
       ↓
User checkout
       ↓
POST /orders (create order)
       ↓
OrderService.create_order()
       ↓
Transfer CartItems → OrderItems
       ↓
Create Order record
       ↓
Clear cart
       ↓
Return order confirmation
```

### Courier Order Acceptance Flow
```
Order created (CREATED status)
       ↓
GET /courier/available-orders
       ↓
CourierService.get_available_orders()
       ↓
Display available orders
       ↓
Courier selects order
       ↓
POST /courier/accept-order
       ↓
Update Order.status = ACCEPTED
       ↓
Assign courier_id
       ↓
Return success
       ↓
Courier updates location
       ↓
PUT /courier/location
       ↓
Update CourierLocation record
       ↓
User sees real-time location
```

---

## Technology Decisions

### Why FastAPI?
- **Async-first**: Built for async/await patterns
- **Performance**: One of the fastest Python frameworks
- **Automatic Validation**: Pydantic integration out-of-box
- **Auto Documentation**: Built-in Swagger/OpenAPI
- **Developer Experience**: Intuitive and well-documented

### Why Next.js?
- **Server-Side Rendering**: SEO and performance benefits
- **App Router**: Modern file-based routing
- **Built-in Optimization**: Image, font, script optimization
- **Full-Stack**: Can add API routes if needed
- **Developer Experience**: Fast refresh, excellent tooling

### Why SQLite?
- **Development**: Zero-configuration, file-based
- **Simplicity**: No separate database server needed
- **SQLAlchemy Support**: Full ORM support
- **Migration**: Easy upgrade path to PostgreSQL

### Why SQLAlchemy ORM?
- **Abstraction**: Database-agnostic queries
- **Relationships**: Easy model associations
- **Migrations**: Version control for schema (via Alembic)
- **Testing**: Easy to mock and test

### Why JWT Authentication?
- **Stateless**: No session storage required
- **Scalable**: Works well with distributed systems
- **Secure**: Token-based with expiration
- **Frontend-Friendly**: Stored in localStorage

---

## Security Architecture

```
┌──────────────────────────────────────┐
│      Frontend (Next.js)              │
│  • Validate input locally            │
│  • Store JWT in localStorage         │
│  • HTTPS only in production          │
└────────────┬─────────────────────────┘
             │ HTTPS + JWT Header
┌────────────┴─────────────────────────┐
│  API Gateway / Middleware            │
│  • CORS validation                   │
│  • Rate limiting (future)            │
│  • Request logging                   │
└────────────┬─────────────────────────┘
             │
┌────────────┴─────────────────────────┐
│      Router Layer (FastAPI)          │
│  • Endpoint definitions              │
│  • Authentication check              │
│  • Authorization (role-based)        │
└────────────┬─────────────────────────┘
             │
┌────────────┴─────────────────────────┐
│      Service Layer                   │
│  • Business logic validation         │
│  • Data transformation               │
│  • Permission checks                 │
└────────────┬─────────────────────────┘
             │ Parameterized Queries
┌────────────┴─────────────────────────┐
│      Database Layer                  │
│  • SQL injection prevention          │
│  • Encrypted passwords               │
│  • Audit logging                     │
└──────────────────────────────────────┘
```

---

## API Communication Pattern

### Request Structure
```json
{
  "headers": {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "Content-Type": "application/json"
  },
  "body": {
    "email": "user@example.com",
    "password": "hashedpassword"
  }
}
```

### Response Structure (Success)
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "role": "user",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### Response Structure (Error)
```json
{
  "status": "error",
  "message": "Invalid credentials",
  "code": "AUTH_INVALID"
}
```

---

## Deployment Architecture (Future)

```
┌─────────────────────────────────────┐
│     AWS / Azure / Heroku            │
├─────────────────────────────────────┤
│  ┌──────────────────────────────┐   │
│  │  CDN (CloudFront/CloudFlare) │   │
│  │  • Static assets             │   │
│  │  • DDoS protection           │   │
│  └──────────────────────────────┘   │
│           ↓                          │
│  ┌──────────────────────────────┐   │
│  │  Load Balancer               │   │
│  │  • Route traffic             │   │
│  │  • SSL termination           │   │
│  └──────────────────────────────┘   │
│           ↓                          │
│  ┌──────────────────────────────┐   │
│  │  API Servers (Docker)        │   │
│  │  • FastAPI instances         │   │
│  │  • Auto-scaling              │   │
│  └──────────────────────────────┘   │
│           ↓                          │
│  ┌──────────────────────────────┐   │
│  │  Database (RDS/Cloud SQL)    │   │
│  │  • PostgreSQL                │   │
│  │  • Automated backups         │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## Scalability Considerations

### Horizontal Scaling
- **Stateless API**: No session state in server
- **Database Connection Pooling**: Handle multiple connections
- **Load Balancer**: Distribute requests
- **Docker Containers**: Easy deployment and scaling

### Caching Strategy (Future)
- **Redis**: User sessions, product cache
- **CDN**: Static assets, images
- **Browser Cache**: Frontend assets

### Database Optimization
- **Indexing**: On frequently queried fields
- **Query Optimization**: Avoid N+1 queries
- **Connection Pooling**: Reuse database connections

---

## Monitoring & Logging (Future)

```
Application
    ↓
├── Error Tracking (Sentry)
├── Performance Monitoring (New Relic)
├── Log Aggregation (ELK Stack)
└── Uptime Monitoring (Pingdom)
    ↓
Dashboard & Alerts
```

---

## File Structure Relationships

```
Router (endpoint) → Service (logic) → Model (database)
    ↓                  ↓                    ↓
   Schema          Schema             ORM Model
(validation)    (transformation)    (database mapping)
    ↓                  ↓
Frontend           localStorage
  (JSX)          (client state)
```

---

**Document Date**: December 2025  
**Version**: 1.0  
**Status**: Complete
