# 🚀 Quick Start Guide

## Local Development (Start Here!)

### 1. Install Dependencies
```bash
./setup.sh
```

### 2. Start the Server
```bash
./start.sh
```

### 3. Open Frontend
```bash
open index.html
```

### 4. Test (Optional)
In a new terminal:
```bash
source venv/bin/activate
python test_api.py
```

---

## 🌐 Deploy to Production

### The Problem
TensorFlow models are **too large** for Vercel serverless functions (250MB limit).

### The Solution
Split deployment:
- **Frontend** → Vercel (static hosting)
- **Backend** → Railway (ML-friendly, free tier)

### Quick Deploy (3 Steps)

#### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
gh repo create webexo --public --source=. --push
```

#### Step 2: Deploy Backend to Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select `webexo` repository
5. Copy your app URL: `https://webexo-production-xxxx.up.railway.app`

#### Step 3: Deploy Frontend to Vercel
```bash
vercel
```

Then update the frontend settings with your Railway URL!

---

## 📊 Full Deployment Guide

See **[DEPLOY.md](DEPLOY.md)** for detailed instructions including:
- Railway deployment (recommended)
- Render deployment (alternative)
- Heroku deployment
- CORS configuration
- Environment variables

---

## 🧪 Test the API

### Health Check
```bash
curl http://127.0.0.1:5001/health
```

### Test Prediction
```bash
python test_api.py
```

### Manual cURL Test
```bash
curl -X POST http://127.0.0.1:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "FLUX.1,FLUX.2\n0.98,0.97\n"}'
```

---

## 🎯 Architecture

```
User Browser
    ↓
Frontend (Vercel)
    ↓ API call
Backend (Railway) 
    ↓
TensorFlow Model
    ↓
Prediction Response
```

---

## 💡 Why This Setup?

### Vercel (Frontend)
✅ Free forever  
✅ Global CDN  
✅ Auto SSL  
✅ GitHub integration  
❌ Can't run TensorFlow (too large)

### Railway (Backend)
✅ Free 500 hours/month  
✅ ML-friendly (512MB RAM)  
✅ Auto-deploys from GitHub  
✅ Great for TensorFlow  
✅ Simple setup

**Total Cost: $0/month** 🎉

---

## 🐛 Common Issues

### Port Already in Use
```bash
lsof -ti:5001 | xargs kill -9
./start.sh
```

### Model Not Loading
Check that these files exist:
```
model_files/
├── exoplanet_bilstm.h5
├── scaler.pkl
└── metadata.pkl
```

### CORS Errors in Production
Make sure `Flask-Cors` is installed:
```bash
pip install Flask-Cors
```

### Backend URL Not Working
In the frontend settings, make sure you enter the **full URL**:
```
https://your-app.up.railway.app/api/predict
```

---

## 📁 Project Structure

```
webexo/
├── index.html          # Frontend (deploy to Vercel)
├── app.py             # Backend (deploy to Railway)
├── model_files/       # ML model files
├── requirements.txt   # Python dependencies
├── Procfile          # Railway/Heroku config
├── runtime.txt       # Python version
├── vercel.json       # Vercel config (static only)
└── DEPLOY.md         # Full deployment guide
```

---

## ✅ Next Steps

1. **Local first**: Get it working on your machine
   ```bash
   ./start.sh
   open index.html
   ```

2. **Upload test data**: Use `sample_data.csv`

3. **Deploy when ready**: Follow [DEPLOY.md](DEPLOY.md)

**Happy exoplanet hunting! 🌌🪐**
