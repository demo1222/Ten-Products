from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import CategoryOut, CategoryCreate
from app.services import product_service
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryOut])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await product_service.get_categories(db)

@router.post("/", response_model=CategoryOut, dependencies=[Depends(get_current_admin)])
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_category(db, category)

