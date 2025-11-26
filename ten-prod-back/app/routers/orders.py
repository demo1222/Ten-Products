from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import OrderOut, OrderCreate, OrderStatus
from app.services import order_service
from app.utils.deps import get_current_user, get_current_user_with_role, UserRole

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
async def place_order(order: OrderCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return await order_service.create_order(db, current_user.id, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[OrderOut])
async def get_orders(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await order_service.get_orders(db, user_id=current_user.id)

@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    order = await order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != current_user.id and current_user.role != UserRole.ADMIN.value and current_user.role != UserRole.COURIER.value:
        raise HTTPException(status_code=403, detail="Not authorized")
    return order

