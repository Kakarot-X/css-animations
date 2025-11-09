# Quick Start - Deploy in 15 Minutes

## Fastest Way: Render.com

### 1. MongoDB (5 min)
```
1. Go to mongodb.com/cloud/atlas
2. Sign up → Create FREE cluster
3. Create user & password
4. Allow all IPs (0.0.0.0/0)
5. Get connection string
```

### 2. Push to GitHub (2 min)
```bash
git init
git add .
git commit -m "Deploy CSS Animation Platform"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### 3. Deploy Backend (4 min)
```
1. render.com → New Web Service
2. Connect GitHub repo
3. Settings:
   - Build: cd backend && pip install -r requirements.txt
   - Start: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
4. Environment:
   - MONGO_URL = your MongoDB string
   - DB_NAME = css_animation_platform
   - SECRET_KEY = any-random-string
   - CORS_ORIGINS = *
5. Create → Copy backend URL
```

### 4. Seed Database (1 min)
```
1. Backend dashboard → Shell tab
2. Run: cd backend && python seed_animations.py
```

### 5. Deploy Frontend (3 min)
```
1. render.com → New Static Site
2. Same GitHub repo
3. Settings:
   - Build: cd frontend && yarn install && yarn build
   - Publish: frontend/build
4. Environment:
   - REACT_APP_BACKEND_URL = your backend URL
5. Create → Get frontend URL
```

### 6. Update CORS (1 min)
```
1. Backend → Environment
2. CORS_ORIGINS = your frontend URL
3. Save
```

## Done! 🎉
Your app is live at your frontend URL

**Login Credentials:**
- Username: CSSMaster
- Password: admin123

**Or register a new account!**
