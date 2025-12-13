# TenProducts - Database Schema

## Database Overview

**Database Type**: SQLite (Development) / PostgreSQL (Production)  
**ORM**: SQLAlchemy  
**Tables**: 10 core tables  
**Relationships**: Foreign keys with proper constraints

---

## Entity Relationship Diagram

```
┌─────────────────┐        ┌──────────────────┐
│     USERS       │        │    CATEGORIES    │
├─────────────────┤        ├──────────────────┤
│ id (PK)         │        │ id (PK)          │
│ name            │        │ name (UNIQUE)    │
│ email (UNIQUE)  │        └──────────────────┘
│ phone           │                 ▲
│ hashed_password │                 │
│ address         │                 │ 1:N
│ role            │                 │
│ created_at      │        ┌──────────────────┐
└─────────────────┘        │    PRODUCTS      │
    ▲                      ├──────────────────┤
    │                      │ id (PK)          │
    │ 1:N                  │ name             │
    │                      │ price            │
    ├──────────────────────│ discount_price   │
    │                      │ stock            │
    │                      │ expiration_date  │
    │                      │ category_id (FK) │
    │                      │ farmer_id (FK)   │
    │                      │ supplier_id (FK) │
    │                      │ image_url        │
    │                      └──────────────────┘
    │                              ▲
    │                              │ 1:N
    │                    ┌─────────┴──────┐
    │                    │                │
    │        ┌───────────────────┐   ┌──────────────────┐
    │        │   CART_ITEMS      │   │  SUPPLIERS       │
    │        ├───────────────────┤   ├──────────────────┤
    │        │ id (PK)           │   │ id (PK)          │
    │        │ user_id (FK) ┐    │   │ name             │
    │        │ product_id   │    │   └──────────────────┘
    │        │ quantity     │    │
    │        └───────────────────┘
    │                 ▲
    │                 │
    └─────────────────┘


┌─────────────────┐         ┌──────────────────┐
│     ORDERS      │         │  ORDER_ITEMS     │
├─────────────────┤         ├──────────────────┤
│ id (PK)         │────N:1──│ id (PK)          │
│ user_id (FK)    │         │ order_id (FK)    │
│ courier_id (FK) │         │ product_id (FK)  │
│ total_price     │         │ quantity         │
│ payment_method  │         │ price            │
│ address         │         └──────────────────┘
│ status          │
│ created_at      │
│ delivered_at    │
└─────────────────┘


┌──────────────────────┐   ┌────────────────────────┐
│ COURIER_LOCATIONS    │   │   FEEDBACKS            │
├──────────────────────┤   ├────────────────────────┤
│ courier_id (PK, FK)  │   │ id (PK)                │
│ lat                  │   │ user_id (FK)           │
│ lng                  │   │ order_id (FK, UNIQUE)  │
│ updated_at           │   │ rating (1-5)           │
└──────────────────────┘   │ comment                │
                           └────────────────────────┘
```

---

## Table Definitions

### USERS Table

**Purpose**: Store user accounts with authentication and role information

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    hashed_password VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    role VARCHAR(50) DEFAULT 'user' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

**Fields**:
- `id`: Unique identifier (Primary Key)
- `name`: User's full name
- `email`: Email address (unique, used for login)
- `phone`: Optional phone number
- `hashed_password`: Password encrypted with bcrypt
- `address`: Delivery address (NULL for farmers/couriers)
- `role`: USER | FARMER | COURIER | ADMIN
- `created_at`: Account creation timestamp
- `updated_at`: Last modification timestamp

**Sample Data**:
```
id=1, email=anna@example.com, name=Anna K., role=user, address=Nevsky Ave, 12
id=2, email=farm@example.com, name=Local Farm Inc., role=farmer
id=3, email=ivan@example.com, name=Ivan P., role=courier
id=4, email=admin@example.com, name=Admin, role=admin
```

---

### CATEGORIES Table

**Purpose**: Product categories for organization and filtering

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE INDEX idx_categories_name ON categories(name);
```

**Fields**:
- `id`: Unique identifier
- `name`: Category name (e.g., "Vegetables", "Fruits")

**Sample Data**:
```
id=1, name=Vegetables
id=2, name=Fruits
id=3, name=Dairy Products
id=4, name=Bakery
```

---

### SUPPLIERS Table

**Purpose**: Store supplier/farmer partnership information

```sql
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);
```

**Fields**:
- `id`: Unique identifier
- `name`: Supplier/farm name

---

### PRODUCTS Table

**Purpose**: Product catalog with pricing, stock, and relationship info

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    discount_price FLOAT,
    stock INTEGER DEFAULT 0,
    expiration_date TIMESTAMP,
    category_id INTEGER NOT NULL,
    supplier_id INTEGER,
    farmer_id INTEGER,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (farmer_id) REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_farmer ON products(farmer_id);
CREATE INDEX idx_products_stock ON products(stock);
```

**Fields**:
- `id`: Unique product identifier
- `name`: Product name (e.g., "Organic Tomatoes")
- `price`: Regular price
- `discount_price`: Sale price (optional)
- `stock`: Available quantity
- `expiration_date`: Best-by date
- `category_id`: Link to categories
- `supplier_id`: Link to suppliers (deprecated)
- `farmer_id`: Link to farmer/seller
- `image_url`: Product image URL
- `created_at`: Creation timestamp

**Sample Data**:
```
id=1, name=Organic Tomatoes, price=25.99, discount_price=22.99, stock=50, farmer_id=2
id=2, name=Fresh Cucumbers, price=15.99, stock=100, farmer_id=2
id=3, name=Local Apples, price=35.99, stock=200, farmer_id=2
```

---

### CART_ITEMS Table

**Purpose**: User shopping cart items (temporary)

```sql
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE(user_id, product_id)
);

-- Indexes
CREATE INDEX idx_cart_items_user ON cart_items(user_id);
CREATE INDEX idx_cart_items_product ON cart_items(product_id);
```

**Fields**:
- `id`: Unique cart item identifier
- `user_id`: Link to user
- `product_id`: Link to product
- `quantity`: Items in cart
- **Constraint**: One product per user in cart (UNIQUE)

**Purpose**: Temporary storage before order creation

---

### ORDERS Table

**Purpose**: Order records with status tracking and delivery info

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    courier_id INTEGER,
    total_price FLOAT NOT NULL,
    payment_method VARCHAR(50),
    address VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'created',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (courier_id) REFERENCES users(id)
);

-- Indexes
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_courier ON orders(courier_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at);
```

**Fields**:
- `id`: Unique order identifier
- `user_id`: Customer reference
- `courier_id`: Assigned courier (NULL until assigned)
- `total_price`: Order total
- `payment_method`: Payment type (e.g., "credit_card")
- `address`: Delivery address
- `status`: Order status (see enum below)
- `created_at`: Order creation time
- `delivered_at`: Delivery completion time

**Status Values**:
```
CREATED     → Order created, awaiting acceptance
ACCEPTED    → Courier accepted the order
PREPARING   → Items being prepared for delivery
ON_THE_WAY  → Delivery in progress
DELIVERED   → Order delivered
CANCELLED   → Order cancelled
```

**Sample Data**:
```
id=1, user_id=1, courier_id=3, total_price=51.98, status=on_the_way, address=123 Main St
```

---

### ORDER_ITEMS Table

**Purpose**: Individual items in an order (detail records)

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Indexes
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

**Fields**:
- `id`: Unique line item identifier
- `order_id`: Link to parent order
- `product_id`: Link to product
- `quantity`: Items in this line
- `price`: Price at time of order (historical)

**Purpose**: Preserves product price history (prices can change)

---

### COURIER_LOCATIONS Table

**Purpose**: Real-time tracking of courier positions

```sql
CREATE TABLE courier_locations (
    courier_id INTEGER PRIMARY KEY,
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (courier_id) REFERENCES users(id)
);

-- Index
CREATE INDEX idx_courier_locations_updated ON courier_locations(updated_at);
```

**Fields**:
- `courier_id`: Primary key, link to courier user
- `lat`: Latitude coordinate
- `lng`: Longitude coordinate
- `updated_at`: Last update timestamp

**Purpose**: Enables real-time delivery tracking

---

### FEEDBACKS Table

**Purpose**: Customer reviews and ratings

```sql
CREATE TABLE feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_id INTEGER UNIQUE NOT NULL,
    rating INTEGER NOT NULL,
    comment VARCHAR(1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Indexes
CREATE INDEX idx_feedbacks_user ON feedbacks(user_id);
CREATE INDEX idx_feedbacks_order ON feedbacks(order_id);
CREATE INDEX idx_feedbacks_rating ON feedbacks(rating);
```

**Fields**:
- `id`: Unique feedback identifier
- `user_id`: Reviewer (must be user)
- `order_id`: Reviewed order (one per order)
- `rating`: 1-5 star rating
- `comment`: Optional review text
- `created_at`: Review creation time

**Constraints**:
- One feedback per order (UNIQUE)
- Rating between 1-5

---

## Data Relationships

### One-to-Many (1:N)

**User → Orders**
```
1 User can have N Orders
- A customer places multiple orders
- Foreign Key: orders.user_id → users.id
```

**User → CartItems**
```
1 User has N CartItems
- User's shopping cart
- Foreign Key: cart_items.user_id → users.id
```

**Category → Products**
```
1 Category has N Products
- Multiple products per category
- Foreign Key: products.category_id → categories.id
```

**Farmer → Products**
```
1 Farmer sells N Products
- Farmer lists multiple products
- Foreign Key: products.farmer_id → users.id
```

**Product → CartItems**
```
1 Product can be in N Carts
- Product appears in multiple users' carts
- Foreign Key: cart_items.product_id → products.id
```

**Product → OrderItems**
```
1 Product ordered N Times
- Popular products ordered multiple times
- Foreign Key: order_items.product_id → products.id
```

**Order → OrderItems**
```
1 Order has N OrderItems
- Order contains multiple products
- Foreign Key: order_items.order_id → orders.id
```

**Order → Feedback**
```
1 Order gets 0-1 Feedback
- One review per order
- Foreign Key: feedbacks.order_id → orders.id
- Relationship: uselist=False
```

### Many-to-One (N:1)

**Orders → User (Courier)**
```
N Orders assigned to 1 Courier
- A courier handles multiple deliveries
- Foreign Key: orders.courier_id → users.id
```

**User → Courier Location**
```
1 Courier has 1 Location
- Real-time location per courier
- Relationship: uselist=False
```

---

## Indexes & Performance

### Primary Indexes (Automatic)
- All PRIMARY KEY columns auto-indexed
- Ensures unique constraint, fast lookups

### Secondary Indexes (Manually Created)

**For Query Performance**:
```
users.email           → Login queries
users.role            → Role-based filtering
products.name         → Search functionality
products.category_id  → Category filtering
products.farmer_id    → Farmer's product listing
products.stock        → Availability queries
orders.user_id        → User's orders
orders.courier_id     → Courier's orders
orders.status         → Status filtering
orders.created_at     → Date-based queries
```

### Query Optimization

**N+1 Prevention**:
```python
# Use relationships with joinedload or selectinload
# Avoid lazy loading in loops

# Good:
orders = session.query(Order).options(
    joinedload(Order.user),
    joinedload(Order.courier),
    joinedload(Order.items)
).all()

# Bad:
for order in orders:
    print(order.user.name)  # N+1 queries!
```

---

## Migration Strategy

### Current Setup
- No migration tool (Alembic) currently in use
- Manual schema creation on startup
- Development-friendly, not production-ready

### For Production
```python
# Use Alembic for migrations
# alembic init alembic
# alembic revision --autogenerate -m "description"
# alembic upgrade head
```

### Backup Strategy
```bash
# SQLite backup
cp fresh_groceries.db fresh_groceries.backup.db

# PostgreSQL backup (production)
pg_dump -U user dbname > backup.sql
```

---

## Database Constraints

### NOT NULL Constraints
- User: name, email, hashed_password, role
- Product: name, price, stock, category_id
- Order: user_id, total_price, address, status
- OrderItem: order_id, product_id, quantity, price

### UNIQUE Constraints
- User: email
- Category: name
- CartItem: (user_id, product_id) composite
- Feedback: order_id

### FOREIGN KEY Constraints
- ON DELETE CASCADE for cart_items, order_items
- ON DELETE RESTRICT for category, supplier references
- Support referential integrity

### CHECK Constraints (Recommended)
```sql
-- Add for validation at DB level:
ALTER TABLE products ADD CONSTRAINT check_price 
    CHECK (price > 0);
    
ALTER TABLE feedbacks ADD CONSTRAINT check_rating 
    CHECK (rating BETWEEN 1 AND 5);
```

---

## Sample Queries

### Find user's current orders
```sql
SELECT o.* FROM orders o
WHERE o.user_id = 1 
AND o.status != 'cancelled'
ORDER BY o.created_at DESC;
```

### Get products by category with stock
```sql
SELECT p.* FROM products p
JOIN categories c ON p.category_id = c.id
WHERE c.name = 'Vegetables'
AND p.stock > 0
ORDER BY p.price ASC;
```

### Get courier's active orders
```sql
SELECT o.*, 
       COUNT(oi.id) as item_count
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE o.courier_id = 3
AND o.status IN ('accepted', 'preparing', 'on_the_way')
GROUP BY o.id;
```

### Get admin statistics
```sql
SELECT 
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT o.id) as total_orders,
    SUM(o.total_price) as total_revenue,
    AVG(o.total_price) as avg_order_value
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

---

**Document Date**: December 2025  
**Version**: 1.0  
**Last Updated**: December 28, 2024
