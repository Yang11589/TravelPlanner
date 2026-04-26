import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db.deps import get_db
from app.db.base import Base
from unittest.mock import patch, MagicMock
from app.schemas.plan import Plan
from app.schemas.place import Place
from app.schemas.trip import TripResponse
import sys
import os

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def mock_generate_plan(city: str, days: int) -> TripResponse:
    """Mock function to generate test plans without calling Google API."""
    places_per_day = [
        [
            Place(name="Attraction 1", type="attraction"),
            Place(name="Restaurant 1", type="food")
        ],
        [
            Place(name="Attraction 2", type="attraction"),
            Place(name="Restaurant 2", type="food")
        ],
        [
            Place(name="Attraction 3", type="attraction"),
            Place(name="Restaurant 3", type="food")
        ],
        [
            Place(name="Attraction 4", type="attraction"),
            Place(name="Restaurant 4", type="food")
        ],
    ]
    
    itinerary = []
    for i in range(days):
        places = places_per_day[i % len(places_per_day)]
        plan = Plan(day=i + 1, places=places)
        itinerary.append(plan)
    
    return TripResponse(
        city=city,
        days=days,
        itinerary=itinerary,
        user_id=None,
        is_saved=False
    )


@pytest.fixture(scope="function", autouse=True)
def mock_api_calls():
    """Automatically mock all Google API calls for all tests."""
    with patch("app.api.planner.generate_plan", side_effect=mock_generate_plan):
        yield


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with override get_db."""
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
