# Fresh Groceries Backend

This is the backend for the Fresh Groceries Delivery service, built with FastAPI.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Seed the database:
   ```bash
   python seed.py
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Features

- **Auth**: JWT authentication with roles (user, farmer, courier, admin).
- **Products**: Browse and search products.
- **Cart**: Manage shopping cart.
- **Orders**: Place and track orders.
- **Courier**: Courier specific endpoints for accepting orders and updating status.
- **Admin**: Manage products and categories.

## Default Users (from seed)

- Admin: `admin@example.com` / `admin`
- User: `anna@example.com` / `user`
- Courier: `ivan@example.com` / `courier`

