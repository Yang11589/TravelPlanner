import pytest
from fastapi.testclient import TestClient


class TestGetTrips:
    """Test cases for retrieving trips"""
    
    def test_get_trips_requires_authentication(self, client):
        """Test that getting trips requires authentication"""
        response = client.get("/api/trips")
        
        assert response.status_code == 403  # Forbidden without auth
    
    def test_get_trips_empty_list(self, client):
        """Test getting trips when no trips exist"""
        # Register and login user
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = register_response.json()["access_token"]
        
        # Get trips
        response = client.get(
            "/api/trips",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
    
    def test_get_trips_with_saved_plans(self, client):
        """Test getting trips after saving some plans"""
        # Register and login user
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = register_response.json()["access_token"]
        user_id = register_response.json()["user_id"]
        
        # Generate and save a plan
        plan_response = client.post(
            "/api/plan",
            json={
                "city": "London",
                "days": 3
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert plan_response.status_code == 200
        
        # Generate and save another plan
        plan_response2 = client.post(
            "/api/plan",
            json={
                "city": "Paris",
                "days": 2
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert plan_response2.status_code == 200
        
        # Get trips
        response = client.get(
            "/api/trips",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2
        
        # Verify trips are from the same user
        for trip in data["items"]:
            assert trip["user_id"] == user_id
            assert trip["is_saved"] is True
    
    def test_get_trips_pagination_limit(self, client):
        """Test pagination with limit parameter"""
        # Register and login user
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = register_response.json()["access_token"]
        
        # Generate 3 plans
        for i in range(3):
            client.post(
                "/api/plan",
                json={
                    "city": f"City{i}",
                    "days": 2 + i
                },
                headers={"Authorization": f"Bearer {token}"}
            )
        
        # Get trips with limit=2
        response = client.get(
            "/api/trips?limit=2",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 2
    
    def test_get_trips_pagination_offset(self, client):
        """Test pagination with offset parameter"""
        # Register and login user
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = register_response.json()["access_token"]
        
        # Generate 3 plans
        for i in range(3):
            client.post(
                "/api/plan",
                json={
                    "city": f"City{i}",
                    "days": 2 + i
                },
                headers={"Authorization": f"Bearer {token}"}
            )
        
        # Get trips with offset=1
        response = client.get(
            "/api/trips?offset=1",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 2  # 3 - offset(1) = 2
    
    def test_get_trips_structure(self, client):
        """Test the structure of returned trips"""
        # Register and login user
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = register_response.json()["access_token"]
        
        # Generate and save a plan
        client.post(
            "/api/plan",
            json={
                "city": "London",
                "days": 2
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get trips
        response = client.get(
            "/api/trips",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        
        # Check trip structure
        for trip in data["items"]:
            assert "city" in trip
            assert "days" in trip
            assert "user_id" in trip
            assert "is_saved" in trip
            assert "itinerary" in trip
            assert trip["is_saved"] is True
    
    def test_get_trips_only_own_trips(self, client):
        """Test that users only see their own trips"""
        # Register first user
        user1_response = client.post(
            "/api/auth/register",
            json={
                "username": "user1",
                "password": "pass123"
            }
        )
        user1_token = user1_response.json()["access_token"]
        
        # Register second user
        user2_response = client.post(
            "/api/auth/register",
            json={
                "username": "user2",
                "password": "pass123"
            }
        )
        user2_token = user2_response.json()["access_token"]
        
        # User1 generates a plan
        client.post(
            "/api/plan",
            json={
                "city": "London",
                "days": 2
            },
            headers={"Authorization": f"Bearer {user1_token}"}
        )
        
        # User2 generates a plan
        client.post(
            "/api/plan",
            json={
                "city": "Paris",
                "days": 3
            },
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        
        # User1 gets their trips
        user1_trips = client.get(
            "/api/trips",
            headers={"Authorization": f"Bearer {user1_token}"}
        )
        assert user1_trips.json()["total"] == 1
        assert user1_trips.json()["items"][0]["city"] == "London"
        
        # User2 gets their trips
        user2_trips = client.get(
            "/api/trips",
            headers={"Authorization": f"Bearer {user2_token}"}
        )
        assert user2_trips.json()["total"] == 1
        assert user2_trips.json()["items"][0]["city"] == "Paris"
