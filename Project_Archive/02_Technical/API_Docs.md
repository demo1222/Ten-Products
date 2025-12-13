# TenProducts - API Documentation

## API Overview

**Base URL**: `http://127.0.0.1:8000`  
**API Version**: 1.0  
**Authentication**: JWT Bearer Token  
**Response Format**: JSON  
**Documentation**: Available at `/docs` (Swagger) and `/redoc` (ReDoc)

---

## Authentication

### JWT Token Flow

1. User logs in with email/password
2. Server returns JWT token
3. Client includes token in `Authorization` header: `Bearer {token}`
4. Token expires after 30 minutes
5. User must log in again to get new token

### Headers Required
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

---

## User Role Permissions

| Endpoint Category | USER | FARMER | COURIER | ADMIN |
|-------------------|------|--------|---------|-------|
| Auth | ✅ | ✅ | ✅ | ✅ |
| Products (Browse) | ✅ | ✅ | ✅ | ✅ |
| Products (Create) | ❌ | ✅ | ❌ | ✅ |
| Cart | ✅ | ❌ | ❌ | ❌ |
| Orders (Own) | ✅ | ❌ | ❌ | ✅ |
| Orders (Manage) | ❌ | ❌ | ❌ | ✅ |
| Courier | ❌ | ❌ | ✅ | ✅ |
| Farmer | ❌ | ✅ | ❌ | ✅ |
| Admin | ❌ | ❌ | ❌ | ✅ |

---

## Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user

**Request**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "password123",
  "role": "user"
}
```

**Response** (201 Created)
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "message": "User registered successfully"
}
```

**Error** (400 Bad Request)
```json
{
  "detail": "Email already registered"
}
```

---

#### POST /auth/login
User login

**Request**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

**Error** (401 Unauthorized)
```json
{
  "detail": "Invalid credentials"
}
```

---

### Product Endpoints

#### GET /products
Get all products (with pagination and filtering)

**Query Parameters**
- `skip`: Pagination offset (default: 0)
- `limit`: Items per page (default: 10)
- `category`: Filter by category ID
- `search`: Search by product name
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter

**Request**
```
GET /products?skip=0&limit=10&category=1&search=tomato
```

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "name": "Organic Tomatoes",
      "price": 25.99,
      "discount_price": 22.99,
      "stock": 50,
      "category_id": 1,
      "farmer_id": 2,
      "image_url": "https://...",
      "expiration_date": "2025-01-30"
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 10
}
```

---

#### GET /products/{product_id}
Get product details

**Request**
```
GET /products/1
```

**Response** (200 OK)
```json
{
  "id": 1,
  "name": "Organic Tomatoes",
  "price": 25.99,
  "discount_price": 22.99,
  "stock": 50,
  "category": {
    "id": 1,
    "name": "Vegetables"
  },
  "farmer": {
    "id": 2,
    "name": "Local Farm Inc.",
    "email": "farm@example.com"
  },
  "image_url": "https://...",
  "expiration_date": "2025-01-30"
}
```

---

#### POST /products
Create a new product (FARMER/ADMIN)

**Request**
```json
{
  "name": "Fresh Cucumbers",
  "price": 15.99,
  "discount_price": 14.99,
  "stock": 100,
  "category_id": 1,
  "image_url": "https://...",
  "expiration_date": "2025-02-05"
}
```

**Response** (201 Created)
```json
{
  "id": 2,
  "name": "Fresh Cucumbers",
  "price": 15.99,
  "discount_price": 14.99,
  "stock": 100,
  "category_id": 1,
  "farmer_id": 2,
  "image_url": "https://...",
  "expiration_date": "2025-02-05"
}
```

**Authentication Required**: Yes (FARMER/ADMIN)

---

#### PUT /products/{product_id}
Update product (FARMER/ADMIN)

**Request**
```json
{
  "price": 16.99,
  "stock": 80,
  "discount_price": 15.99
}
```

**Response** (200 OK)
```json
{
  "id": 1,
  "name": "Organic Tomatoes",
  "price": 16.99,
  "discount_price": 15.99,
  "stock": 80
}
```

---

### Category Endpoints

#### GET /categories
Get all categories

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "name": "Vegetables"
    },
    {
      "id": 2,
      "name": "Fruits"
    }
  ]
}
```

---

#### POST /categories
Create category (ADMIN)

**Request**
```json
{
  "name": "Dairy Products"
}
```

**Response** (201 Created)
```json
{
  "id": 3,
  "name": "Dairy Products"
}
```

---

### Cart Endpoints

#### GET /cart
Get user's shopping cart

**Authentication Required**: Yes (USER)

**Response** (200 OK)
```json
{
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Organic Tomatoes",
      "quantity": 2,
      "price": 25.99,
      "subtotal": 51.98
    }
  ],
  "total_items": 2,
  "cart_total": 51.98
}
```

---

#### POST /cart/add
Add item to cart

**Authentication Required**: Yes (USER)

**Request**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response** (201 Created)
```json
{
  "id": 1,
  "product_id": 1,
  "quantity": 2,
  "message": "Item added to cart"
}
```

---

#### PUT /cart/update/{cart_item_id}
Update cart item quantity

**Authentication Required**: Yes (USER)

**Request**
```json
{
  "quantity": 5
}
```

**Response** (200 OK)
```json
{
  "id": 1,
  "product_id": 1,
  "quantity": 5,
  "message": "Cart updated"
}
```

---

#### DELETE /cart/remove/{cart_item_id}
Remove item from cart

**Authentication Required**: Yes (USER)

**Response** (200 OK)
```json
{
  "message": "Item removed from cart"
}
```

---

### Order Endpoints

#### POST /orders
Create order from cart

**Authentication Required**: Yes (USER)

**Request**
```json
{
  "address": "123 Main Street, City",
  "payment_method": "credit_card"
}
```

**Response** (201 Created)
```json
{
  "id": 1,
  "user_id": 1,
  "total_price": 51.98,
  "address": "123 Main Street, City",
  "payment_method": "credit_card",
  "status": "created",
  "created_at": "2025-01-15T10:30:00",
  "items": [
    {
      "product_id": 1,
      "product_name": "Organic Tomatoes",
      "quantity": 2,
      "price": 25.99
    }
  ]
}
```

---

#### GET /orders
Get user's orders

**Authentication Required**: Yes (USER)

**Query Parameters**
- `skip`: Pagination offset
- `limit`: Items per page
- `status`: Filter by status (created, accepted, preparing, on_the_way, delivered)

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "total_price": 51.98,
      "status": "on_the_way",
      "address": "123 Main Street, City",
      "created_at": "2025-01-15T10:30:00",
      "courier": {
        "id": 3,
        "name": "Ivan P.",
        "phone": "+1234567890"
      }
    }
  ]
}
```

---

#### GET /orders/{order_id}
Get order details

**Authentication Required**: Yes (USER/ADMIN)

**Response** (200 OK)
```json
{
  "id": 1,
  "user_id": 1,
  "total_price": 51.98,
  "status": "on_the_way",
  "address": "123 Main Street, City",
  "created_at": "2025-01-15T10:30:00",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Organic Tomatoes",
      "quantity": 2,
      "price": 25.99
    }
  ],
  "courier": {
    "id": 3,
    "name": "Ivan P.",
    "phone": "+1234567890",
    "location": {
      "lat": 40.7128,
      "lng": -74.0060,
      "updated_at": "2025-01-15T10:45:00"
    }
  }
}
```

---

#### PUT /orders/{order_id}/status
Update order status (ADMIN/COURIER)

**Authentication Required**: Yes (ADMIN/COURIER)

**Request**
```json
{
  "status": "on_the_way"
}
```

**Response** (200 OK)
```json
{
  "id": 1,
  "status": "on_the_way",
  "message": "Order status updated"
}
```

---

### Courier Endpoints

#### GET /courier/available-orders
Get available orders for courier

**Authentication Required**: Yes (COURIER)

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "total_price": 51.98,
      "address": "123 Main Street, City",
      "status": "created",
      "items": [
        {
          "product_name": "Organic Tomatoes",
          "quantity": 2
        }
      ],
      "user": {
        "name": "John Doe",
        "phone": "+1234567890"
      }
    }
  ]
}
```

---

#### POST /courier/accept-order
Accept an order for delivery

**Authentication Required**: Yes (COURIER)

**Request**
```json
{
  "order_id": 1
}
```

**Response** (200 OK)
```json
{
  "order_id": 1,
  "status": "accepted",
  "message": "Order accepted successfully"
}
```

---

#### PUT /courier/location
Update courier real-time location

**Authentication Required**: Yes (COURIER)

**Request**
```json
{
  "lat": 40.7128,
  "lng": -74.0060
}
```

**Response** (200 OK)
```json
{
  "courier_id": 3,
  "lat": 40.7128,
  "lng": -74.0060,
  "updated_at": "2025-01-15T10:45:00"
}
```

---

### Admin Endpoints

#### GET /admin/orders
Get all orders (ADMIN)

**Authentication Required**: Yes (ADMIN)

**Query Parameters**
- `skip`: Pagination offset
- `limit`: Items per page
- `status`: Filter by status
- `user_id`: Filter by user

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "user": { "id": 1, "name": "John Doe" },
      "courier": { "id": 3, "name": "Ivan P." },
      "total_price": 51.98,
      "status": "on_the_way"
    }
  ],
  "total": 45
}
```

---

#### GET /admin/statistics
Get system statistics (ADMIN)

**Authentication Required**: Yes (ADMIN)

**Response** (200 OK)
```json
{
  "total_users": 100,
  "total_orders": 45,
  "total_revenue": 5000.00,
  "orders_today": 12,
  "pending_deliveries": 3,
  "avg_order_value": 111.11,
  "popular_products": [
    { "id": 1, "name": "Tomatoes", "sold": 50 }
  ]
}
```

---

#### GET /admin/products
Get all products for admin management (ADMIN)

**Authentication Required**: Yes (ADMIN)

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "name": "Organic Tomatoes",
      "price": 25.99,
      "stock": 50,
      "farmer": { "id": 2, "name": "Farm Inc." }
    }
  ]
}
```

---

### Farmer Endpoints

#### POST /farmer/products
Add product (FARMER)

**Authentication Required**: Yes (FARMER)

**Request**
```json
{
  "name": "Fresh Apples",
  "price": 35.99,
  "stock": 200,
  "category_id": 2,
  "image_url": "https://..."
}
```

**Response** (201 Created)
```json
{
  "id": 5,
  "name": "Fresh Apples",
  "price": 35.99,
  "stock": 200,
  "farmer_id": 2
}
```

---

#### GET /farmer/products
Get farmer's products (FARMER)

**Authentication Required**: Yes (FARMER)

**Response** (200 OK)
```json
{
  "data": [
    {
      "id": 1,
      "name": "Organic Tomatoes",
      "price": 25.99,
      "stock": 50,
      "sold_count": 120
    }
  ]
}
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error |

---

## Testing API Endpoints

### Using Swagger UI
1. Start backend: `uvicorn app.main:app --reload`
2. Open: `http://127.0.0.1:8000/docs`
3. Click on endpoint to expand
4. Click "Try it out"
5. Enter parameters and click "Execute"

### Using cURL
```bash
# Login
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Get products
curl -X GET "http://127.0.0.1:8000/products" \
  -H "Authorization: Bearer {token}"

# Create order
curl -X POST "http://127.0.0.1:8000/orders" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"address":"123 Main St","payment_method":"credit_card"}'
```

---

**Document Date**: December 2025  
**Version**: 1.0  
**Last Updated**: December 28, 2024
