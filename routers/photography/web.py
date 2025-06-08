from typing import Optional

from fastapi import APIRouter, Request, Query, Depends, Form, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select

from models import PhotographerSQL, PhotoSQL
from db_connection import get_session
from supabase_connection import upload_img_supabase
import operations as crud
from terms import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/info", response_class=HTMLResponse)
async def read_info(request:Request):
    return templates.TemplateResponse("info.html",{"request":request})


@router.get("/creador", response_class=HTMLResponse)
async def read_creador(request:Request):
    return templates.TemplateResponse("creador.html",{"request":request})


#all photographers
@router.get("/all_photographers", response_class=HTMLResponse)
async def photographers_list(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1),
        session: Session = Depends(get_session)
):
    total = await crud.count_photographers(session)
    offset = (page - 1) * per_page
    photographers = await crud.get_photographers_paginated(session, offset, limit = per_page)
    total_pages = (total + per_page - 1) // per_page
    return templates.TemplateResponse("photographers/list.html",
                                      {"request": request,
                                       "photographers": photographers,
                                       "page": page,
                                       "total_pages": total_pages,
                                       })

@router.get("/new_photographer", response_class=HTMLResponse)
async def add_photographer(request: Request):
    return templates.TemplateResponse("photographers/create.html",
                                      {"request": request,
                                       "genres":[genre.value for genre in Genre],
                                       "nationalities":[nationality.value for nationality in Nationality],
                                       "photographic_styles_name":[photographic_style_name.value for photographic_style_name in PhotographicStyle]})

@router.post("/new_photographer", response_class=HTMLResponse)
async def add_photographer_process(
        request: Request,
        name: str = Form(...),
        genre: Optional[Genre] = Form(None),
        nationality: Optional[Nationality] = Form(None),
        photographic_style_name: Optional[PhotographicStyle] = Form(None),
        is_alive:Optional[bool] = Form(None),
        photographer_image:Optional[UploadFile] = File(None),
        session: Session = Depends(get_session)
):
    if not photographer_image:
        raise HTTPException(status_code=400, detail="Debes subir una imagen")

    image_url = await upload_img_supabase(photographer_image, subfolder="photographers")

    photographer_data = PhotographerSQL(
        name=name,
        genre=genre,
        nationality=nationality,
        photographic_style_name=photographic_style_name,
        is_alive=is_alive,
        photographer_image_path=image_url
    )

    photographer = await crud.create_photographer(session, photographer_data)

    session.add(photographer)

    return RedirectResponse("/web/all_photographers", status_code=303)


@router.get("/search_photographer", response_class=HTMLResponse)
async def get_search(request: Request):
    return templates.TemplateResponse("photographers/search.html",
                                      {"request": request,
                                       "genres":[genre.value for genre in Genre],
                                       "nationalities": [nationality.value for nationality in Nationality],
                                       "photographic_styles_name":[photographic_style_name.value for photographic_style_name in PhotographicStyle]})

@router.post("/search_photographer", response_class=HTMLResponse)
async def get_search_process(
        request: Request,
        photographer_genre: Optional[str] = Form(None),
        photographer_nationality: Optional[str] = Form(None),
        photographer_style: Optional[str] = Form(None),
        is_alive: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):

    if not photographer_genre and not photographer_nationality and not photographer_style and not is_alive:
        return RedirectResponse("/web/all_photographers", status_code=303)


    genre_enum = Genre(photographer_genre) if photographer_genre else None
    nationality_enum = Nationality(photographer_nationality) if photographer_nationality else None
    style_enum = PhotographicStyle(photographer_style) if photographer_style else None

    if is_alive == "true":
        is_alive_bool = True
    elif is_alive == "false":
        is_alive_bool = False
    else:
        is_alive_bool = None

    photographer = await crud.filter_photographer(session, genre_enum, nationality_enum, style_enum, is_alive_bool)
    return templates.TemplateResponse("photographers/search.html",
                                      {"request": request,
                                       "photographer": photographer,
                                       "genres":[genre.value for genre in Genre],
                                       "nationalities":[nationality.value for nationality in Nationality],
                                       "photographic_styles_name":[photographic_style_name.value for photographic_style_name in PhotographicStyle]})

@router.get("/search_photographer_by_ID", response_class=HTMLResponse)
async def read_photographer(request:Request):
    return templates.TemplateResponse("photographers/search_by_id.html", {"request": request})

@router.post("/search_photographer_by_ID", response_class=HTMLResponse)
async def read_photographer_process(
        request: Request,
        photographer_id: Optional[int] = Form(None),
        session: Session = Depends(get_session)
):

    if not photographer_id:
        return RedirectResponse("/web/all_photographers", status_code=303)


    photographer = await crud.get_photographer(session, photographer_id)

    return templates.TemplateResponse("photographers/search_by_id.html",
                                      {"request": request,
                                       "photographer": photographer})

@router.get("/update_photographer", response_class=HTMLResponse)
async def modify_photographer(request: Request):
    return templates.TemplateResponse("photographers/update.html",
                                      {"request": request,
                                       "genres": [genre.value for genre in Genre],
                                       "nationalities": [nationality.value for nationality in Nationality],
                                       "photographic_styles_name": [photographic_style_name.value for
                                                                    photographic_style_name in PhotographicStyle]
                                       })

@router.post("/update_photographer", response_class=HTMLResponse)
async def modify_photographer_process(
        request: Request,
        photographer_id: Optional[int] = Form(None),
        name: str = Form(...),
        genre: Optional[Genre] = Form(None),
        nationality: Optional[Nationality] = Form(None),
        photographic_style_name: Optional[PhotographicStyle] = Form(None),
        is_alive:Optional[bool] = Form(None),
        photographer_image:Optional[UploadFile] = File(None),
        session: Session = Depends(get_session)
):
    if not photographer_image:
        raise HTTPException(status_code=400, detail="Debes subir una imagen")

    image_url = await upload_img_supabase(photographer_image, subfolder="photographers")

    photographer_data = PhotographerSQL(
        name=name,
        genre=genre,
        nationality=nationality,
        photographic_style_name=photographic_style_name,
        is_alive=is_alive,
        photographer_image_path=image_url
    )

    photographer = await crud.update_photographer(session, photographer_id, photographer_data.dict(exclude_unset=True))
    session.add(photographer)
    return RedirectResponse("/web/all_photographers", status_code=303)

@router.post("/inactive_photographer", response_class=HTMLResponse)
async def inactive_photographer(
        request: Request,
        photographer_id: Optional[int] = Form(...),
        session: Session = Depends(get_session)
):
    await crud.update_photographer(session, photographer_id, {"is_alive": False})
    return RedirectResponse("/web/all_photographers", status_code=303)

@router.post("/delete_photographer", response_class=HTMLResponse)
async def remove_photographer(
        request: Request,
        photographer_id: Optional[int] = Form(...),
        session: Session = Depends(get_session)
):
    await crud.update_photographer(session, photographer_id, {"is_deleted": True})
    return RedirectResponse("/web/all_photographers", status_code=303)


@router.get("/photographer_deleted", response_class=HTMLResponse)
async def get_deleted_photographer(
        request: Request,
        session: Session = Depends(get_session)
):
    query = select(PhotographerSQL).where(PhotographerSQL.is_deleted == True)
    results = await session.execute(query)
    deleted_photographers = results.scalars().all()

    return templates.TemplateResponse("photographers/deleted_list.html",
                                      {"request": request,
                                       "photographers": deleted_photographers})






#all photos
@router.get("/all_photos", response_class=HTMLResponse)
async def photos_list(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1),
        session: Session = Depends(get_session)
):
    total = await crud.count_photos(session)
    offset = (page - 1) * per_page
    photos = await crud.get_photos_paginated(session, offset, limit=per_page)
    total_pages = (total + per_page - 1) // per_page
    return templates.TemplateResponse("photos/list.html",
                                      {"request": request,
                                       "photos": photos,
                                       "page": page,
                                       "total_pages": total_pages})



@router.get("/new_photo", response_class=HTMLResponse)
async def add_photo(request: Request):
    return templates.TemplateResponse("photos/create.html",
                                      {"request": request,
                                       "categories":[category.value for category in PhotographicStyle]})

@router.post("/new_photo", response_class=HTMLResponse)
async def add_photo_process(
        request: Request,
        photographer_name: str = Form(...),
        title: Optional[str] = Form(None),
        category: Optional[PhotographicStyle] = Form(None),
        photo_created_at:Optional[int] = Form(None),
        photo_image:Optional[UploadFile] = File(None),
        session: Session = Depends(get_session)
):

    if not photo_image:
        raise HTTPException(status_code=400, detail="Debe subir una imagen")

    image_url = await upload_img_supabase(photo_image, subfolder="photos")

    photo_data = PhotoSQL(
        photographer_name=photographer_name,
        title=title,
        category=category,
        photo_created_at=photo_created_at,
        photo_image_path=image_url
    )

    photo = await crud.create_photo(session, photo_data)

    session.add(photo)

    return RedirectResponse("/web/all_photos", status_code=303)


@router.get("/search_photo_by_ID", response_class=HTMLResponse)
async def read_photo(request: Request):
    return templates.TemplateResponse("photos/search_by_id.html", {"request": request})

@router.post("/search_photo_by_ID", response_class=HTMLResponse)
async def read_photo_process(
        request: Request,
        photo_id: Optional[int] = Form(None),
        session: Session = Depends(get_session)
):
    if not photo_id:
        return RedirectResponse("/web/all_photos", status_code=303)

    photo = await crud.get_photo(session, photo_id)

    return templates.TemplateResponse("photos/search_by_id.html", {"request": request, "photo": photo})

@router.get("/search_photo_by_category", response_class=HTMLResponse)
async def get_photo_search(request: Request):
    return templates.TemplateResponse("photos/search.html",
                                      {"request": request,
                                       "categories": [category.value for category in PhotographicStyle]})

@router.post("/search_photo_by_category", response_class=HTMLResponse)
async def get_photo_search_process(
        request: Request,
        select_category: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):

    if not select_category:
        return RedirectResponse("/web/all_photos", status_code=303)

    category_enum = PhotographicStyle(select_category) if select_category else None

    photo = await crud.filter_photographer_photo(session, category_enum)
    return templates.TemplateResponse("photos/search.html",
                                      {"request": request,
                                       "photo": photo,
                                       "categories":[category.value for category in PhotographicStyle]})


@router.get("/update_photo", response_class=HTMLResponse)
async def modify_photo(request: Request):
    return templates.TemplateResponse("photos/update.html",
                                      {"request": request,
                                       "categories":[category.value for category in PhotographicStyle]})

@router.post("/update_photo", response_class=HTMLResponse)
async def modify_photo_process(
        request: Request,
        photo_id: Optional[int] = Form(None),
        photographer_name: str = Form(...),
        title: Optional[str] = Form(None),
        category: Optional[PhotographicStyle] = Form(None),
        photo_created_at:Optional[int] = Form(None),
        photo_image:Optional[UploadFile] = File(None),
        session: Session = Depends(get_session)
):

    if not photo_image:
        raise HTTPException(status_code=400, detail="Debe subir una imagen")

    image_url = await upload_img_supabase(photo_image, subfolder="photos")

    photo_data = PhotoSQL(
        photographer_name=photographer_name,
        title=title,
        category=category,
        photo_created_at=photo_created_at,
        photo_image_path=image_url
    )

    photo = await crud.update_photo(session, photo_id, photo_data.dict(exclude_unset=True))
    session.add(photo)
    return RedirectResponse("/web/all_photos", status_code=303)


@router.post("/delete_photo", response_class=HTMLResponse)
async def remove_photo(
        request: Request,
        photo_id: Optional[int] = Form(...),
        session: Session = Depends(get_session)
):
    await crud.update_photo(session, photo_id, {"is_deleted": True})
    return RedirectResponse("/web/all_photos", status_code=303)


@router.get("/photo_deleted", response_class=HTMLResponse)
async def get_deleted_photo(
        request: Request,
        session: Session = Depends(get_session)
):
    query = select(PhotoSQL).where(PhotoSQL.is_deleted == True)
    results = await session.execute(query)
    deleted_photos = results.scalars().all()

    return templates.TemplateResponse("photos/deleted_list.html",
                                      {"request": request,
                                       "photos": deleted_photos})


@router.get("/planeacion", response_class=HTMLResponse)
async def get_planeacion(request: Request):
    return templates.TemplateResponse("planeacion.html", {"request": request})


@router.get("/diseño", response_class=HTMLResponse)
async def get_disenio(request: Request):
    return templates.TemplateResponse("diseño.html", {"request": request})