import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Create a default system user for pre-populated animations
system_user = {
    "id": "system-user-001",
    "username": "CSSMaster",
    "email": "admin@cssanimations.com",
    "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5BI2vQjIWy0lW",  # hashed "admin123"
    "bio": "Official CSS Animation Hub - Curated collection of professional animations",
    "profile_picture": "",
    "joined_date": datetime.now(timezone.utc).isoformat(),
    "followers": [],
    "following": []
}

animations = [
    # FADE Category
    {
        "id": str(uuid.uuid4()),
        "title": "Fade In",
        "css_code": """@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

.animated-element {
  animation: fadeIn 1.5s ease-in;
}""",
        "category": "Fade",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Fade Out",
        "css_code": """@keyframes fadeOut {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

.animated-element {
  animation: fadeOut 1.5s ease-out;
}""",
        "category": "Fade",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Fade Slide Up",
        "css_code": """@keyframes fadeSlideUp {
  0% { 
    opacity: 0;
    transform: translateY(30px);
  }
  100% { 
    opacity: 1;
    transform: translateY(0);
  }
}

.animated-element {
  animation: fadeSlideUp 1s ease-out;
}""",
        "category": "Fade",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Fade Zoom",
        "css_code": """@keyframes fadeZoom {
  0% { 
    opacity: 0;
    transform: scale(0.8);
  }
  100% { 
    opacity: 1;
    transform: scale(1);
  }
}

.animated-element {
  animation: fadeZoom 0.8s ease-out;
}""",
        "category": "Fade",
        "shape_type": "cube",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    
    # SLIDE Category
    {
        "id": str(uuid.uuid4()),
        "title": "Slide In Left",
        "css_code": """@keyframes slideInLeft {
  0% { 
    transform: translateX(-100%);
    opacity: 0;
  }
  100% { 
    transform: translateX(0);
    opacity: 1;
  }
}

.animated-element {
  animation: slideInLeft 0.8s ease-out;
}""",
        "category": "Slide",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Slide In Right",
        "css_code": """@keyframes slideInRight {
  0% { 
    transform: translateX(100%);
    opacity: 0;
  }
  100% { 
    transform: translateX(0);
    opacity: 1;
  }
}

.animated-element {
  animation: slideInRight 0.8s ease-out;
}""",
        "category": "Slide",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Slide Down",
        "css_code": """@keyframes slideDown {
  0% { 
    transform: translateY(-100%);
    opacity: 0;
  }
  100% { 
    transform: translateY(0);
    opacity: 1;
  }
}

.animated-element {
  animation: slideDown 0.7s ease-out;
}""",
        "category": "Slide",
        "shape_type": "cube",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Slide Up",
        "css_code": """@keyframes slideUp {
  0% { 
    transform: translateY(100%);
    opacity: 0;
  }
  100% { 
    transform: translateY(0);
    opacity: 1;
  }
}

.animated-element {
  animation: slideUp 0.7s ease-out;
}""",
        "category": "Slide",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    
    # ROTATE Category
    {
        "id": str(uuid.uuid4()),
        "title": "Spin Clockwise",
        "css_code": """@keyframes spinClockwise {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animated-element {
  animation: spinClockwise 2s linear infinite;
}""",
        "category": "Rotate",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Flip Horizontal",
        "css_code": """@keyframes flipHorizontal {
  0% { transform: rotateY(0deg); }
  100% { transform: rotateY(360deg); }
}

.animated-element {
  animation: flipHorizontal 1.5s ease-in-out infinite;
}""",
        "category": "Rotate",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Flip Vertical",
        "css_code": """@keyframes flipVertical {
  0% { transform: rotateX(0deg); }
  100% { transform: rotateX(360deg); }
}

.animated-element {
  animation: flipVertical 1.5s ease-in-out infinite;
}""",
        "category": "Rotate",
        "shape_type": "cube",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Rotate 3D",
        "css_code": """@keyframes rotate3D {
  0% { transform: rotate3d(1, 1, 1, 0deg); }
  100% { transform: rotate3d(1, 1, 1, 360deg); }
}

.animated-element {
  animation: rotate3D 3s linear infinite;
  transform-style: preserve-3d;
}""",
        "category": "Rotate",
        "shape_type": "cube",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Wobble Rotate",
        "css_code": """@keyframes wobbleRotate {
  0% { transform: rotate(0deg); }
  25% { transform: rotate(15deg); }
  75% { transform: rotate(-15deg); }
  100% { transform: rotate(0deg); }
}

.animated-element {
  animation: wobbleRotate 1s ease-in-out infinite;
}""",
        "category": "Rotate",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    
    # BOUNCE Category
    {
        "id": str(uuid.uuid4()),
        "title": "Bounce",
        "css_code": """@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
}

.animated-element {
  animation: bounce 2s ease infinite;
}""",
        "category": "Bounce",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Rubber Band",
        "css_code": """@keyframes rubberBand {
  0% { transform: scale(1); }
  30% { transform: scaleX(1.25) scaleY(0.75); }
  40% { transform: scaleX(0.75) scaleY(1.25); }
  50% { transform: scaleX(1.15) scaleY(0.85); }
  65% { transform: scaleX(0.95) scaleY(1.05); }
  75% { transform: scaleX(1.05) scaleY(0.95); }
  100% { transform: scale(1); }
}

.animated-element {
  animation: rubberBand 1.5s ease infinite;
}""",
        "category": "Bounce",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Shake",
        "css_code": """@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
  20%, 40%, 60%, 80% { transform: translateX(10px); }
}

.animated-element {
  animation: shake 1s ease infinite;
}""",
        "category": "Bounce",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Jello",
        "css_code": """@keyframes jello {
  0%, 100% { transform: skewX(0deg) skewY(0deg); }
  30% { transform: skewX(25deg) skewY(25deg); }
  40% { transform: skewX(-20deg) skewY(-20deg); }
  50% { transform: skewX(15deg) skewY(15deg); }
  65% { transform: skewX(-10deg) skewY(-10deg); }
  75% { transform: skewX(5deg) skewY(5deg); }
}

.animated-element {
  animation: jello 1.5s ease infinite;
}""",
        "category": "Bounce",
        "shape_type": "cube",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Swing",
        "css_code": """@keyframes swing {
  20% { transform: rotate(15deg); }
  40% { transform: rotate(-10deg); }
  60% { transform: rotate(5deg); }
  80% { transform: rotate(-5deg); }
  100% { transform: rotate(0deg); }
}

.animated-element {
  animation: swing 1.5s ease-in-out infinite;
  transform-origin: top center;
}""",
        "category": "Bounce",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    
    # SCALE Category
    {
        "id": str(uuid.uuid4()),
        "title": "Zoom In",
        "css_code": """@keyframes zoomIn {
  0% { 
    transform: scale(0);
    opacity: 0;
  }
  100% { 
    transform: scale(1);
    opacity: 1;
  }
}

.animated-element {
  animation: zoomIn 0.8s ease-out;
}""",
        "category": "Scale",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Zoom Out",
        "css_code": """@keyframes zoomOut {
  0% { 
    transform: scale(1);
    opacity: 1;
  }
  100% { 
    transform: scale(0);
    opacity: 0;
  }
}

.animated-element {
  animation: zoomOut 0.8s ease-in;
}""",
        "category": "Scale",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Pulse",
        "css_code": """@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.animated-element {
  animation: pulse 1.5s ease-in-out infinite;
}""",
        "category": "Scale",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Heartbeat",
        "css_code": """@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  10% { transform: scale(1.2); }
  20% { transform: scale(1); }
  30% { transform: scale(1.2); }
  40% { transform: scale(1); }
}

.animated-element {
  animation: heartbeat 1.5s ease-in-out infinite;
}""",
        "category": "Scale",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Expand Vertical",
        "css_code": """@keyframes expandVertical {
  0% { transform: scaleY(0); }
  100% { transform: scaleY(1); }
}

.animated-element {
  animation: expandVertical 0.8s ease-out;
}""",
        "category": "Scale",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    
    # SPECIAL EFFECTS Category
    {
        "id": str(uuid.uuid4()),
        "title": "Glow Pulse",
        "css_code": """@keyframes glowPulse {
  0%, 100% {
    box-shadow: 0 0 5px rgba(100, 200, 255, 0.5);
  }
  50% {
    box-shadow: 0 0 30px rgba(100, 200, 255, 1),
                0 0 50px rgba(100, 200, 255, 0.8);
  }
}

.animated-element {
  animation: glowPulse 2s ease-in-out infinite;
}""",
        "category": "Special Effects",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Shimmer",
        "css_code": """@keyframes shimmer {
  0% {
    background-position: -200% center;
  }
  100% {
    background-position: 200% center;
  }
}

.animated-element {
  background: linear-gradient(
    90deg,
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.8) 50%,
    rgba(255,255,255,0) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s ease-in-out infinite;
}""",
        "category": "Special Effects",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Wave",
        "css_code": """@keyframes wave {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(20deg);
  }
  75% {
    transform: rotate(-20deg);
  }
}

.animated-element {
  animation: wave 1s ease-in-out infinite;
  transform-origin: bottom center;
}""",
        "category": "Special Effects",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Flash",
        "css_code": """@keyframes flash {
  0%, 50%, 100% {
    opacity: 1;
  }
  25%, 75% {
    opacity: 0;
  }
}

.animated-element {
  animation: flash 2s ease-in-out infinite;
}""",
        "category": "Special Effects",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Color Change",
        "css_code": """@keyframes colorChange {
  0% { filter: hue-rotate(0deg); }
  100% { filter: hue-rotate(360deg); }
}

.animated-element {
  animation: colorChange 5s linear infinite;
}""",
        "category": "Special Effects",
        "shape_type": "cube",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Float",
        "css_code": """@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animated-element {
  animation: float 3s ease-in-out infinite;
}""",
        "category": "Special Effects",
        "shape_type": "circle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Blur In",
        "css_code": """@keyframes blurIn {
  0% {
    filter: blur(20px);
    opacity: 0;
  }
  100% {
    filter: blur(0px);
    opacity: 1;
  }
}

.animated-element {
  animation: blurIn 1.5s ease-out;
}""",
        "category": "Special Effects",
        "shape_type": "square",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Neon Glow",
        "css_code": """@keyframes neonGlow {
  0%, 100% {
    box-shadow: 0 0 10px #00ff00,
                0 0 20px #00ff00,
                0 0 30px #00ff00;
  }
  50% {
    box-shadow: 0 0 20px #00ff00,
                0 0 40px #00ff00,
                0 0 60px #00ff00,
                0 0 80px #00ff00;
  }
}

.animated-element {
  animation: neonGlow 1.5s ease-in-out infinite;
}""",
        "category": "Special Effects",
        "shape_type": "rectangle",
        "user_id": "system-user-001",
        "username": "CSSMaster",
        "user_profile_picture": "",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "likes": [],
        "likes_count": 0
    }
]

async def seed_database():
    print("Starting database seeding...")
    
    # Check if system user already exists
    existing_user = await db.users.find_one({"id": system_user["id"]})
    if not existing_user:
        await db.users.insert_one(system_user)
        print(f"✓ Created system user: {system_user['username']}")
    else:
        print(f"✓ System user already exists: {system_user['username']}")
    
    # Check if animations already exist
    existing_animations = await db.animations.count_documents({})
    if existing_animations > 0:
        print(f"✓ Database already has {existing_animations} animations")
        response = input("Do you want to clear and reseed? (yes/no): ")
        if response.lower() == 'yes':
            await db.animations.delete_many({})
            print("✓ Cleared existing animations")
        else:
            print("Seeding cancelled.")
            return
    
    # Insert animations
    await db.animations.insert_many(animations)
    print(f"✓ Inserted {len(animations)} animations")
    
    print("\n" + "="*50)
    print("✓ Database seeding completed successfully!")
    print("="*50)
    print(f"\nTotal animations: {len(animations)}")
    print(f"Categories: Fade, Slide, Rotate, Bounce, Scale, Special Effects")
    print(f"\nSystem User Credentials:")
    print(f"  Username: {system_user['username']}")
    print(f"  Password: admin123")

if __name__ == "__main__":
    asyncio.run(seed_database())
    client.close()
