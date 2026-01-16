# TravelPlanner

.venv\Scripts\activate.bat

uvicorn app.main:app --reload

netstat -ano | findstr :8000
taskkill /PID 12296 /F


