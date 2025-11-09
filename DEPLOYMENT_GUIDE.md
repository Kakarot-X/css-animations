# Deployment Guide - CSS Animation Platform

## Option 1: Render.com (Recommended - Free Tier Available)

### Prerequisites
- GitHub account
- Render account (sign up at https://render.com)
- MongoDB Atlas account (free at https://www.mongodb.com/cloud/atlas)

### Step 1: Setup MongoDB Atlas (Free)

1. Go to https://mongodb.com/cloud/atlas
2. Sign up/Login
3. Create a **FREE** cluster:
   - Click "Build a Database"
   - Choose **FREE** tier (M0)
   - Select region closest to you
   - Click "Create Cluster"

4. Create Database User:
   - Go to "Database Access"
   - Click "Add New Database User"
   - Create username & password (save these!)
   - Set privileges to "Read and write to any database"

5. Allow Network Access:
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Confirm

6. Get Connection String:
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Example: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`

---

### Step 2: Push Code to GitHub

1. Create a new GitHub repository
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - CSS Animation Platform"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/css-animations.git
   git push -u origin main
   ```

---

### Step 3: Deploy Backend on Render

1. Login to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `css-animations-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

5. Add Environment Variables:
   - `MONGO_URL` = Your MongoDB Atlas connection string
   - `DB_NAME` = `css_animation_platform`
   - `SECRET_KEY` = Any random string (e.g., `your-super-secret-key-change-me`)
   - `CORS_ORIGINS` = `*` (will update after frontend deployment)

6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy your backend URL (e.g., `https://css-animations-backend.onrender.com`)

---

### Step 4: Seed Database

1. After backend deploys, go to your backend service dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   cd backend
   python seed_animations.py
   ```
4. This creates the system user and 31 animations

---

### Step 5: Deploy Frontend on Render

1. Click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name**: `css-animations-frontend`
   - **Build Command**: `cd frontend && yarn install && yarn build`
   - **Publish Directory**: `frontend/build`

4. Add Environment Variable:
   - `REACT_APP_BACKEND_URL` = Your backend URL from Step 3

5. Click "Create Static Site"
6. Wait for deployment (5-10 minutes)
7. You'll get a frontend URL (e.g., `https://css-animations-frontend.onrender.com`)

---

### Step 6: Update CORS Settings

1. Go back to your backend service on Render
2. Click "Environment"
3. Update `CORS_ORIGINS` environment variable:
   - Change from `*` to your frontend URL
   - Example: `https://css-animations-frontend.onrender.com`
4. Save changes (service will redeploy)

---

### Step 7: Test Your Deployment

1. Visit your frontend URL
2. Register a new account
3. Login and test:
   - View animations
   - Search users (search for "CSSMaster")
   - Follow users
   - Create an animation
   - Like animations
   - Switch themes

---

## Option 2: Railway.app (Alternative)

### Advantages
- Even simpler than Render
- One-click MongoDB deployment
- Free $5 credit monthly

### Steps:

1. **Sign up**: https://railway.app
2. **New Project** → "Deploy from GitHub repo"
3. **Add MongoDB**: 
   - Click "+ New"
   - Select "Database" → "MongoDB"
   - Copy the `MONGO_URL` connection string
4. **Deploy Backend**:
   - Add service from repo
   - Root directory: `/backend`
   - Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (same as Render)
5. **Deploy Frontend**:
   - Add another service
   - Root directory: `/frontend`
   - Railway auto-detects React
   - Add `REACT_APP_BACKEND_URL`
6. **Generate domains** for both services
7. **Update CORS_ORIGINS** in backend with frontend URL

---

## Option 3: DigitalOcean App Platform

### Advantages
- $200 free credit for new users
- Professional infrastructure
- Easy scaling

### Steps:

1. Sign up: https://www.digitalocean.com/products/app-platform
2. Create App → From GitHub
3. Configure:
   - **Backend Component**: Python, port 8001
   - **Frontend Component**: React static site
   - **Database**: MongoDB (via MongoDB Atlas)
4. Add environment variables
5. Deploy

---

## Important Notes

### Free Tier Limitations:
- **Render Free**: Services sleep after 15 min inactivity (30s cold start)
- **Railway**: $5/month credit (usually enough for small apps)
- **MongoDB Atlas Free**: 512MB storage (plenty for this app)

### Custom Domain:
- Most platforms allow free custom domain setup
- Update CORS settings after adding custom domain

### Troubleshooting:

**Backend not responding:**
- Check environment variables are set correctly
- Check MongoDB connection string is correct
- View logs in platform dashboard

**Frontend can't connect to backend:**
- Verify `REACT_APP_BACKEND_URL` is correct
- Check CORS settings in backend
- Must include `https://` in URL

**Animations not showing:**
- Run seed script: `python backend/seed_animations.py`
- Check MongoDB connection

---

## Cost Breakdown (If Scaling):

**Free Forever:**
- MongoDB Atlas M0: FREE (512MB)
- Frontend hosting: FREE on most platforms
- Backend: FREE tier available (with limitations)

**Paid (If needed):**
- Render: $7/month for always-on backend
- Railway: Pay-as-you-go (~$5-10/month)
- DigitalOcean: Starting at $5/month

---

## Success Checklist ✓

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with password
- [ ] Network access allows all IPs
- [ ] Connection string copied
- [ ] Code pushed to GitHub
- [ ] Backend deployed and running
- [ ] Backend URL copied
- [ ] Database seeded with animations
- [ ] Frontend deployed
- [ ] CORS updated with frontend URL
- [ ] Can register and login
- [ ] Animations display correctly
- [ ] Search works
- [ ] Can follow users
- [ ] Can create animations

Your CSS Animation Platform is now live! 🎉
