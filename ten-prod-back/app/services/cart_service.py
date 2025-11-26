from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import CartItem, Product
from app.schemas import CartItemCreate, CartItemUpdate

async def get_cart_items(db: AsyncSession, user_id: int):
    # Need to load product.category and product.supplier as well if they are in the response schema
    query = select(CartItem).options(
        selectinload(CartItem.product).selectinload(Product.category),
        selectinload(CartItem.product).selectinload(Product.supplier)
    ).where(CartItem.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()

async def add_to_cart(db: AsyncSession, user_id: int, item: CartItemCreate):
    # Check if item exists
    query = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == item.product_id)
    result = await db.execute(query)
    existing_item = result.scalars().first()
    
    if existing_item:
        existing_item.quantity += item.quantity
        await db.commit()
        await db.refresh(existing_item)
        
        # Reload with product relationship
        query = select(CartItem).options(
            selectinload(CartItem.product).selectinload(Product.category),
            selectinload(CartItem.product).selectinload(Product.supplier)
        ).where(CartItem.id == existing_item.id)
        result = await db.execute(query)
        return result.scalars().first()
    else:
        new_item = CartItem(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        
        # Reload with product relationship
        query = select(CartItem).options(
            selectinload(CartItem.product).selectinload(Product.category),
            selectinload(CartItem.product).selectinload(Product.supplier)
        ).where(CartItem.id == new_item.id)
        result = await db.execute(query)
        return result.scalars().first()

async def update_cart_item(db: AsyncSession, user_id: int, item_id: int, update: CartItemUpdate):
    query = select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
    result = await db.execute(query)
    item = result.scalars().first()
    if item:
        item.quantity = update.quantity
        await db.commit()
        await db.refresh(item)
        
        # Reload with product relationship
        query = select(CartItem).options(
            selectinload(CartItem.product).selectinload(Product.category),
            selectinload(CartItem.product).selectinload(Product.supplier)
        ).where(CartItem.id == item.id)
        result = await db.execute(query)
        return result.scalars().first()
    return None

async def remove_cart_item(db: AsyncSession, user_id: int, item_id: int):
    query = select(CartItem).where(CartItem.id == item_id, CartItem.user_id == user_id)
    result = await db.execute(query)
    item = result.scalars().first()
    if item:
        await db.delete(item)
        await db.commit()
        return True
    return False

async def clear_cart(db: AsyncSession, user_id: int):
    query = select(CartItem).where(CartItem.user_id == user_id)
    result = await db.execute(query)
    items = result.scalars().all()
    for item in items:
        await db.delete(item)
    await db.commit()
