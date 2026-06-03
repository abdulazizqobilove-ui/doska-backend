import os, json, uuid
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from ...core.database import get_db
from ...core.config import settings
from ... import models, schemas
from ..deps import get_current_user, get_current_user_optional

router = APIRouter(prefix="/listings", tags=["listings"])

@router.get("", response_model=List[schemas.ListingOut])
def get_listings(
    category: Optional[str] = None,
    city: Optional[str] = None,
    q: Optional[str] = None,
    sort: str = "date",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
):
    query = db.query(models.Listing).filter(models.Listing.status == "active")
    if category:
        query = query.filter(models.Listing.category == category)
    if city:
        query = query.filter(models.Listing.city == city)
    if q:
        query = query.filter(models.Listing.title.ilike(f"%{q}%"))
    if sort == "price_asc":
        query = query.order_by(models.Listing.price.asc())
    elif sort == "price_desc":
        query = query.order_by(models.Listing.price.desc())
    elif sort == "views":
        query = query.order_by(models.Listing.views.desc())
    else:
        query = query.order_by(models.Listing.created_at.desc())
    return query.offset(skip).limit(limit).all()

@router.get("/{listing_id}", response_model=schemas.ListingOut)
def get_listing(
    listing_id: int,
    db: Session = Depends(get_db),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    listing.views += 1
    db.commit()
    db.refresh(listing)
    return listing

@router.post("", response_model=schemas.ListingOut)
def create_listing(
    body: schemas.ListingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    listing = models.Listing(**body.model_dump(), user_id=current_user.id)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

@router.patch("/{listing_id}", response_model=schemas.ListingOut)
def update_listing(
    listing_id: int,
    body: schemas.ListingUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id,
        models.Listing.user_id == current_user.id,
    ).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Не найдено")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(listing, k, v)
    db.commit()
    db.refresh(listing)
    return listing

@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id,
        models.Listing.user_id == current_user.id,
    ).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Не найдено")
    db.delete(listing)
    db.commit()
    return {"ok": True}

@router.post("/{listing_id}/images")
async def upload_images(
    listing_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id,
        models.Listing.user_id == current_user.id,
    ).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Не найдено")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    urls = []
    for i, file in enumerate(files[:10]):
        ext = os.path.splitext(file.filename or "img.jpg")[1] or ".jpg"
        fname = f"{uuid.uuid4()}{ext}"
        path = os.path.join(settings.UPLOAD_DIR, fname)
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        img = models.ListingImage(listing_id=listing_id, url=f"/uploads/{fname}", order=i)
        db.add(img)
        urls.append(f"/uploads/{fname}")
    db.commit()
    return {"urls": urls}

@router.post("/{listing_id}/favorite")
def toggle_favorite(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    fav = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.listing_id == listing_id,
    ).first()
    if fav:
        db.delete(fav)
        db.commit()
        return {"is_favorite": False}
    db.add(models.Favorite(user_id=current_user.id, listing_id=listing_id))
    db.commit()
    return {"is_favorite": True}

@router.get("/my/all", response_model=List[schemas.ListingOut])
def get_my_listings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Listing).filter(
        models.Listing.user_id == current_user.id
    ).order_by(models.Listing.created_at.desc()).all()
