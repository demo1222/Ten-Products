from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import OrderOut
from app.services import order_service
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/orders", response_model=List[OrderOut])
async def get_all_orders(db: AsyncSession = Depends(get_db), admin = Depends(get_current_admin)):
    return await order_service.get_orders(db)

