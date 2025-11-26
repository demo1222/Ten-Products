from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import Order, OrderItem, Product, OrderStatus, CartItem
from app.schemas import OrderCreate, OrderStatusUpdate
from app.services.cart_service import get_cart_items, clear_cart

async def create_order(db: AsyncSession, user_id: int, order_data: OrderCreate):
    # Get cart items
    cart_items = await get_cart_items(db, user_id)
    if not cart_items:
        raise ValueError("Cart is empty")
    
    total_price = 0
    order_items = []
    
    for item in cart_items:
        # Assuming item.product is loaded
        price = item.product.price
        if item.product.discount_price:
            price = item.product.discount_price
            
        total_price += price * item.quantity
        order_items.append(OrderItem(product_id=item.product_id, quantity=item.quantity, price=price))
    
    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        payment_method=order_data.payment_method,
        address=order_data.address,
        status=OrderStatus.CREATED.value
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    new_order_id = new_order.id
    
    for order_item in order_items:
        order_item.order_id = new_order_id
        db.add(order_item)
    
    await db.commit()
    
    # Refresh to get the relationships loaded properly before clearing cart?
    # Actually clearing cart deletes CartItems, not OrderItems.
    await clear_cart(db, user_id)
    
    # Return with items loaded - must eagerly load nested relationships
    # Pydantic tries to access these fields if they are in the schema
    query = select(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier),
        # selectinload(Product.farmer) is not in ProductOut schema, so not strictly needed, but safe to keep or remove.
        # Wait, ProductOut DOES NOT have 'farmer' field in schemas.py.
        # So I can remove .selectinload(Product.farmer) to be safe/clean.
    ).where(Order.id == new_order_id)
    
    result = await db.execute(query)
    return result.scalars().first()

async def get_orders(db: AsyncSession, user_id: int = None, skip: int = 0, limit: int = 100):
    query = select(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier)
    )
    if user_id:
        query = query.where(Order.user_id == user_id)
    query = query.offset(skip).limit(limit).order_by(Order.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_order(db: AsyncSession, order_id: int):
    query = select(Order).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier)
    ).where(Order.id == order_id)
    result = await db.execute(query)
    return result.scalars().first()

async def update_order_status(db: AsyncSession, order_id: int, status: str):
    order = await get_order(db, order_id)
    if order:
        order.status = status
        await db.commit()
        await db.refresh(order)
        # Re-fetch to ensure relationships are loaded for response
        return await get_order(db, order_id)
    return None

# Courier functions
async def get_unassigned_orders(db: AsyncSession):
    query = select(Order).where(Order.courier_id == None, Order.status == OrderStatus.CREATED.value).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def assign_order_to_courier(db: AsyncSession, order_id: int, courier_id: int):
    order = await get_order(db, order_id)
    if order and order.courier_id is None:
        order.courier_id = courier_id
        order.status = OrderStatus.ACCEPTED.value
        await db.commit()
        await db.refresh(order)
        
        # Need to reload with relations before returning
        return await get_order(db, order_id)
    return None

async def get_courier_orders(db: AsyncSession, courier_id: int):
    query = select(Order).where(Order.courier_id == courier_id).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier)
    )
    result = await db.execute(query)
    return result.scalars().all()
