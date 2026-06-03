from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
    email: Optional[str] = None

class UserLogin(BaseModel):
    phone: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    avatar: Optional[str]
    rating: float
    reviews_count: int
    is_verified: bool
    response_time: str
    is_online: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ImageOut(BaseModel):
    id: int
    url: str
    order: int
    class Config:
        from_attributes = True

class ListingCreate(BaseModel):
    title: str
    description: str
    price: float
    currency: str = "UZS"
    category: str
    city: str
    location: Optional[str] = None
    # Realty
    realty_type: Optional[str] = None
    deal_type: Optional[str] = None
    rooms: Optional[int] = None
    area: Optional[float] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    has_parking: bool = False
    has_furniture: bool = False
    has_appliances: bool = False
    # Auto
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    mileage: Optional[int] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    engine_volume: Optional[float] = None
    color: Optional[str] = None
    body_type: Optional[str] = None
    owners_count: Optional[int] = None
    has_accident: bool = False
    # Jobs
    listing_type: Optional[str] = None
    job_type: Optional[str] = None
    company: Optional[str] = None
    experience: Optional[str] = None
    salary: Optional[float] = None
    salary_to: Optional[float] = None
    schedule: Optional[str] = None
    skills: Optional[str] = None

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[str] = None

class ListingOut(BaseModel):
    id: int
    title: str
    description: str
    price: float
    currency: str
    category: str
    city: str
    location: Optional[str]
    status: str
    views: int
    is_promoted: bool
    promoted_until: Optional[datetime]
    created_at: datetime
    user_id: int
    user: UserOut
    images: List[ImageOut] = []
    # Realty
    realty_type: Optional[str] = None
    deal_type: Optional[str] = None
    rooms: Optional[int] = None
    area: Optional[float] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    has_parking: bool = False
    has_furniture: bool = False
    has_appliances: bool = False
    # Auto
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    mileage: Optional[int] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    engine_volume: Optional[float] = None
    color: Optional[str] = None
    body_type: Optional[str] = None
    owners_count: Optional[int] = None
    has_accident: bool = False
    # Jobs
    listing_type: Optional[str] = None
    job_type: Optional[str] = None
    company: Optional[str] = None
    experience: Optional[str] = None
    salary: Optional[float] = None
    salary_to: Optional[float] = None
    schedule: Optional[str] = None
    skills: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    seller_id: int
    rating: int
    text: str
    listing_title: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    author_id: int
    seller_id: int
    rating: int
    text: str
    listing_title: Optional[str]
    created_at: datetime
    author: UserOut
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    chat_id: str
    text: str

class MessageOut(BaseModel):
    id: int
    chat_id: str
    sender_id: int
    text: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True
