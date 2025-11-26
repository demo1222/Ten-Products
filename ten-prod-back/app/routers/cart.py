from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import CartItemOut, CartItemCreate, CartItemUpdate
from app.services import cart_service
from app.utils.deps import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartItemOut])
async def get_cart(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await cart_service.get_cart_items(db, current_user.id)

@router.post("/", response_model=CartItemOut)
async def add_to_cart(item: CartItemCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await cart_service.add_to_cart(db, current_user.id, item)

@router.put("/{item_id}", response_model=CartItemOut)
async def update_cart_item(item_id: int, item: CartItemUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    updated = await cart_service.update_cart_item(db, current_user.id, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
async def remove_cart_item(item_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    success = await cart_service.remove_cart_item(db, current_user.id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item removed"}

