from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""
    joined_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    followers: List[str] = []
    following: List[str] = []

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""
    joined_date: datetime
    followers_count: int
    following_count: int
    animations_count: int

class Animation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    css_code: str
    category: str
    shape_type: str
    user_id: str
    username: str
    user_profile_picture: Optional[str] = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    likes: List[str] = []
    likes_count: int = 0

class AnimationCreate(BaseModel):
    title: str
    css_code: str
    category: str
    shape_type: str

class TokenResponse(BaseModel):
    token: str
    user: User

# Helper functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id: str) -> str:
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Auth Routes
@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_input: UserCreate):
    # Check if username exists
    existing_user = await db.users.find_one({"username": user_input.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    existing_email = await db.users.find_one({"email": user_input.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    user_dict = user_input.model_dump(exclude={"password"})
    user = User(**user_dict)
    
    doc = user.model_dump()
    doc['password'] = hash_password(user_input.password)
    doc['joined_date'] = doc['joined_date'].isoformat()
    
    await db.users.insert_one(doc)
    
    token = create_token(user.id)
    return TokenResponse(token=token, user=user)

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user_doc = await db.users.find_one({"username": credentials.username})
    if not user_doc or not verify_password(credentials.password, user_doc['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if isinstance(user_doc['joined_date'], str):
        user_doc['joined_date'] = datetime.fromisoformat(user_doc['joined_date'])
    
    user = User(**user_doc)
    token = create_token(user.id)
    return TokenResponse(token=token, user=user)

@api_router.get("/auth/me", response_model=User)
async def get_current_user(token: str):
    user_id = decode_token(token)
    user_doc = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    if isinstance(user_doc['joined_date'], str):
        user_doc['joined_date'] = datetime.fromisoformat(user_doc['joined_date'])
    
    return User(**user_doc)

# User Routes
@api_router.get("/users/search")
async def search_users(q: str):
    users = await db.users.find(
        {"username": {"$regex": q, "$options": "i"}},
        {"_id": 0, "password": 0}
    ).limit(20).to_list(20)
    
    for user in users:
        if isinstance(user['joined_date'], str):
            user['joined_date'] = datetime.fromisoformat(user['joined_date'])
    
    return users

@api_router.get("/users/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    user_doc = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    if isinstance(user_doc['joined_date'], str):
        user_doc['joined_date'] = datetime.fromisoformat(user_doc['joined_date'])
    
    animations_count = await db.animations.count_documents({"user_id": user_id})
    
    return UserProfile(
        id=user_doc['id'],
        username=user_doc['username'],
        email=user_doc['email'],
        bio=user_doc.get('bio', ''),
        profile_picture=user_doc.get('profile_picture', ''),
        joined_date=user_doc['joined_date'],
        followers_count=len(user_doc.get('followers', [])),
        following_count=len(user_doc.get('following', [])),
        animations_count=animations_count
    )

@api_router.post("/users/{user_id}/follow")
async def follow_user(user_id: str, token: str):
    current_user_id = decode_token(token)
    
    if current_user_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    # Add to current user's following
    await db.users.update_one(
        {"id": current_user_id},
        {"$addToSet": {"following": user_id}}
    )
    
    # Add to target user's followers
    await db.users.update_one(
        {"id": user_id},
        {"$addToSet": {"followers": current_user_id}}
    )
    
    return {"success": True}

@api_router.post("/users/{user_id}/unfollow")
async def unfollow_user(user_id: str, token: str):
    current_user_id = decode_token(token)
    
    await db.users.update_one(
        {"id": current_user_id},
        {"$pull": {"following": user_id}}
    )
    
    await db.users.update_one(
        {"id": user_id},
        {"$pull": {"followers": current_user_id}}
    )
    
    return {"success": True}

@api_router.get("/users/{user_id}/animations", response_model=List[Animation])
async def get_user_animations(user_id: str):
    animations = await db.animations.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("created_at", -1).to_list(1000)
    
    for anim in animations:
        if isinstance(anim['created_at'], str):
            anim['created_at'] = datetime.fromisoformat(anim['created_at'])
        anim['likes_count'] = len(anim.get('likes', []))
    
    return animations

# Animation Routes
@api_router.get("/animations", response_model=List[Animation])
async def get_all_animations(limit: int = 50, skip: int = 0):
    animations = await db.animations.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    for anim in animations:
        if isinstance(anim['created_at'], str):
            anim['created_at'] = datetime.fromisoformat(anim['created_at'])
        anim['likes_count'] = len(anim.get('likes', []))
    
    return animations

@api_router.get("/animations/following", response_model=List[Animation])
async def get_following_animations(token: str, limit: int = 50, skip: int = 0):
    user_id = decode_token(token)
    user_doc = await db.users.find_one({"id": user_id})
    
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    following_ids = user_doc.get('following', [])
    
    animations = await db.animations.find(
        {"user_id": {"$in": following_ids}},
        {"_id": 0}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    for anim in animations:
        if isinstance(anim['created_at'], str):
            anim['created_at'] = datetime.fromisoformat(anim['created_at'])
        anim['likes_count'] = len(anim.get('likes', []))
    
    return animations

@api_router.post("/animations", response_model=Animation)
async def create_animation(animation_input: AnimationCreate, token: str):
    user_id = decode_token(token)
    user_doc = await db.users.find_one({"id": user_id})
    
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    animation_dict = animation_input.model_dump()
    animation_dict['user_id'] = user_id
    animation_dict['username'] = user_doc['username']
    animation_dict['user_profile_picture'] = user_doc.get('profile_picture', '')
    
    animation = Animation(**animation_dict)
    
    doc = animation.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.animations.insert_one(doc)
    
    return animation

@api_router.get("/animations/{animation_id}", response_model=Animation)
async def get_animation(animation_id: str):
    animation_doc = await db.animations.find_one({"id": animation_id}, {"_id": 0})
    if not animation_doc:
        raise HTTPException(status_code=404, detail="Animation not found")
    
    if isinstance(animation_doc['created_at'], str):
        animation_doc['created_at'] = datetime.fromisoformat(animation_doc['created_at'])
    
    animation_doc['likes_count'] = len(animation_doc.get('likes', []))
    
    return Animation(**animation_doc)

@api_router.post("/animations/{animation_id}/like")
async def like_animation(animation_id: str, token: str):
    user_id = decode_token(token)
    
    animation_doc = await db.animations.find_one({"id": animation_id})
    if not animation_doc:
        raise HTTPException(status_code=404, detail="Animation not found")
    
    likes = animation_doc.get('likes', [])
    
    if user_id in likes:
        # Unlike
        await db.animations.update_one(
            {"id": animation_id},
            {"$pull": {"likes": user_id}}
        )
        return {"liked": False, "likes_count": len(likes) - 1}
    else:
        # Like
        await db.animations.update_one(
            {"id": animation_id},
            {"$addToSet": {"likes": user_id}}
        )
        return {"liked": True, "likes_count": len(likes) + 1}

@api_router.get("/animations/categories/list")
async def get_categories():
    return {
        "categories": [
            "Fade",
            "Slide",
            "Rotate",
            "Bounce",
            "Scale",
            "Special Effects"
        ]
    }

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
