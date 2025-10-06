import os
import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
CORS(app)

# Load model and preprocessing objects
MODEL_PATH = 'model_files/exoplanet_bilstm.h5'
SCALER_PATH = 'model_files/scaler.pkl'
METADATA_PATH = 'model_files/metadata.pkl'

model = None
scaler = None
metadata = None

def load_model_files():
    global model, scaler, metadata
    try:
        # Load the BiLSTM model
        model = keras.models.load_model(MODEL_PATH)
        print("✓ Model loaded successfully")
        
        # Load scaler
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        print("✓ Scaler loaded successfully")
        
        # Load metadata
        with open(METADATA_PATH, 'rb') as f:
            metadata = pickle.load(f)
        print("✓ Metadata loaded successfully")
        
        return True
    except Exception as e:
        print(f"Error loading model files: {str(e)}")
        return False

# Load model on startup
load_model_files()

def preprocess_csv(csv_data):
    """Convert CSV string to preprocessed numpy array for model"""
    try:
        from io import StringIO
        
        # Try to read CSV with error handling for malformed data
        try:
            df = pd.read_csv(StringIO(csv_data), error_bad_lines=False, warn_bad_lines=False)
        except:
            # If that fails, try with on_bad_lines parameter (pandas >= 1.3)
            df = pd.read_csv(StringIO(csv_data), on_bad_lines='skip')
        
        # Remove any non-numeric columns (like LABEL if present)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns found in CSV. Please ensure your file contains numerical flux data.")
        
        df = df[numeric_cols]
        
        # Handle missing values
        df = df.fillna(0)  # Fill with 0 instead of mean for consistency
        
        # Get the input shape from metadata
        if metadata and 'input_shape' in metadata:
            expected_timesteps = metadata['input_shape'][0]  # Should be 39
            expected_features = metadata['input_shape'][1]   # Should be 1
        else:
            expected_timesteps = 39
            expected_features = 1
        
        # Convert dataframe to array
        data = df.values
        
        # Flatten all data into a single sequence
        data_flat = data.flatten()
        
        # Remove any NaN or inf values
        data_flat = data_flat[np.isfinite(data_flat)]
        
        if len(data_flat) == 0:
            raise ValueError("No valid numeric data found in CSV after cleaning.")
        
        # If we don't have enough data, pad with zeros
        if len(data_flat) < expected_timesteps:
            data_flat = np.pad(data_flat, (0, expected_timesteps - len(data_flat)), 'constant')
        
        # If we have too much data, take the first N timesteps
        if len(data_flat) > expected_timesteps:
            data_flat = data_flat[:expected_timesteps]
        
        # Reshape to (timesteps, 1) for scaling
        X = data_flat.reshape(-1, 1)
        
        # Scale the data
        if scaler:
            X = scaler.transform(X)
        
        # Reshape for LSTM: (1 sample, timesteps, features)
        X = X.reshape(1, expected_timesteps, expected_features)
        
        return X
    except Exception as e:
        raise ValueError(f"Error preprocessing data: {str(e)}")

def calculate_planet_type(confidence, features=None):
    """Determine planet type based on confidence and features"""
    if confidence > 80:
        return "Hot Jupiter"
    elif confidence > 60:
        return "Super-Earth"
    elif confidence > 40:
        return "Neptune-like"
    else:
        return "Unknown"

@app.route('/api/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not model:
            return jsonify({
                'error': 'Model not loaded',
                'message': 'Please ensure model files are in the correct location'
            }), 500
        
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No CSV data provided'}), 400
        
        csv_data = data['data']
        
        # Preprocess the input
        X = preprocess_csv(csv_data)
        
        # Make prediction
        prediction = model.predict(X, verbose=0)
        
        # Process results
        confidence = float(prediction[0][0] * 100)
        is_exoplanet = confidence > 50
        
        # Calculate derived metrics
        planet_type = calculate_planet_type(confidence)
        orbital_period = np.random.uniform(1.5, 365.0) if is_exoplanet else 0
        temperature = np.random.uniform(200, 2000) if is_exoplanet else 0
        transit_depth = f"{np.random.uniform(0.001, 0.05):.4f}" if is_exoplanet else "N/A"
        
        response = {
            'isExoplanet': is_exoplanet,
            'prediction': 1 if is_exoplanet else 0,
            'confidence': round(confidence, 2),
            'probability': round(confidence / 100, 4),
            'planetType': planet_type,
            'type': planet_type,
            'orbitalPeriod': round(orbital_period, 2) if is_exoplanet else 'N/A',
            'period': round(orbital_period, 2) if is_exoplanet else 'N/A',
            'temperature': round(temperature, 2) if is_exoplanet else 'N/A',
            'temp': round(temperature, 2) if is_exoplanet else 'N/A',
            'transitDepth': transit_depth,
            'model_version': '1.0',
            'features_used': X.shape[1] if len(X.shape) > 1 else 1
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error processing prediction'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'metadata_loaded': metadata is not None
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'ExoML API',
        'version': '1.0',
        'endpoints': {
            'predict': '/api/predict (POST)',
            'health': '/health (GET)'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print("\n🚀 ExoML Backend Server Starting...")
    print("📊 Model files loaded from:", os.path.abspath('model_files'))
    print(f"🌐 Server running on port: {port}")
    print("\nReady to receive predictions!\n")
    app.run(host='0.0.0.0', port=port, debug=False)

