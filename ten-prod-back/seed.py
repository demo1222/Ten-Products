import asyncio
from app.database import SessionLocal, engine, Base
from app.models import User, Category, Product, UserRole
from app.utils.security import get_password_hash

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # Users
        admin = User(email="admin@example.com", name="Admin", hashed_password=get_password_hash("admin"), role=UserRole.ADMIN.value)
        user = User(email="anna@example.com", name="Anna K.", hashed_password=get_password_hash("user"), role=UserRole.USER.value, address="Nevsky Ave, 12")
        courier = User(email="ivan@example.com", name="Ivan P.", hashed_password=get_password_hash("courier"), role=UserRole.COURIER.value)
        farmer = User(email="farmer@example.com", name="Oleg F.", hashed_password=get_password_hash("farmer"), role=UserRole.FARMER.value)
        
        db.add(admin)
        db.add(user)
        db.add(courier)
        db.add(farmer)
        
        # Categories
        vegetables = Category(name="Vegetables")
        dairy = Category(name="Dairy")
        bakery = Category(name="Bakery")
        fruits = Category(name="Fruits")
        
        db.add(vegetables)
        db.add(dairy)
        db.add(bakery)
        db.add(fruits)
        
        await db.commit()
        await db.refresh(vegetables)
        await db.refresh(dairy)
        await db.refresh(bakery)
        await db.refresh(fruits)
        await db.refresh(farmer)
        
        # Products
        p1 = Product(name="Russet Potatoes", price=80, category_id=vegetables.id, stock=100, image_url="https://placehold.co/600x400", farmer_id=farmer.id)
        p2 = Product(name="Organic Milk", price=95, category_id=dairy.id, stock=50, image_url="https://placehold.co/600x400", farmer_id=farmer.id)
        p3 = Product(name="Sourdough Bread", price=150, category_id=bakery.id, stock=30, image_url="https://placehold.co/600x400")
        p4 = Product(name="Bananas", price=60, category_id=fruits.id, stock=200, image_url="https://placehold.co/600x400")
        
        db.add(p1)
        db.add(p2)
        db.add(p3)
        db.add(p4)
        
        await db.commit()
        
        print("Seed data created successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
