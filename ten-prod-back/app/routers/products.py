from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.schemas import ProductOut, ProductCreate, CategoryOut, UserRole
from app.services import product_service
from app.utils.deps import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductOut])
async def read_products(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    return await product_service.get_products(db, skip, limit, category_id, search)

@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut)
async def create_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN.value, UserRole.FARMER.value]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Automatically assign farmer_id if user is a farmer
    if current_user.role == UserRole.FARMER.value:
        product.farmer_id = current_user.id
        
    return await product_service.create_product(db, product)
