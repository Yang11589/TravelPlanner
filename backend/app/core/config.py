import os

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/travel_planner"

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
