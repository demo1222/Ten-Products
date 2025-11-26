from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import CourierLocation
from app.schemas import CourierLocationUpdate
from datetime import datetime

async def update_location(db: AsyncSession, courier_id: int, location: CourierLocationUpdate):
    query = select(CourierLocation).where(CourierLocation.courier_id == courier_id)
    result = await db.execute(query)
    loc = result.scalars().first()
    
    if loc:
        loc.lat = location.lat
        loc.lng = location.lng
        loc.updated_at = datetime.utcnow()
    else:
        loc = CourierLocation(courier_id=courier_id, lat=location.lat, lng=location.lng)
        db.add(loc)
    
    await db.commit()
    await db.refresh(loc)
    return loc

async def get_location(db: AsyncSession, courier_id: int):
    query = select(CourierLocation).where(CourierLocation.courier_id == courier_id)
    result = await db.execute(query)
    return result.scalars().first()

