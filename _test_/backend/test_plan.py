import pytest
from fastapi.testclient import TestClient


class TestGeneratePlan:
    """Test cases for plan generation"""
    
    def test_generate_plan_without_login(self, client):
        """Test generating plan without authentication"""
        response = client.post(
            "/api/plan",
            json={
                "city": "London",
                "days": 3
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "London"
        assert data["days"] == 3
        assert data["is_saved"] is False
        assert data["user_id"] is None
        assert "itinerary" in data
        assert len(data["itinerary"]) == 3
    
    def test_generate_plan_with_login(self, client):
        """Test generating plan with authentication - plan is saved"""
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
        
        # Generate plan with authentication
        response = client.post(
            "/api/plan",
            json={
                "city": "Paris",
                "days": 2
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Paris"
        assert data["days"] == 2
        assert data["is_saved"] is True
        assert data["user_id"] == user_id
        assert "itinerary" in data
        assert len(data["itinerary"]) == 2
    
    def test_generate_plan_structure(self, client):
        """Test the structure of generated plan"""
        response = client.post(
            "/api/plan",
            json={
                "city": "Tokyo",
                "days": 4
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check main fields
        assert data["city"] == "Tokyo"
        assert data["days"] == 4
        assert len(data["itinerary"]) == 4
        
        # Check itinerary structure
        for i, day in enumerate(data["itinerary"]):
            assert day["day"] == i + 1
            assert "places" in day
            assert len(day["places"]) > 0
            
            # Check each place
            for place in day["places"]:
                assert "name" in place
                assert "type" in place
                assert place["type"] in ["food", "attraction", "lodging", "transportation"]
    
    def test_generate_plan_invalid_days(self, client):
        """Test generating plan with invalid number of days"""
        response = client.post(
            "/api/plan",
            json={
                "city": "Berlin",
                "days": "not_a_number"
            }
        )
        
        # Should fail validation
        assert response.status_code == 422
    
    def test_generate_plan_missing_city(self, client):
        """Test generating plan without city"""
        response = client.post(
            "/api/plan",
            json={
                "days": 3
            }
        )
        
        assert response.status_code == 422  # Validation error
