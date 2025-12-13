# TenProducts - Project Archive Documentation

## Project Overview

**TenProducts** is a modern fresh groceries delivery platform that connects local farmers with customers for fast, reliable delivery of fresh produce. The system supports multiple user roles including customers, farmers, couriers, and administrators.

### Key Features
- 🚚 **Fast Delivery**: ~15-minute delivery in city zones
- 💰 **Affordable**: 10% cheaper than supermarkets
- 👨‍🌾 **Local Farmers**: Support for 20+ local agricultural partners
- 📱 **Modern UI**: Responsive Next.js frontend
- 🔐 **Secure**: JWT-based authentication with role-based access control
- 📊 **Admin Dashboard**: Comprehensive order and inventory management

---

## Project Structure

```
Project_Archive/
│
├── 01_Project_Management/          # Project planning and management documents
│   ├── Proposal.md                  # Project proposal and business case
│   ├── Requirements.md              # Functional and technical requirements
│   └── Timeline.md                  # Project timeline and milestones
│
├── 02_Technical/                    # Technical documentation
│   ├── Architecture.md              # System architecture overview
│   ├── API_Docs.md                  # RESTful API documentation
│   ├── Database/
│   │   └── Database_Schema.md       # Database design and schema
│   └── Source_Code/                 # References to source code structure
│
├── 03_Deliverables/
│   └── Final_Deliverables_Checklist.md  # Deliverable verification checklist
│
├── 04_Reports/
│   ├── Final_Report.md              # Project final report
│   └── Test_Report.md               # Testing and QA results
│
├── 05_Lessons_Learned.md            # Project retrospective and insights
│
└── README.md                        # This file

```

---

## Quick Start Guide

### Prerequisites
- **Backend**: Python 3.8+, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Node.js 18+, Next.js 16, React 19, SCSS
- **Tools**: Git, npm/pip, Uvicorn

### Running the Backend (Fresh Groceries API)

1. **Install dependencies**:
   ```bash
   cd ten-prod-back
   pip install -r requirements.txt
   ```

2. **Seed the database** (optional):
   ```bash
   cd ten-prod-back
   python seed.py
   ```

3. **Start the server**:
   ```bash
   cd ten-prod-back
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **API Documentation**:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

### Running the Frontend (TenProducts Web App)

1. **Install dependencies**:
   ```bash
   cd ten-prod-front
   npm install
   ```

2. **Start development server**:
   ```bash
   cd ten-prod-front
   npm run dev
   ```

3. **Access the application**:
   - Open browser: http://localhost:3000

4. **Production build**:
   ```bash
   npm run build
   npm start
   ```

---

## Default Test Users

All users have password: `password` (after seeding)

| Email | Password | Role | Purpose |
|-------|----------|------|---------|
| admin@example.com | admin | Admin | System administration |
| anna@example.com | user | User | Browse and order products |
| ivan@example.com | courier | Courier | Accept and deliver orders |

---

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Async**: aiosqlite for async database operations
- **Security**: Passlib + bcrypt for password hashing
- **Validation**: Pydantic data models

### Frontend
- **Framework**: Next.js 16 (React 19)
- **Styling**: SCSS Modules
- **State Management**: React hooks + localStorage
- **HTTP Client**: Custom API wrapper
- **Build Tool**: Next.js with Turbopack

---

## API Endpoints Summary

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Products
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `GET /products/search` - Search products

### Categories
- `GET /categories` - List all categories
- `POST /categories` - Create category (Admin only)

### Cart
- `GET /cart` - Get user's cart
- `POST /cart/add` - Add item to cart
- `PUT /cart/update` - Update cart item
- `DELETE /cart/remove` - Remove from cart

### Orders
- `POST /orders` - Create order
- `GET /orders` - Get user's orders
- `GET /orders/{id}` - Get order details
- `PUT /orders/{id}/status` - Update order status

### Courier
- `GET /courier/available-orders` - List available orders
- `POST /courier/accept-order` - Accept an order
- `PUT /courier/location` - Update courier location

### Admin
- `GET /admin/orders` - View all orders
- `GET /admin/products` - Manage products
- `GET /admin/statistics` - View analytics

### Farmer
- `POST /farmer/products` - Add product to catalog
- `GET /farmer/products` - View farmer's products
- `PUT /farmer/products/{id}` - Update product

---

## Key System Entities

### User Roles
- **USER**: Customer who browses and orders products
- **FARMER**: Sells products to the platform
- **COURIER**: Accepts and delivers orders
- **ADMIN**: Manages inventory, categories, partners, and pricing

### Order Status Lifecycle
1. **CREATED** - Order just created, waiting for acceptance
2. **ACCEPTED** - Courier accepted the order
3. **PREPARING** - Preparation in progress
4. **ON_THE_WAY** - Delivery in progress
5. **DELIVERED** - Order successfully delivered
6. **CANCELLED** - Order cancelled

### Database Tables
- **users** - User accounts with roles and authentication
- **products** - Product catalog with pricing and stock
- **categories** - Product categories
- **suppliers** - Supplier/farmer information
- **orders** - Order records
- **order_items** - Individual items in orders
- **cart_items** - Shopping cart items
- **courier_locations** - Real-time courier location data
- **feedbacks** - Customer reviews and ratings

---

## Development Workflow

### Making Changes to Backend
1. Modify models in `app/models/models.py`
2. Create migration if schema changes (currently using alembic-free approach)
3. Update routers in `app/routers/`
4. Update services in `app/services/`
5. Test endpoints in Swagger UI at `/docs`

### Making Changes to Frontend
1. Create/modify components in `src/components/`
2. Update pages in `src/app/`
3. Adjust styles in corresponding `.module.scss` files
4. Test in development server
5. Build and verify production version

### CORS Configuration
- Backend allows all origins in development mode (`*`)
- Frontend points to `http://127.0.0.1:8000` by default
- Change `API_URL` in `src/utils/api.js` for production

---

## Security Considerations

### Current Setup (Development)
- CORS is open (`*`) for development convenience
- Secrets should be moved to environment variables
- JWT expiration: 30 minutes

### Production Recommendations
- Move `SECRET_KEY` and `DATABASE_URL` to `.env` file
- Restrict CORS to specific frontend domain
- Use HTTPS only
- Implement rate limiting
- Add input validation and sanitization
- Use environment-specific configurations

---

## Troubleshooting

### Backend Issues
**Port 8000 already in use**:
```bash
# Change port in Uvicorn command
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

**Database locked error**:
```bash
# Remove SQLite database and reseed
rm ten-prod-back/fresh_groceries.db
python ten-prod-back/seed.py
```

### Frontend Issues
**Port 3000 already in use**:
```bash
# Next.js will prompt for alternative port
npm run dev
```

**CORS/API errors**:
- Verify backend is running on `http://127.0.0.1:8000`
- Check network tab in browser dev tools
- Ensure token is properly stored in localStorage

---

## Project Metrics & Statistics

- **Backend**: ~500+ lines of Python code
- **Frontend**: ~1000+ lines of JSX/SCSS
- **Database**: 10 tables, normalized schema
- **API Endpoints**: 25+ RESTful endpoints
- **User Roles**: 4 distinct role types
- **Development Time**: Full-stack application
- **Test Coverage**: Unit tests and integration tests available

---

## Contact & Support

For issues or questions about this project:
- Review the specific documentation in each folder
- Check API documentation at http://127.0.0.1:8000/docs
- Review source code comments and docstrings
- Consult the Lessons Learned document for common issues

---

## Document Overview

| Document | Purpose |
|----------|---------|
| **01_Project_Management/** | Planning, requirements, timeline |
| **02_Technical/** | Architecture, API, database, code structure |
| **03_Deliverables/** | Checklist of project deliverables |
| **04_Reports/** | Final reports and test results |
| **05_Lessons_Learned.md** | Retrospective and insights |

---

**Last Updated**: December 2025  
**Project Status**: Complete  
**Version**: 1.0.0
