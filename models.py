from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel, Relationship
from terms import *

class PhotographerBase(SQLModel):
    name:str = Field(min_length=3, max_length=50)
    genre: Optional[Genre] = Field(default=None)
    nationality: Optional[Nationality] = Field(default=None)
    photographic_style_name: Optional[PhotographicStyle]= Field(default=None)
    is_alive: Optional[bool] = Field(default=True)

    photographer_image_path: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    is_deleted: Optional[bool] = Field(default=False)


class PhotoBase(SQLModel):
    photographer_id: Optional[int] = Field(foreign_key="photographers.id")
    photographer_name: Optional[str] = Field(min_length=1, max_length=20)
    title: Optional[str] = Field(min_length=1, max_length=500)
    category: Optional[PhotographicStyle] = Field(default=None)
    photo_created_at: Optional[int] = Field(default=None)

    photo_image_path: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    is_deleted: Optional[bool] = Field(default=False)

class PhotoSQL(PhotoBase, table=True):
    __tablename__ = "photos"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)

    photographer: Optional["PhotographerSQL"] = Relationship(back_populates="photos")

class PhotographerSQL(PhotographerBase, table=True):
    __tablename__ = "photographers"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)

    photos: List[PhotoSQL] = Relationship(back_populates="photographer")

