import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import sys
import os


# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Data/")))

from preprocessing import run_preprocessing 

def load_data(file_path):
    """Loads the dataset from a CSV file."""
    return pd.read_csv(file_path)

def preprocess_data(data):
    """Preprocess the data by converting the 'Price' column to numeric."""
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
    return data

def train_model(data):
    """Trains a Random Forest model and returns the model and encoder."""
    # Split features and target variable
    X = data[['Region', 'Nature', 'Type']]
    y = data['Price']

    # Encode categorical features
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Define the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Evaluate the model
    train_rmse = root_mean_squared_error(y_train, y_pred_train, squared=False)
    test_rmse = root_mean_squared_error(y_test, y_pred_test, squared=False)

    print(f"Train RMSE: {train_rmse}")
    print(f"Test RMSE: {test_rmse}")

    return model, encoder

def predict_price(region, nature, property_type, model, encoder):
    """Predicts the price given input features."""
    # Transform input features into numerical format
    input_features = pd.DataFrame([[region, nature, property_type]], columns=['Region', 'Nature', 'Type'])
    input_encoded = encoder.transform(input_features)

    # Make prediction
    predicted_price = model.predict(input_encoded)

    return predicted_price[0]

def run_pipeline():
    """Runs the entire pipeline: scraping, preprocessing, training, and evaluation."""
    # Run the preprocessing pipeline
    run_preprocessing()

    # Load the preprocessed data
    data = load_data('..\\..\\Data\\data-preprocessed.csv')

    # Preprocess the data
    data = preprocess_data(data)

    # Train the model
    model, encoder = train_model(data)

    return model, encoder
