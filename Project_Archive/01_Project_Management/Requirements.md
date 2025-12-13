# TenProducts - Requirements Document

## 1. Functional Requirements

### 1.1 Authentication & Authorization

#### User Registration (REQ-AUTH-001)
- Users can register with email and password
- System validates email format and uniqueness
- Password must be encrypted using bcrypt
- Default role assigned: USER
- Confirmation email sent (future feature)

#### User Login (REQ-AUTH-002)
- Users login with email and password
- System validates credentials against database
- JWT token issued on successful login
- Token includes user ID, email, and role
- Token expiration: 30 minutes
- Refresh token support (future)

#### Role-Based Access Control (REQ-AUTH-003)
- Four user roles: USER, FARMER, COURIER, ADMIN
- Each role has specific endpoint permissions
- Role assignment at registration or admin panel
- Role changes require admin authorization

### 1.2 Product Management

#### Browse Products (REQ-PROD-001)
- Users can view all products with pagination
- Products display: name, price, image, stock status
- Discount prices shown if available
- Expiration date displayed where applicable

#### Search & Filter (REQ-PROD-002)
- Search products by name
- Filter by category
- Filter by price range
- Filter by availability (in stock / out of stock)
- Sort by price, freshness, popularity

#### Product Details (REQ-PROD-003)
- View complete product information
- Display supplier/farmer information
- Show customer ratings and reviews
- Display availability and stock levels

#### Product Management (REQ-PROD-004) [Farmer/Admin]
- Farmers can add products to catalog
- Farmers can update product details
- Farmers can manage inventory levels
- Admin can moderate products
- Admin can adjust pricing
- Admin can create/manage categories

### 1.3 Shopping Cart

#### Cart Operations (REQ-CART-001)
- Add items to cart with quantity
- Update item quantities
- Remove items from cart
- View cart contents
- Cart persists across sessions (localStorage)

#### Cart Calculations (REQ-CART-002)
- Calculate subtotal
- Apply discounts
- Calculate taxes (if applicable)
- Calculate total with delivery fee
- Display item-by-item breakdown

### 1.4 Orders

#### Order Creation (REQ-ORDER-001)
- Users can place orders from cart
- Delivery address required
- Payment method selection
- Order summary before confirmation
- Order confirmation number generated

#### Order Tracking (REQ-ORDER-002)
- Users can view order status
- Real-time status updates
- Order history accessible
- Delivery address and ETA displayed
- Courier contact information shown

#### Order Management (REQ-ORDER-003) [Admin/Courier]
- View all orders (admin)
- Filter orders by status
- Update order status
- Assign courier to order
- Cancel orders (with conditions)

#### Order Status Workflow (REQ-ORDER-004)
- Status sequence: CREATED → ACCEPTED → PREPARING → ON_THE_WAY → DELIVERED
- Cancellation possible at CREATED/ACCEPTED stages
- Status change notifications sent to user

### 1.5 Courier Management

#### Courier Authentication (REQ-COURIER-001)
- Courier login with email/password
- Courier-specific dashboard
- Real-time order availability view

#### Order Acceptance (REQ-COURIER-002)
- Couriers see available orders (created status)
- Accept order with one click
- Order assigned to courier
- Estimated delivery time calculated
- Route optimization applied

#### Location Tracking (REQ-COURIER-003)
- Couriers can update real-time location
- Location stored in database (lat/lng)
- Location shared with customer (future)
- GPS tracking support (future)

#### Delivery Updates (REQ-COURIER-004)
- Update order status (accepted, preparing, on_the_way, delivered)
- Add delivery notes
- Photo proof of delivery (future)
- Signature capture (future)

### 1.6 Farmer Features

#### Product Catalog (REQ-FARMER-001)
- Farmers can list their products
- Set pricing and discounts
- Manage inventory quantities
- Set expiration dates
- Upload product images

#### Order Fulfillment (REQ-FARMER-002)
- View orders containing their products
- Prepare products for delivery
- Update product availability
- Track delivery progress

#### Performance Analytics (REQ-FARMER-003)
- View sales statistics
- Track popular products
- Monitor customer ratings
- Revenue reports

### 1.7 Admin Dashboard

#### User Management (REQ-ADMIN-001)
- View all users with roles
- Create/modify/delete users
- Assign roles to users
- View user activity logs

#### Product Management (REQ-ADMIN-002)
- Approve new products
- Moderate product listings
- Manage categories
- Adjust pricing
- Monitor inventory

#### Order Management (REQ-ADMIN-003)
- View all orders system-wide
- Filter and search orders
- Update order status
- Refund orders
- Generate order reports

#### Analytics & Reporting (REQ-ADMIN-004)
- Daily order statistics
- Revenue tracking
- User growth metrics
- Popular products
- Farmer performance
- Courier performance

#### System Configuration (REQ-ADMIN-005)
- Manage delivery zones
- Set delivery fees
- Configure system settings
- Manage notifications

---

## 2. Non-Functional Requirements

### 2.1 Performance (REQ-PERF-001)
- API response time: <200ms (95th percentile)
- Page load time: <2 seconds
- Database query time: <50ms
- Concurrent user support: 1000+ users
- Handle 100+ orders/hour

### 2.2 Availability & Reliability (REQ-AVAIL-001)
- System uptime: 99.5% (excluding maintenance)
- Graceful degradation during issues
- Automatic failover support (future)
- Data backup: daily backups
- Recovery time objective: 1 hour

### 2.3 Security (REQ-SEC-001)
- HTTPS for all communications
- JWT token-based authentication
- Password encryption (bcrypt)
- SQL injection prevention (ORM)
- CORS configured appropriately
- Rate limiting (future)
- Two-factor authentication (future)

### 2.4 Scalability (REQ-SCALE-001)
- Horizontal scaling support
- Database connection pooling
- Caching strategy (Redis - future)
- Static asset CDN support
- Load balancing ready

### 2.5 Usability (REQ-USAB-001)
- Mobile responsive design
- Intuitive navigation
- Accessible (WCAG 2.1 AA - future)
- Consistent UI/UX
- Support for dark mode

### 2.6 Maintainability (REQ-MAINT-001)
- Clean, modular code architecture
- Comprehensive code documentation
- API documentation (OpenAPI/Swagger)
- Database schema documentation
- Clear separation of concerns

---

## 3. Data Requirements

### 3.1 Data Models

#### User
- id (Primary Key)
- name (String)
- email (String, Unique)
- phone (String)
- hashed_password (String)
- address (String)
- role (Enum: USER, FARMER, COURIER, ADMIN)
- created_at (DateTime)
- updated_at (DateTime)

#### Product
- id (Primary Key)
- name (String)
- price (Float)
- discount_price (Float, Optional)
- stock (Integer)
- expiration_date (DateTime, Optional)
- category_id (Foreign Key)
- farmer_id (Foreign Key)
- image_url (String)
- created_at (DateTime)

#### Category
- id (Primary Key)
- name (String, Unique)
- description (String, Optional)

#### Order
- id (Primary Key)
- user_id (Foreign Key)
- courier_id (Foreign Key, Optional)
- total_price (Float)
- payment_method (String)
- address (String)
- status (Enum)
- created_at (DateTime)
- delivered_at (DateTime, Optional)

#### OrderItem
- id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity (Integer)
- price (Float)

#### CartItem
- id (Primary Key)
- user_id (Foreign Key)
- product_id (Foreign Key)
- quantity (Integer)

#### CourierLocation
- courier_id (Primary Key)
- lat (Float)
- lng (Float)
- updated_at (DateTime)

#### Feedback
- id (Primary Key)
- user_id (Foreign Key)
- order_id (Foreign Key)
- rating (Integer, 1-5)
- comment (String, Optional)

### 3.2 Data Validation

- Email: Valid format (RFC 5322)
- Password: Minimum 6 characters, encrypted
- Price: Positive number, max 2 decimal places
- Quantity: Positive integer
- Rating: Integer between 1-5
- Phone: Valid format (optional)
- Address: Minimum 10 characters

---

## 4. Integration Requirements

### 4.1 Frontend-Backend Integration
- RESTful API endpoints
- JSON request/response format
- Standardized error responses
- CORS properly configured

### 4.2 External Services (Future)
- Payment Gateway (Stripe, PayPal)
- Email Service (SendGrid, AWS SES)
- SMS Service (Twilio)
- Maps API (Google Maps)
- File Storage (AWS S3)

---

## 5. Compliance & Standards

### 5.1 Data Protection
- GDPR compliance (EU users)
- Data encryption at rest
- Secure password storage
- Audit logging

### 5.2 Business Rules
- Orders only from in-stock products
- No negative prices/quantities
- Delivery address required
- User can only view own orders
- Farmers can only manage own products

---

## 6. User Stories

### User (Customer)
- **As a** customer, **I want to** browse fresh products from local farmers **so that** I can find quality produce
- **As a** customer, **I want to** add items to cart and checkout **so that** I can purchase products
- **As a** customer, **I want to** track my delivery in real-time **so that** I know when to expect my order
- **As a** customer, **I want to** rate and review products **so that** I can share my experience

### Farmer
- **As a** farmer, **I want to** list my products on the platform **so that** I can reach more customers
- **As a** farmer, **I want to** manage my inventory **so that** I don't oversell
- **As a** farmer, **I want to** view my sales and earnings **so that** I can track my business

### Courier
- **As a** courier, **I want to** see available orders **so that** I can choose deliveries
- **As a** courier, **I want to** update delivery status **so that** customers know progress
- **As a** courier, **I want to** track my location **so that** customer can find me

### Admin
- **As an** admin, **I want to** manage all orders **so that** I can oversee operations
- **As an** admin, **I want to** view system analytics **so that** I can make data-driven decisions
- **As an** admin, **I want to** manage users and products **so that** I can maintain platform quality

---

## 7. Acceptance Criteria

### Release Criteria
- ✅ All critical features implemented
- ✅ 80% code coverage with unit tests
- ✅ All endpoints documented and tested
- ✅ No critical security vulnerabilities
- ✅ Performance benchmarks met
- ✅ User documentation complete
- ✅ Database migrations tested

---

**Document Date**: December 2025  
**Version**: 1.0  
**Status**: Finalized
