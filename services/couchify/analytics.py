"""Analytics and metrics tracking for Couchify."""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import User as DBUser, Space as DBSpace, Booking as DBBooking


def get_analytics(db: Session) -> Dict[str, Any]:
    """Get comprehensive analytics for the platform."""
    
    total_users = db.query(DBUser).count()
    total_spaces = db.query(DBSpace).filter(DBSpace.status == "active").count()
    total_bookings = db.query(DBBooking).count()
    
    total_revenue = db.query(func.sum(DBBooking.total)).scalar() or 0
    platform_fee = db.query(func.sum(DBBooking.platform_fee)).scalar() or 0
    host_payouts = total_revenue - platform_fee
    
    booking_status_counts = {}
    for status in ["pending", "confirmed", "checked_in", "completed", "cancelled"]:
        count = db.query(DBBooking).filter(DBBooking.status == status).count()
        booking_status_counts[status] = count
    
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_bookings = db.query(DBBooking).filter(DBBooking.created_at >= seven_days_ago).count()
    recent_revenue = db.query(func.sum(DBBooking.total)).filter(
        DBBooking.created_at >= seven_days_ago
    ).scalar() or 0
    
    top_spaces = db.query(
        DBSpace.title,
        DBSpace.neighborhood,
        func.count(DBBooking.id).label("booking_count"),
        func.sum(DBBooking.total).label("revenue")
    ).join(DBBooking).group_by(DBSpace.id).order_by(
        func.count(DBBooking.id).desc()
    ).limit(5).all()
    
    avg_duration = db.query(func.avg(DBBooking.duration_minutes)).scalar() or 0
    
    total_booked_minutes = db.query(func.sum(DBBooking.duration_minutes)).scalar() or 0
    total_available_minutes = total_spaces * 24 * 60
    occupancy_rate = (total_booked_minutes / total_available_minutes * 100) if total_available_minutes > 0 else 0
    
    return {
        "overview": {
            "total_users": total_users,
            "total_spaces": total_spaces,
            "total_bookings": total_bookings,
            "total_revenue": float(total_revenue),
            "platform_fee": float(platform_fee),
            "host_payouts": float(host_payouts),
        },
        "bookings": {
            "by_status": booking_status_counts,
            "last_7_days": recent_bookings,
            "last_7_days_revenue": float(recent_revenue),
            "average_duration_minutes": float(avg_duration),
        },
        "spaces": {
            "top_performing": [
                {
                    "title": space.title,
                    "neighborhood": space.neighborhood,
                    "booking_count": space.booking_count,
                    "revenue": float(space.revenue)
                }
                for space in top_spaces
            ],
            "occupancy_rate": round(occupancy_rate, 2),
        },
        "generated_at": datetime.utcnow().isoformat(),
    }


def get_host_analytics(host_id: str, db: Session) -> Dict[str, Any]:
    """Get analytics for a specific host."""
    host_uuid = host_id if isinstance(host_id, str) else str(host_id)
    spaces = db.query(DBSpace).filter(DBSpace.host_id == host_uuid).all()
    space_ids = [s.id for s in spaces]
    bookings = db.query(DBBooking).filter(DBBooking.space_id.in_(space_ids)).all()
    total_revenue = sum(b.total for b in bookings)
    total_bookings = len(bookings)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_bookings = [b for b in bookings if b.created_at >= thirty_days_ago]
    recent_revenue = sum(b.total for b in recent_bookings)
    space_performance = []
    for space in spaces:
        space_bookings = [b for b in bookings if b.space_id == space.id]
        space_revenue = sum(b.total for b in space_bookings)
        space_performance.append({
            "title": space.title,
            "bookings": len(space_bookings),
            "revenue": float(space_revenue),
            "status": space.status,
        })
    return {
        "host_id": host_uuid,
        "overview": {
            "total_spaces": len(spaces),
            "total_bookings": total_bookings,
            "total_revenue": float(total_revenue),
            "last_30_days_bookings": len(recent_bookings),
            "last_30_days_revenue": float(recent_revenue),
        },
        "space_performance": space_performance,
    }


def get_guest_analytics(guest_id: str, db: Session) -> Dict[str, Any]:
    """Get analytics for a specific guest."""
    guest_uuid = guest_id if isinstance(guest_id, str) else str(guest_id)
    bookings = db.query(DBBooking).filter(DBBooking.guest_id == guest_uuid).all()
    total_bookings = len(bookings)
    total_spent = sum(b.total for b in bookings)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_bookings = [b for b in bookings if b.created_at >= thirty_days_ago]
    neighborhood_counts = {}
    for booking in bookings:
        if booking.space:
            neighborhood = booking.space.neighborhood
            neighborhood_counts[neighborhood] = neighborhood_counts.get(neighborhood, 0) + 1
    favorite_neighborhoods = sorted(neighborhood_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    return {
        "guest_id": guest_uuid,
        "overview": {
            "total_bookings": total_bookings,
            "total_spent": float(total_spent),
            "last_30_days_bookings": len(recent_bookings),
        },
        "preferences": {
            "favorite_neighborhoods": [
                {"neighborhood": n, "count": c}
                for n, c in favorite_neighborhoods
            ],
        },
    }
