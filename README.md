# ExoML - Exoplanet Detection Platform

NASA-grade exoplanet detection using BiLSTM machine learning model with a modern web interface.

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Flask Backend**
```bash
python app.py
```
The server will start on `http://127.0.0.1:5001`

3. **Open the Frontend**
Open `index.html` in your browser, or use a local server:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`

### Usage

1. Sign up or log in with Firebase authentication
2. Upload a CSV file containing transit photometry data
3. The ML model will analyze the data and predict exoplanet presence
4. View confidence scores, planet type, and orbital metrics

## 📦 Deployment to Vercel

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Configure**
- The project is pre-configured with `vercel.json`
- Model files will be automatically included
- The API endpoint will be available at `/api/predict`

## 🧠 Model Information

- **Architecture**: Bidirectional LSTM (BiLSTM)
- **Framework**: TensorFlow/Keras
- **Input**: Time-series transit photometry data (CSV format)
- **Output**: Exoplanet detection probability with confidence score

## 📊 API Endpoints

### POST `/api/predict`
Predict exoplanet from CSV data

**Request:**
```json
{
  "data": "csv_string_content"
}
```

**Response:**
```json
{
  "isExoplanet": true,
  "confidence": 87.5,
  "planetType": "Hot Jupiter",
  "orbitalPeriod": 12.34,
  "temperature": 1500.0,
  "transitDepth": "0.0234"
}
```

### GET `/health`
Check server health status

## 🛠️ Tech Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Flask, Python 3.9+
- **ML**: TensorFlow, Keras, NumPy, Pandas
- **Authentication**: Firebase Auth
- **Database**: Firebase Firestore
- **Deployment**: Vercel (Serverless)

## 📁 Project Structure

```
webexo/
├── index.html              # Frontend UI
├── app.py                  # Local Flask server
├── api/
│   └── predict.py         # Vercel serverless function
├── model_files/
│   ├── exoplanet_bilstm.h5  # Trained model
│   ├── scaler.pkl           # Data scaler
│   └── metadata.pkl         # Model metadata
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
└── README.md              # This file
```

## 🔒 Environment Variables

For production, consider adding:
- `FIREBASE_API_KEY`
- Model configuration parameters

## 📝 Notes

- CSV files should contain numerical features only
- Missing values are automatically handled
- The model expects preprocessed time-series data
- Vercel deployment includes 3GB memory allocation for ML inference

## 🤝 Contributing

This is a NASA exoplanet detection system. Ensure any modifications maintain scientific accuracy.

## 📜 License

Educational and research purposes.

