import pandas as pd
from prophet import Prophet
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from price_prediction import run_pipeline  # Import the pipeline function

def preprocess_data(data):
    """Preprocess data for Prophet model."""
    data['ds'] = pd.to_datetime(data['Modified Date'], format='%d/%m/%Y')
    data = data.sort_values('ds')

    # Feature engineering
    data['Year'] = data['ds'].dt.year
    data['Month'] = data['ds'].dt.month
    data['Day'] = data['ds'].dt.day

    return data

def train_and_forecast(data):
    """Train Prophet model and generate forecast."""
    # Model training
    prophet_model = Prophet()
    prophet_model.fit(data[['ds', 'Price']].rename(columns={'ds': 'ds', 'Price': 'y'}))

    # Prediction
    future = pd.DataFrame({'ds': pd.date_range(start=data['ds'].min(), end=data['ds'].max(), freq='D')})
    forecast = prophet_model.predict(future)

    return forecast

def comparative_analysis(data, forecast):
    """Perform comparative analysis by region, type, and nature."""
    results = []
    for region, type_, nature in data[['Region', 'Type', 'Nature']].drop_duplicates().values:
        subset = data[(data['Region'] == region) & (data['Type'] == type_) & (data['Nature'] == nature)]
        forecast_subset = forecast[(forecast['ds'].dt.month >= subset['ds'].min().month) & 
                                   (forecast['ds'].dt.month <= subset['ds'].max().month)]
        highest_price_month = forecast_subset.loc[forecast_subset['yhat'].idxmax(), 'ds'].strftime('%B')
        lowest_price_month = forecast_subset.loc[forecast_subset['yhat'].idxmin(), 'ds'].strftime('%B')
        highest_price = forecast_subset['yhat'].max()
        lowest_price = forecast_subset['yhat'].min()
        results.append([region, type_, nature, highest_price_month, lowest_price_month, highest_price, lowest_price])

    # Create DataFrame
    results_df = pd.DataFrame(results, columns=['Region', 'Type', 'Nature', 
                                                'Highest Price Month', 'Lowest Price Month', 
                                                'Highest Price', 'Lowest Price'])

    return results_df

def run_forecasting():
    """Run the full seasonal forecasting pipeline."""
    # Ensure data-preprocessing pipeline is run
    run_pipeline()

    # Load the preprocessed data
    data_path = '..\\..\\Data\\data-preprocessed.csv'
    data = pd.read_csv(data_path)

    # Preprocess data
    data = preprocess_data(data)

    # Train model and forecast
    forecast = train_and_forecast(data)

    # Perform comparative analysis
    results_df = comparative_analysis(data, forecast)

    # Save results to CSV
    results_path = '..\\..\\Data\\forecasting.csv'
    results_df.to_csv(results_path, index=False)

    print(f"Forecasting completed. Results saved to {results_path}")

# Make callable from another file
if __name__ == "__main__":
    run_forecasting()
