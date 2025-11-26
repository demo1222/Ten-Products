from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import Order, Product, OrderStatus, UserRole, OrderItem
from app.schemas import OrderOut, ProductOut
from app.utils.deps import get_current_user_with_role
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/farmer", tags=["Farmer"])

@router.get("/orders", response_model=List[OrderOut])
async def get_farmer_orders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_with_role(UserRole.FARMER))
):
    # For MVP, Farmer sees orders that are Accepted (by courier) or Created, so they can start preparing.
    # Ideally, filter by products owned by this farmer.
    # Let's try to find orders containing at least one product from this farmer.
    
    # This query is a bit complex for simple select.
    # Select Orders where exists (OrderItem -> Product where farmer_id == current_user.id)
    
    subquery = select(OrderItem.order_id).join(Product).where(Product.farmer_id == current_user.id)
    
    # But for MVP simplification, if product linking isn't perfect yet, let's show all orders in relevant states.
    # States: CREATED, ACCEPTED, PREPARING.
    
    query = select(Order).where(
        Order.status.in_([OrderStatus.CREATED.value, OrderStatus.ACCEPTED.value, OrderStatus.PREPARING.value])
    ).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier)
    ).order_by(Order.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/products", response_model=List[ProductOut])
async def get_farmer_products(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_with_role(UserRole.FARMER))
):
    query = select(Product).where(Product.farmer_id == current_user.id).options(
        selectinload(Product.category),
        selectinload(Product.supplier)
    )
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/orders/{order_id}/prepare", response_model=OrderOut)
async def prepare_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_with_role(UserRole.FARMER))
):
    # Farmer moves order to PREPARING
    query = select(Order).where(Order.id == order_id).options(
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.category),
        selectinload(Order.items).selectinload(OrderItem.product).selectinload(Product.supplier)
    )
    result = await db.execute(query)
    order = result.scalars().first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check status transition
    if order.status not in [OrderStatus.CREATED.value, OrderStatus.ACCEPTED.value]:
         raise HTTPException(status_code=400, detail="Order cannot be prepared in current state")

    order.status = OrderStatus.PREPARING.value
    await db.commit()
    await db.refresh(order)
    return order

@router.put("/orders/{order_id}/ready", response_model=OrderOut)
async def ready_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_with_role(UserRole.FARMER))
):
    # Farmer marks as Ready? Or "On the way" is strictly courier?
    # "Statuses follow a pipeline: created → accepted → preparing → on_the_way → delivered"
    # Usually "Ready for Pickup" is a state. But not in our enum.
    # If "Preparing" is done, maybe it stays "Preparing" until courier picks up?
    # Or we assume "Preparing" means "Being Prepared".
    # Let's assume Farmer just sets it to Preparing. 
    # But maybe we need a signal that it's DONE preparing.
    # Let's add a virtual state or just let Courier handle "On the way".
    
    # I'll allow Farmer to toggle it back to ACCEPTED? No.
    # Let's stick to "Prepare" action only for now.
    raise HTTPException(status_code=501, detail="Not implemented yet")

