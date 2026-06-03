from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .core.database import Base

class CategoryEnum(str, enum.Enum):
    realty = "realty"
    auto = "auto"
    jobs = "jobs"
    electronics = "electronics"
    clothing = "clothing"
    services = "services"
    furniture = "furniture"
    other = "other"

class ListingStatus(str, enum.Enum):
    active = "active"
    closed = "closed"
    pending = "pending"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(String(500), nullable=True)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    response_time = Column(String(50), default="~1 час")
    is_online = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    listings = relationship("Listing", back_populates="user")
    reviews_given = relationship("Review", foreign_keys="Review.author_id", back_populates="author")
    reviews_received = relationship("Review", foreign_keys="Review.seller_id", back_populates="seller")

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="UZS")
    category = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)
    status = Column(String(20), default="active")
    views = Column(Integer, default=0)
    is_promoted = Column(Boolean, default=False)
    promoted_until = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Realty fields
    realty_type = Column(String(50), nullable=True)
    deal_type = Column(String(20), nullable=True)
    rooms = Column(Integer, nullable=True)
    area = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    has_parking = Column(Boolean, default=False)
    has_furniture = Column(Boolean, default=False)
    has_appliances = Column(Boolean, default=False)

    # Auto fields
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    mileage = Column(Integer, nullable=True)
    transmission = Column(String(30), nullable=True)
    fuel_type = Column(String(30), nullable=True)
    engine_volume = Column(Float, nullable=True)
    color = Column(String(50), nullable=True)
    body_type = Column(String(50), nullable=True)
    owners_count = Column(Integer, nullable=True)
    has_accident = Column(Boolean, default=False)

    # Jobs fields
    listing_type = Column(String(20), nullable=True)
    job_type = Column(String(30), nullable=True)
    company = Column(String(200), nullable=True)
    experience = Column(String(100), nullable=True)
    salary = Column(Float, nullable=True)
    salary_to = Column(Float, nullable=True)
    schedule = Column(String(100), nullable=True)
    skills = Column(Text, nullable=True)  # JSON array stored as text

    user = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="listing", cascade="all, delete-orphan")

class ListingImage(Base):
    __tablename__ = "listing_images"
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    url = Column(String(500), nullable=False)
    order = Column(Integer, default=0)
    listing = relationship("Listing", back_populates="images")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    listing = relationship("Listing", back_populates="favorites")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    listing_title = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author = relationship("User", foreign_keys=[author_id], back_populates="reviews_given")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="reviews_received")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String(100), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
