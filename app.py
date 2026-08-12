import os
import joblib
import logging
import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib

#(LOADING NEW COMPRESSED FILE)
model = joblib.load("models/indian_house_price_model.joblib")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Load the Indian-context model
model = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'indian_house_price_model.pkl')

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        logging.info("Indian House Price Model loaded successfully.")
    else:
        logging.warning("Model not found. Please run src/train.py first.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

@app.route('/')
def home():
    """Render the home page with the input form."""
    return render_template('index.html')

def format_indian_rupee(amount):
    """Formats number nicely in Indian system (Crores/Lakhs) and exact commas"""
    if amount >= 10000000:
        cr = amount / 10000000
        return f"₹{cr:,.2f} Crore"
    elif amount >= 100000:
        L = amount / 100000
        return f"₹{L:,.2f} Lakhs"
    else:
        return f"₹{amount:,.0f}"

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to predict house prices based on form input."""
    if not model:
        return jsonify({'error': 'Model is not trained yet. Run the training script.'}), 500
        
    try:
        # Get data from POST request
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            
        logging.info(f"Received prediction request: {data}")
        
        # Safely extract and typecast features
        features_dict = {
            'Location': data.get('Location', 'Mumbai'),
            'BHK': float(data.get('BHK', 2.0)),
            'SquareFootage': float(data.get('SquareFootage', 1000.0)),
            'ConstructionYear': int(data.get('ConstructionYear', 2008)),
            'HasParking': int(data.get('HasParking', 0)),
            'HasElevator': int(data.get('HasElevator', 0))
        }
        
        # Must package as DataFrame so ColumnTransformer maps properly
        features_df = pd.DataFrame([features_dict])
        
        # Predict
        predicted_price_inr = model.predict(features_df)[0]
        
        # Format the INR string
        formatted_inr_text = format_indian_rupee(predicted_price_inr)
        
        # Convert to USD (Approx current exchange rate)
        predicted_price_usd = predicted_price_inr / 95.0
        formatted_usd_text = f"Approx: ${predicted_price_usd:,.0f} USD"
        
        return jsonify({
            'success': True,
            'predicted_price_inr': round(predicted_price_inr, 2),
            'formatted_inr': formatted_inr_text,
            'formatted_usd': formatted_usd_text,
            'features_used': features_dict
        })
        
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
