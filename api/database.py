"""
MEMBRA Database Configuration

SQLAlchemy setup for PostgreSQL database with async support.
Includes all models for persistence.
"""
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

# Database URL - configure via environment variables
DATABASE_URL = "postgresql://user:password@localhost/membra"

# Create async engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    """User accounts"""
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    
    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    hero_house = relationship("HeroHouseDB", back_populates="host", uselist=False)


class WalletDB(Base):
    """Wallet persistence model"""
    __tablename__ = "wallets"
    
    wallet_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"))
    balance_credits = Column(Integer, default=0)
    balance_usd = Column(Float, default=0.0)
    total_earnings_usd = Column(Float, default=0.0)
    total_spent_usd = Column(Float, default=0.0)
    referral_rewards_credits = Column(Integer, default=0)
    cashback_credits = Column(Integer, default=0)
    deposit_balance_usd = Column(Float, default=0.0)
    loyalty_level = Column(String, default="bronze")
    reputation_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship("WalletTransactionDB", back_populates="wallet")


class WalletTransactionDB(Base):
    """Wallet transaction persistence"""
    __tablename__ = "wallet_transactions"
    
    transaction_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    wallet_id = Column(String, ForeignKey("wallets.wallet_id"))
    transaction_type = Column(String)  # credit_earn, credit_spend, deposit, withdrawal, payout, cashback, refund
    amount = Column(Float)
    currency = Column(String, default="USD")
    reference_id = Column(String, nullable=True)
    description = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    wallet = relationship("WalletDB", back_populates="transactions")


class HeroHouseDB(Base):
    """Hero House persistence"""
    __tablename__ = "hero_houses"
    
    house_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    host_id = Column(String, ForeignKey("users.user_id"))
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    house_type = Column(String)  # apartment, house, condo, townhouse
    capabilities = Column(JSON)  # List[str]
    storage_capacity_items = Column(Integer, default=0)
    storage_volume_cubic_ft = Column(Float, nullable=True)
    pickup_window_start = Column(String, default="08:00")
    pickup_window_end = Column(String, default="22:00")
    pickup_days = Column(JSON)  # List[str]
    rules = Column(JSON)  # List[str]
    amenities = Column(JSON)  # List[str]
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    host = relationship("User", back_populates="hero_house")


class AlphaHubDB(HeroHouseDB):
    """Alpha Hub persistence (inherits from HeroHouse)"""
    __tablename__ = "alpha_hubs"
    
    hub_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    house_id = Column(String, ForeignKey("hero_houses.house_id"))
    hub_level = Column(Integer, default=1)
    inventory_for_others = Column(JSON)  # List[str]
    hub_fee_percentage = Column(Float, default=12.0)
    monthly_volume_usd = Column(Float, default=0.0)
    total_earnings_usd = Column(Float, default=0.0)
    supported_heroes = Column(JSON)  # List[str]
    compliance_level = Column(String, default="standard")
    insurance_coverage_usd = Column(Float, default=0.0)
    verified_at = Column(DateTime, nullable=True)


class ListingDB(Base):
    """Listing persistence"""
    __tablename__ = "listings"
    
    listing_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    host_id = Column(String, ForeignKey("users.user_id"))
    mode = Column(String)  # sell, rent, split, store
    price_usd = Column(Float)
    price_unit = Column(String)  # per_item, per_hour, per_minute, flat
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    delivery_modes = Column(JSON)  # List[str]
    risk_level = Column(String, default="low")
    proof_required = Column(Boolean, default=True)
    deposit_required = Column(Boolean, default=False)
    deposit_usd = Column(Float, nullable=True)
    visibility = Column(String, default="public")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Item/Space/Skill data stored as JSON for flexibility
    item_data = Column(JSON, nullable=True)
    space_data = Column(JSON, nullable=True)
    skill_data = Column(JSON, nullable=True)


class TransactionDB(Base):
    """Transaction persistence"""
    __tablename__ = "transactions"
    
    transaction_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String, ForeignKey("listings.listing_id"))
    requester_id = Column(String, ForeignKey("users.user_id"))
    host_id = Column(String, ForeignKey("users.user_id"))
    mode = Column(String)
    delivery_mode = Column(String)
    total_price_usd = Column(Float)
    delivery_fee_usd = Column(Float, default=0.0)
    platform_fee_usd = Column(Float, default=0.0)
    host_payout_usd = Column(Float)
    deposit_usd = Column(Float, nullable=True)
    deposit_returned_usd = Column(Float, nullable=True)
    proof_required = Column(Boolean, default=True)
    proof_photo_url = Column(String, nullable=True)
    proof_signature = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)


class SplitOrderDB(Base):
    """SplitOrder persistence"""
    __tablename__ = "split_orders"
    
    split_order_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    initiator_id = Column(String, ForeignKey("users.user_id"))
    item_name = Column(String)
    item_url = Column(String, nullable=True)
    total_quantity = Column(Integer)
    total_cost_usd = Column(Float)
    unit_type = Column(String)
    units_available = Column(Integer)
    units_reserved = Column(Integer, default=0)
    price_per_unit_usd = Column(Float)
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    fulfillment_location = Column(String)
    fulfillment_house_id = Column(String, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class SplitReservationDB(Base):
    """SplitReservation persistence"""
    __tablename__ = "split_reservations"
    
    reservation_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    split_order_id = Column(String, ForeignKey("split_orders.split_order_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    quantity = Column(Integer)
    cost_usd = Column(Float)
    pickup_window_start = Column(String)
    pickup_window_end = Column(String)
    status = Column(String, default="reserved")
    created_at = Column(DateTime, default=datetime.utcnow)


class SplitPulseDB(Base):
    """SplitPulse persistence"""
    __tablename__ = "split_pulses"
    
    pulse_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_name = Column(String)
    item_url = Column(String, nullable=True)
    interest_count = Column(Integer, default=0)
    anonymous_users = Column(Boolean, default=True)
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    radius_miles = Column(Float, default=2.0)
    urgency = Column(String, default="normal")
    category = Column(String, nullable=True)
    suggested_split_quantity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class IntentDB(Base):
    """Intent persistence (Intent-as-Inventory)"""
    __tablename__ = "intents"
    
    intent_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"))
    intent_type = Column(String)  # supply_intent, demand_intent, permission, boundary, preference
    content = Column(Text)
    category = Column(String, nullable=True)
    conditions = Column(JSON)  # List[str]
    availability_windows = Column(JSON)  # List[dict]
    location_latitude = Column(Float, nullable=True)
    location_longitude = Column(Float, nullable=True)
    radius_miles = Column(Float, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DemandSignalDB(Base):
    """Demand signal persistence"""
    __tablename__ = "demand_signals"
    
    signal_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    item_name = Column(String)
    category = Column(String)
    request_count = Column(Integer, default=0)
    failed_match_count = Column(Integer, default=0)
    average_budget_usd = Column(Float)
    urgency_distribution = Column(JSON)  # dict
    time_of_day_distribution = Column(JSON)  # dict
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    radius_miles = Column(Float, default=2.0)
    trend_score = Column(Float, default=0.0)
    suggested_action = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
