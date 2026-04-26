import pytest
from fastapi.testclient import TestClient


class TestAuthRegister:
    """Test cases for user registration"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["access_token"] is not None
        assert data["user_id"] is not None
        assert data["username"] == "testuser"
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        # First registration
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        # Second registration with same username
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "differentpass123"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        response = client.post(
            "/api/auth/register",
            json={"username": "testuser"}
        )
        
        assert response.status_code == 422  # Validation error


class TestAuthLogin:
    """Test cases for user login"""
    
    def test_login_success(self, client):
        """Test successful login"""
        # First register a user
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        # Then login
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["access_token"] is not None
        assert data["user_id"] is not None
        assert data["username"] == "testuser"
    
    def test_login_invalid_username(self, client):
        """Test login with non-existent username"""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "nonexistent",
                "password": "anypass123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, client):
        """Test login with wrong password"""
        # First register a user
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        # Try login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpass123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]
    
    def test_login_missing_fields(self, client):
        """Test login with missing required fields"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser"}
        )
        
        assert response.status_code == 422  # Validation error
