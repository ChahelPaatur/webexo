# 🚀 Deployment Guide

## Why Split Deployment?

TensorFlow models are **too large** for Vercel serverless functions. The solution:
- **Frontend** → Vercel (free, fast CDN)
- **Backend** → Railway/Render (free, ML-friendly)

---

## 📦 Deploy Backend to Railway (Recommended)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your `webexo` repository
5. Railway auto-detects Python and deploys!
6. Get your URL: `https://your-app.up.railway.app`

### Step 3: Update Frontend
In `index.html`, update line 150:
```javascript
const ML_MODEL_API = 'https://your-app.up.railway.app';
```

---

## 🌐 Deploy Frontend to Vercel

```bash
vercel
```

That's it! Your frontend is live at `https://your-project.vercel.app`

---

## 🎯 Alternative: Deploy Backend to Render

### Option 1: Render (Free Tier)
1. Go to [render.com](https://render.com)
2. Create **New Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Get URL: `https://your-app.onrender.com`

---

## 🏠 Local Development (No Deployment)

Just want to run locally? No problem!

```bash
# Terminal 1: Start backend
./start.sh

# Terminal 2: Start frontend
python -m http.server 8000
```

Visit `http://localhost:8000`

---

## 🔧 Update API Endpoint

Your frontend auto-detects the environment:
- **Local**: Uses `http://127.0.0.1:5001`
- **Production**: Uses `/api/predict` or custom endpoint

To set a custom endpoint:
1. Open your deployed frontend
2. Click **"Settings"**
3. Enter your Railway/Render URL: `https://your-app.up.railway.app/api/predict`

---

## ✅ Recommended Setup

```
Frontend (Vercel)     →  Backend (Railway)  →  ML Model
free, fast CDN           free, 512MB RAM       TensorFlow BiLSTM
```

**Total Cost: $0/month** 🎉

---

## 🐛 Troubleshooting

### Backend takes long to respond?
- Railway/Render free tier spins down after inactivity
- First request takes 30-60s (cold start)
- Subsequent requests are fast

### CORS errors?
- Make sure Flask-CORS is in requirements.txt
- Check that backend URL is correct in frontend

### Model too large?
- Railway free tier: 512MB RAM (should work)
- Render free tier: 512MB RAM (should work)
- If needed, upgrade to paid tier for 2GB+ RAM

---

## 💡 Pro Tips

1. **Railway is easier** - auto-detects everything
2. **Keep model files in repo** - they'll be deployed automatically
3. **Use environment variables** - for API keys and secrets
4. **Monitor logs** - Railway/Render both have great log viewers

---

## 📊 Deployment Checklist

- [x] Create `Procfile` and `runtime.txt`
- [x] Update `app.py` to use PORT env variable
- [x] Push to GitHub
- [ ] Deploy backend to Railway
- [ ] Get backend URL
- [ ] Update frontend with backend URL
- [ ] Deploy frontend to Vercel
- [ ] Test end-to-end

**You're ready to deploy! 🚀**

