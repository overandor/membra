"""Seed database with NYC spaces."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Space, AvailabilityWindow

DATABASE_URL = "sqlite:///./couchify.db"

SPACES_DATA = [
    ("Soho Loft", "desk", "SoHo", 2, 0.45, "https://images.unsplash.com/photo-1497366216548-37526070297c?w=400"),
    ("Brooklyn Nook", "couch", "Brooklyn Heights", 1, 0.35, "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400"),
    ("Midtown Phone Booth", "phone_booth", "Midtown", 1, 0.65, "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=400"),
    ("East Village Desk", "desk", "East Village", 1, 0.30, "https://images.unsplash.com/photo-1510074377623-8cf13fb86c08?w=400"),
    ("Chelsea Meeting Room", "meeting_room", "Chelsea", 4, 0.80, "https://images.unsplash.com/photo-1556761175-4b46a572b786?w=400"),
]

def main():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    host = User(id=uuid.uuid4(), email="host@couchify.dev", name="Demo Host", role="host")
    db.add(host)
    db.flush()

    for title, space_type, neighborhood, seats, price, image in SPACES_DATA:
        space = Space(
            id=uuid.uuid4(),
            host_id=host.id,
            title=title,
            space_type=space_type,
            neighborhood=neighborhood,
            capacity_seats=seats,
            price_per_minute=price,
            image_url=image,
            status="active"
        )
        db.add(space)
        db.flush()

        db.add(AvailabilityWindow(
            space_id=space.id,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=7),
            auto_accept=True
        ))

    db.commit()
    print("Database seeded with 5 spaces")

if __name__ == "__main__":
    main()
