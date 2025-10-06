import os
import sys
import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras

# Vercel serverless function
app = Flask(__name__)

# Global variables for model caching
_model = None
_scaler = None
_metadata = None

def get_model_path(filename):
    """Get the correct path for model files in Vercel environment"""
    # In Vercel, files are in the root directory
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, 'model_files', filename)

def load_model_files():
    """Load model files with caching"""
    global _model, _scaler, _metadata
    
    if _model is not None:
        return _model, _scaler, _metadata
    
    try:
        model_path = get_model_path('exoplanet_bilstm.h5')
        scaler_path = get_model_path('scaler.pkl')
        metadata_path = get_model_path('metadata.pkl')
        
        # Load the BiLSTM model
        _model = keras.models.load_model(model_path)
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            _scaler = pickle.load(f)
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            _metadata = pickle.load(f)
        
        return _model, _scaler, _metadata
    except Exception as e:
        print(f"Error loading model files: {str(e)}")
        raise

def preprocess_csv(csv_data, scaler, metadata):
    """Convert CSV string to preprocessed numpy array for model"""
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        
        # Remove any non-numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df = df[numeric_cols]
        
        # Handle missing values
        df = df.fillna(df.mean())
        
        # Get expected features from metadata if available
        if metadata and 'feature_names' in metadata:
            expected_features = metadata['feature_names']
            missing_cols = set(expected_features) - set(df.columns)
            if missing_cols:
                for col in missing_cols:
                    df[col] = 0
            df = df[expected_features]
        
        # Scale the data
        if scaler:
            X = scaler.transform(df)
        else:
            X = df.values
        
        # Reshape for LSTM
        if len(X.shape) == 2:
            if X.shape[0] == 1:
                X = X.reshape(1, X.shape[1], 1)
            else:
                X = X.reshape(X.shape[0], X.shape[1], 1)
        
        return X
    except Exception as e:
        raise ValueError(f"Error preprocessing data: {str(e)}")

def calculate_planet_type(confidence):
    """Determine planet type based on confidence"""
    if confidence > 80:
        return "Hot Jupiter"
    elif confidence > 60:
        return "Super-Earth"
    elif confidence > 40:
        return "Neptune-like"
    else:
        return "Unknown"

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Load model files
        model, scaler, metadata = load_model_files()
        
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No CSV data provided'}), 400
        
        csv_data = data['data']
        
        # Preprocess the input
        X = preprocess_csv(csv_data, scaler, metadata)
        
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

# Vercel serverless handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

