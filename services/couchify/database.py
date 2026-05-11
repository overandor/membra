"""PostgreSQL database models for booking-concierge."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="guest")
    stripe_account_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    verification_status: Mapped[str] = mapped_column(String, default="unverified")
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    spaces: Mapped[list["Space"]] = relationship(back_populates="host")
    bookings_guest: Mapped[list["Booking"]] = relationship(foreign_keys="Booking.guest_id", back_populates="guest")
    bookings_host: Mapped[list["Booking"]] = relationship(foreign_keys="Booking.host_id", back_populates="host")
    reviews_given: Mapped[list["Review"]] = relationship(foreign_keys="Review.reviewer_id", back_populates="reviewer")
    reviews_received: Mapped[list["Review"]] = relationship(foreign_keys="Review.reviewee_id", back_populates="reviewee")


class Space(Base):
    __tablename__ = "spaces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    host_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    space_type: Mapped[str] = mapped_column(String, nullable=False)
    neighborhood: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    capacity_seats: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price_per_minute: Mapped[float] = mapped_column(Numeric, nullable=False)
    minimum_minutes: Mapped[int] = mapped_column(Integer, default=10)
    maximum_minutes: Mapped[int] = mapped_column(Integer, default=180)
    privacy_score: Mapped[float] = mapped_column(Float, default=0.5)
    features: Mapped[list] = mapped_column(String, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    host: Mapped["User"] = relationship(back_populates="spaces")
    availability_windows: Mapped[list["AvailabilityWindow"]] = relationship(back_populates="space")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="space")


class AvailabilityWindow(Base):
    __tablename__ = "availability_windows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    space_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("spaces.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    auto_accept: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    space: Mapped["Space"] = relationship(back_populates="availability_windows")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guest_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    host_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    space_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("spaces.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    seat_count: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[float] = mapped_column(Numeric, nullable=False)
    platform_fee: Mapped[float] = mapped_column(Numeric, nullable=False)
    total: Mapped[float] = mapped_column(Numeric, nullable=False)
    check_in_code: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")
    payment_intent_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    check_in_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    check_out_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    guest: Mapped["User"] = relationship(foreign_keys=[guest_id], back_populates="bookings_guest")
    host: Mapped["User"] = relationship(foreign_keys=[host_id], back_populates="bookings_host")
    space: Mapped["Space"] = relationship(back_populates="bookings")
    review: Mapped[Optional["Review"]] = relationship(back_populates="booking")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    reviewer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reviewee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    booking: Mapped["Booking"] = relationship(back_populates="review")
    reviewer: Mapped["User"] = relationship(foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewee: Mapped["User"] = relationship(foreign_keys=[reviewee_id], back_populates="reviews_received")
