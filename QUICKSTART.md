# 🚀 Quick Start Guide

## Local Development (Easy Way)

### 1. Install Dependencies
```bash
./setup.sh
```

### 2. Start the Server
```bash
./start.sh
```

### 3. Open Frontend
Open `index.html` in your browser or run:
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

## Manual Setup

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5001`

---

## Deploy to Vercel

### One-Command Deploy
```bash
npm i -g vercel
vercel
```

Follow the prompts:
- Project name: webexo (or your choice)
- Directory: ./
- Framework: Other
- Build command: (leave empty)
- Output directory: (leave empty)

That's it! Your API will be live at `https://your-project.vercel.app/api/predict`

### Update Frontend
After deploying, the frontend will automatically use the Vercel endpoint when not on localhost.

---

## Usage

1. **Sign Up/Login**: Use Firebase authentication
2. **Upload CSV**: Click "Upload CSV" and select your exoplanet data
3. **View Results**: See predictions, confidence scores, and orbital metrics
4. **AI Assistant**: Ask questions about the predictions

---

## API Testing

### Local Test
```bash
curl -X POST http://127.0.0.1:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "FLUX.1,FLUX.2\n0.98,0.97\n"}'
```

### Health Check
```bash
curl http://127.0.0.1:5001/health
```

---

## Troubleshooting

### Port Already in Use
```bash
lsof -ti:5001 | xargs kill -9
```

### Model Not Loading
Ensure these files exist:
- `model_files/exoplanet_bilstm.h5`
- `model_files/scaler.pkl`
- `model_files/metadata.pkl`

### CORS Issues
- Frontend and backend must be running
- Check browser console for errors
- CORS is enabled in Flask with `Flask-Cors`

### Vercel Deployment Issues
- Increase memory: Set in `vercel.json` (currently 3GB)
- Check logs: `vercel logs`
- TensorFlow size: Using optimized version for serverless

---

## File Structure

```
webexo/
├── index.html           # Frontend UI
├── app.py              # Local Flask server
├── api/predict.py      # Vercel serverless function
├── model_files/        # ML model files
├── requirements.txt    # Python packages
├── vercel.json        # Vercel config
├── setup.sh           # Setup script
├── start.sh           # Start script
└── test_api.py        # API test script
```

---

## Next Steps

1. ✅ Start local server: `./start.sh`
2. ✅ Test API: `python test_api.py`
3. ✅ Open `index.html` in browser
4. ✅ Upload sample data: `sample_data.csv`
5. 🚀 Deploy to Vercel: `vercel`

**You're all set! Happy exoplanet hunting! 🌌**

