from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.models import UserRole, OrderStatus

# --- Auth & User ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

# --- Categories & Suppliers ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class SupplierBase(BaseModel):
    name: str

class SupplierCreate(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id: int
    class Config:
        from_attributes = True

# --- Products ---
class ProductBase(BaseModel):
    name: str
    price: float
    discount_price: Optional[float] = None
    stock: int = 0
    expiration_date: Optional[datetime] = None
    category_id: int
    supplier_id: Optional[int] = None
    farmer_id: Optional[int] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    discount_price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    farmer_id: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    category: Optional[CategoryOut] = None
    supplier: Optional[SupplierOut] = None
    class Config:
        from_attributes = True

# --- Cart ---
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemOut(CartItemBase):
    id: int
    product: Optional[ProductOut] = None
    class Config:
        from_attributes = True

class CartOut(BaseModel):
    items: List[CartItemOut]
    total_price: float

# --- Orders ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemOut(OrderItemBase):
    id: int
    price: float
    product: ProductOut
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    address: str
    payment_method: str

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderOut(BaseModel):
    id: int
    user_id: int
    courier_id: Optional[int] = None
    total_price: float
    payment_method: str
    address: str
    status: str
    created_at: datetime
    items: List[OrderItemOut]
    
    class Config:
        from_attributes = True

# --- Courier ---
class CourierLocationUpdate(BaseModel):
    lat: float
    lng: float

class CourierLocationOut(CourierLocationUpdate):
    courier_id: int
    updated_at: datetime
    class Config:
        from_attributes = True

# --- Feedback ---
class FeedbackCreate(BaseModel):
    order_id: int
    rating: int
    comment: Optional[str] = None

class FeedbackOut(FeedbackCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

