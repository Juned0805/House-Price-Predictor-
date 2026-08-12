# AI House Price Predictor

A complete end-to-end Machine Learning web application to predict property values using the California Housing Dataset and Random Forest Regression.

## Overview
This project demonstrates modern ML best practices:
- **ML Pipeline**: Handles fetching data, preprocessing, feature scaling, and comparing models (Linear Regression vs Random Forest).
- **Evaluation**: Calculates RMSE, MAE, and R² scores.
- **Backend**: Python Flask REST API to serve the trained model.
- **Frontend**: Clean, responsive, premium UI built with Bootstrap 5 and custom CSS.
- **Deployment**: Containerized via Docker for easy deployment.

## Project Structure
- `data/`: Raw dataset and samples (generated upon training).
- `models/`: Saved `.pkl` model artifacts.
- `src/train.py`: ML Pipeline script.
- `app.py`: Flask web application.
- `templates/`, `static/`: Frontend HTML, CSS, and JS code.
- `Dockerfile`: Container image definition.

## Installation & Setup

1. **Set up virtual environment & install dependencies**:
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/MacOS
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Train the Model**:
   You MUST train the model before running the application to generate the `.pkl` file.
   ```bash
   python src/train.py
   ```

3. **Run the Application Locally**:
   ```bash
   python app.py
   ```
   Navigate to `http://localhost:5000` to interact with the UI.

## Deployment (Docker)
You can easily deploy this app using Docker:
```bash
# Build the image
docker build -t house-price-predictor .

# Run the container
docker run -p 5000:5000 house-price-predictor
```

*Note: Make sure to either build the model locally before copying files into Docker, or inject a script step in Docker to run `src/train.py` if building a fresh container.*
