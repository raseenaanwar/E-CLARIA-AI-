# # app/main.py
# from fastapi import FastAPI
# from app.routes import auth, profile, strategy
# from app import models, database

# models.Base.metadata.create_all(bind=database.engine)

# app = FastAPI()

# app.include_router(auth.router, prefix="/api")
# app.include_router(profile.router, prefix="/api")
# app.include_router(strategy.router, prefix="/api")
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, profile, strategy
from app import models, database
from app.routes import outreach
from app.routes import community

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(strategy.router, prefix="/api")
app.include_router(outreach.router,prefix="/api")
app.include_router(community.router,prefix="/api")
