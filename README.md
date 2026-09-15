# TravelPlanner

TravelPlanner is an AI-powered travel planning application. It generates personalized itineraries based on a destination and trip duration, and allows users to modify their plans through a conversational interface.

## Features

- User registration and login
- AI-generated travel itineraries
- Conversational itinerary modification
- Save and view travel plans
- Delete saved trips
- JWT-based authentication

## Tech Stack

### Frontend

- React
- Vite
- React Router
- Tailwind CSS
- Axios

### Backend

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Google Gemini API
- JWT

## Requirements
- Python 3.10+
- Node.js 18+
- MySQL 8+
- Google Gemini API key

## Database Setup
The default database configuration is:

```bash
mysql+pymysql://root:root@localhost:3306/travel_planner
```

Create the database before starting the backend:

```bash
CREATE DATABASE travel_planner
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

## Backend Setup
Open a terminal in the project root and run:

```bash
cd backend
.venv\Scripts\activate.bat
pip install -r requirements.txt
```
Set the Google Gemini API key:

```bash
$env:GEMINI_API_KEY="your-gemini-api-key"
```

Optionally set a custom JWT secret:

```bash
$env:SECRET_KEY="your-secret-key"
```

Initialize the database tables:

```bash
python create_tables.py
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

## Frontend Setup

Open another terminal and run:

```bash
cd frontend
npm install
npm run dev
```

## Run Tests

Run the tests from the project root:

```bash
pytest
```