from sqlalchemy import func
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from typing import Dict, Any
from models import PhotographerSQL, PhotoSQL
from terms import Genre, PhotographicStyle, Nationality
import matplotlib.pyplot as plt


#Creation of one photographer in DB
async def create_photographer(session: Session, photographer:PhotographerSQL):
    db_photographer = PhotographerSQL.model_validate(photographer, from_attributes=True)
    db_photographer.created_at = datetime.now()

    session.add(db_photographer)
    await session.commit()
    await session.refresh(db_photographer)

    return db_photographer

#Get photographer by the id
async def get_photographer(session:Session, photographer_id:int):
    query = select(PhotographerSQL).where(
        PhotographerSQL.id == photographer_id,
        PhotographerSQL.is_deleted == False
    )

    result = await session.execute(query)
    return result.scalar_one_or_none()


#Get all photographers of the list
"""async def get_all_photographers(session:Session):
    query = select(PhotographerSQL).where(PhotographerSQL.is_deleted == False)
    results = await session.exec(query)
    photographers = results.all()
    return photographers"""

async def count_photographers(session: Session) -> int:
    result = await session.execute(select(func.count()).select_from(PhotographerSQL))
    return result.scalar_one()

async def get_photographers_paginated(session: Session, offset: int, limit: int):
    result = await session.execute(select(PhotographerSQL).offset(offset).limit(limit))
    return result.scalars().all()

#update photographer
async def update_photographer(session:Session, photographer_id:int, photographer_update:Dict[str, Any]):
    photographer = await session.get(PhotographerSQL, photographer_id)
    if photographer is None:
        return None

    photographer_data = photographer.dict()
    for key, value in photographer_update.items():
        if value is not None:
            photographer_data[key]=value

    photographer_data["updated_at"] = datetime.now()

    for key, value in photographer_data.items():
        setattr(photographer, key, value)

    session.add(photographer)
    await session.commit()
    await session.refresh(photographer)

    return photographer

#Modify photographer status.
"""async def mark_photographer_inactive(session:Session, photographer_id:int):
    return await update_photographer(session, photographer_id, {"is_alive":False})"""

async def filter_photographer(
        session:Session,
        photographer_genre:Genre,
        photographer_nationality:Nationality,
        photographer_style:PhotographicStyle,
        is_alive:bool
):

    query = select(PhotographerSQL)

    if photographer_genre:
        query = query.where(PhotographerSQL.genre == photographer_genre)

    if photographer_nationality:
        query = query.where(PhotographerSQL.nationality == photographer_nationality)

    if photographer_style:
        query = query.where(PhotographerSQL.photographic_style_name == photographer_style)

    if is_alive is not None:
        query = query.where(PhotographerSQL.is_alive == is_alive)

    query = query.where(PhotographerSQL.is_deleted == False)

    results = await session.execute(query)
    photographers = results.scalars().all()
    return photographers

#filter by genre
"""async def filter_genre(session:Session, photographer_genre:Genre):
    query = (select(PhotographerSQL).where(PhotographerSQL.genre == photographer_genre))
    result = await session.execute(query)

    genre = result.scalars().all()

    return genre

#filter by nacionality
async def filter_nationality(session:Session, photographer_nationality:Nationality):
    query = (select(PhotographerSQL).where(PhotographerSQL.nationality == photographer_nationality))
    result = await session.execute(query)
    nationality = result.scalars().all()
    return nationality"""


#Creation of one photo in DB
async def create_photo(session: Session, photo:PhotoSQL):
    db_photo = PhotoSQL.model_validate(photo, from_attributes=True)
    db_photo.created_at = datetime.now()

    session.add(db_photo)
    await session.commit()
    await session.refresh(db_photo)

    return db_photo

#Get photo by the id
async def get_photo(session:Session, photo_id:int):
    query = select(PhotoSQL).where(
        PhotoSQL.id == photo_id,
        PhotoSQL.is_deleted == False
    )

    result = await session.execute(query)
    return result.scalar_one_or_none()


#Get all photos of the list
"""async def get_all_photos(session:Session):
    query = select(PhotoSQL).where(PhotoSQL.is_deleted == False)
    results = await session.exec(query)
    photos = results.all()
    return photos"""

#update photo
async def update_photo(session:Session, photo_id:int, photo_update:Dict[str, Any]):
    photo = await session.get(PhotoSQL, photo_id)
    if photo is None:
        return None

    photo_data = photo.dict()
    for key, value in photo_update.items():
        if value is not None:
            photo_data[key]=value

    photo_data["updated_at"] = datetime.now()

    for key, value in photo_data.items():
        setattr(photo, key, value)

    session.add(photo)
    await session.commit()
    await session.refresh(photo)

    return photo


async def filter_photographer_photo(session:Session, select_category:PhotographicStyle):
    query = (select(PhotoSQL).where(PhotoSQL.category == select_category, PhotoSQL.is_deleted == False))
    result = await session.execute(query)
    photo_category = result.scalars().all()
    return photo_category


async def count_photos(session: Session) -> int:
    result = await session.execute(select(func.count()).select_from(PhotoSQL))
    return result.scalar_one()


async def get_photos_paginated(session: Session, offset: int, limit: int):
    result = await session.execute(select(PhotoSQL).offset(offset).limit(limit))
    return result.scalars().all()




#------------------------------
#gráfica

paises = ['India', 'México', 'España', 'Brasil', 'Italia', 'Sudáfrica', 'USA', 'China', 'Francia', 'Japón']
porcentajes = [35, 26, 24, 22, 22, 20, 19, 19, 17, 10]

plt.figure(figsize=(10, 6))
plt.bar(paises, porcentajes, color='#600000')
plt.title("¡Foto aquí, foto allá!", fontsize=14)
plt.ylabel("Porcentaje (%)")
plt.xlabel("Países encuestados")
plt.ylim(0, 40)
for i, v in enumerate(porcentajes):
    plt.text(i, v + 1, f"{v}%", ha='center')
plt.tight_layout()

plt.savefig("images/photographic_images/grafica.png")