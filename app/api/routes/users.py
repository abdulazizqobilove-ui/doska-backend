from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ... import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.get("/{user_id}/listings", response_model=List[schemas.ListingOut])
def get_user_listings(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Listing).filter(
        models.Listing.user_id == user_id,
        models.Listing.status == "active"
    ).order_by(models.Listing.created_at.desc()).all()

@router.get("/{user_id}/reviews", response_model=List[schemas.ReviewOut])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(
        models.Review.seller_id == user_id
    ).order_by(models.Review.created_at.desc()).all()

@router.post("/reviews", response_model=schemas.ReviewOut)
def create_review(
    body: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if body.seller_id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя оставить отзыв себе")
    review = models.Review(
        author_id=current_user.id,
        seller_id=body.seller_id,
        rating=body.rating,
        text=body.text,
        listing_title=body.listing_title,
    )
    db.add(review)
    # Recalculate seller rating
    seller = db.query(models.User).filter(models.User.id == body.seller_id).first()
    if seller:
        all_reviews = db.query(models.Review).filter(models.Review.seller_id == body.seller_id).all()
        total = sum(r.rating for r in all_reviews) + body.rating
        seller.rating = round(total / (len(all_reviews) + 1), 1)
        seller.reviews_count = len(all_reviews) + 1
    db.commit()
    db.refresh(review)
    return review
