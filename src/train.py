import os
import joblib
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_mock_indian_housing_data(n_samples=15000):
    """Generates a mock dataset for Indian housing with logical price correlations."""
    np.random.seed(42)
    
    locations = [
        'Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Hyderabad', 
        'Chennai', 'Ahmedabad', 'Kolkata', 'Jaipur', 'Surat'
    ]
    bhk_options = [1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    
    # Base prices per sqft in INR
    base_price_sqft = {
        'Mumbai': 18000, 
        'Delhi': 12000,
        'Bangalore': 9000, 
        'Pune': 7500, 
        'Hyderabad': 7200,
        'Chennai': 6500, 
        'Ahmedabad': 5500,
        'Kolkata': 5000,
        'Surat': 4800,
        'Jaipur': 4500
    }
    
    data = {
        'Location': np.random.choice(locations, n_samples),
        'BHK': np.random.choice(bhk_options, n_samples),
        'ConstructionYear': np.random.randint(1995, 2025, n_samples),
        'HasParking': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]), # 70% have parking
        'HasElevator': np.random.choice([0, 1], n_samples, p=[0.2, 0.8]) # 80% have elevators
    }
    
    df = pd.DataFrame(data)
    
    # Calculate sensible sqft based on BHK (approx 500-600 sqft per BHK unit on average)
    df['SquareFootage'] = df['BHK'] * np.random.uniform(450, 650, n_samples)
    
    # Calculate target Price (INR)
    prices = []
    for _, row in df.iterrows():
        price = row['SquareFootage'] * base_price_sqft[row['Location']]
        age = 2025 - row['ConstructionYear']
        price = price * (1 - (age * 0.005))
        
        if row['HasParking']: price += 300000 
        if row['HasElevator']: price += 200000 
        
        price = price * np.random.uniform(0.90, 1.10)
        prices.append(price)
        
    df['Price'] = prices
    return df

def main():
    logging.info("Starting Indian model training pipeline with extended cities...")
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    df = generate_mock_indian_housing_data(15000)
    df.to_csv('data/indian_housing_dataset.csv', index=False)
    
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    categorical_features = ['Location']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    numeric_features = ['BHK', 'SquareFootage', 'ConstructionYear', 'HasParking', 'HasElevator']
    numeric_transformer = StandardScaler()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    logging.info("Training Random Forest...")
    rf_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    rf_pipeline.fit(X_train, y_train)
    rf_preds = rf_pipeline.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    r2 = r2_score(y_test, rf_preds)
    logging.info(f"Random Forest - RMSE: ₹{rmse:,.2f} | R²: {r2:.4f}")

    model_path = 'models/indian_house_price_model.pkl'
    joblib.dump(rf_pipeline, model_path)
    logging.info("Pipeline completed successfully!")

if __name__ == '__main__':
    main()
