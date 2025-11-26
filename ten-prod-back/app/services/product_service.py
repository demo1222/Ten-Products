from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models import Product, Category, Supplier
from app.schemas import ProductCreate, ProductUpdate, CategoryCreate, SupplierCreate

# Product
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, search: Optional[str] = None):
    query = select(Product).options(selectinload(Product.category), selectinload(Product.supplier))
    if category_id:
        query = query.where(Product.category_id == category_id)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    query = select(Product).options(selectinload(Product.category), selectinload(Product.supplier)).where(Product.id == product_id)
    result = await db.execute(query)
    return result.scalars().first()

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    # We need to refresh the object to get the ID and defaults.
    # However, to return nested relationships (like category/supplier) in response_model, 
    # we must ensure they are loaded if the response model requires them.
    # The ProductOut schema has Optional[CategoryOut] and Optional[SupplierOut].
    # db.refresh(db_product) might not load relationships by default in async unless configured.
    # But usually for creation return, simple fields are enough if front-end handles it.
    # The error "MissingGreenlet" usually happens when Pydantic tries to access a lazy-loaded relationship that wasn't awaited.
    
    await db.refresh(db_product)
    
    # Explicitly reload with options to satisfy Pydantic serialization if it touches relationships
    # Or, simpler: just return the product and let Pydantic handle empty relationships if they are None.
    # The issue is likely that Pydantic tries to access `db_product.category` which is not loaded.
    # We can eager load it after refresh.
    
    query = select(Product).options(selectinload(Product.category), selectinload(Product.supplier)).where(Product.id == db_product.id)
    result = await db.execute(query)
    return result.scalars().first()

async def update_product(db: AsyncSession, product_id: int, product_update: ProductUpdate):
    db_product = await get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
        return True
    return False

# Category
async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()

async def create_category(db: AsyncSession, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

# Supplier
async def get_suppliers(db: AsyncSession):
    result = await db.execute(select(Supplier))
    return result.scalars().all()

async def create_supplier(db: AsyncSession, supplier: SupplierCreate):
    db_supplier = Supplier(name=supplier.name)
    db.add(db_supplier)
    await db.commit()
    await db.refresh(db_supplier)
    return db_supplier
