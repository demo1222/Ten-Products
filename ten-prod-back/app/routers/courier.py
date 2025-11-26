from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import OrderOut, CourierLocationUpdate, CourierLocationOut
from app.services import order_service, courier_service
from app.utils.deps import get_current_user_with_role, UserRole
from app.models import OrderStatus

router = APIRouter(prefix="/courier", tags=["Courier"])

@router.get("/orders/available", response_model=List[OrderOut])
async def get_available_orders(
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user_with_role(UserRole.COURIER))
):
    return await order_service.get_unassigned_orders(db)

@router.post("/orders/{order_id}/accept", response_model=OrderOut)
async def accept_order(
    order_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user_with_role(UserRole.COURIER))
):
    order = await order_service.assign_order_to_courier(db, order_id, current_user.id)
    if not order:
         raise HTTPException(status_code=400, detail="Order not available or already assigned")
    return order

@router.get("/orders/my", response_model=List[OrderOut])
async def get_my_orders(
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user_with_role(UserRole.COURIER))
):
    return await order_service.get_courier_orders(db, current_user.id)

@router.put("/orders/{order_id}/status", response_model=OrderOut)
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user_with_role(UserRole.COURIER))
):
    order = await order_service.get_order(db, order_id)
    if not order or order.courier_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this order")
    
    return await order_service.update_order_status(db, order_id, status.value)

@router.post("/location", response_model=CourierLocationOut)
async def update_location(
    location: CourierLocationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_with_role(UserRole.COURIER))
):
    return await courier_service.update_location(db, current_user.id, location)

