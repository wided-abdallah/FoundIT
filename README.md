Key Features:

Data Scraping:

The project includes a web scraper that collects property data from 'TunisieAnnonces', a popular Tunisian real estate website.
It extracts essential property details such as region, nature, type, and price.
This process is managed by the module 'tunisieannonces.py' that generates a csv file ('tunisie-annonces.csv'), containing organized scraped data.
I have named the module after the website because I plan on adding more website scrapers in the future.
It shouldn't be too different from the one I have included though, depending on the structure of the websites.


Data Preprocessing:

After collection, the raw data undergoes preprocessing to clean, structure, and prepare it for modeling.
Missing values, incorrect data types, and other inconsistencies are handled to ensure the dataset is ready for machine learning models.
This process is managed by the module 'preprocessing.py' that generates a csv file ('data-preprocessed.csv') containing the cleaned data.


Price Prediction:

Using a Random Forest Regressor model, the app allows users to predict the price of a property based on various parameters like region, nature and property type.
The model is trained on historical data and offers price predictions for selected parameters with high accuracy.
This process is managed by the module 'price_prediction.py'.


Seasonal Forecasting:

The app leverages Prophet, a forecasting tool by Facebook, to predict the seasonal fluctuations in property prices.
It identifies the best months to invest based on historical price trends, guiding users on when to buy, rent or sell properties and when to avoid doing so.
This process is managed by the module 'seasonal_forecasting.py' that generates a csv fie('forecasting.csv') containing the predicted data.
The predicted data consists of : 
1 - the combination of prediction (Region, Type, Nature)
2- Month extrema (Highest Price Month / Lowest Price Month)
3- Price extrema (Highest Price / Lowest Price)


User Interface with Streamlit:

The frontend is built using Streamlit, offering a clean and interactive user interface that simplifies the real estate price prediction and analysis process.
Users can select a region, property type, and nature to get a price prediction and insights into investment trends.
Visualizations are presented dynamically based on user input.
the streamlit app is 'UI.py'.


Investment Insights:

Based on the seasonal forecasting data, the app also provides suggestions on whether it’s a good time to invest in a given property.
It compares the current month with historical trends and alerts users to the best and worst months for property investments.
