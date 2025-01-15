### ***Key Features:***

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

---

### **List Of Technologies Used**

### 1. **Pandas**
   - **Usage**: 
     - Data manipulation and analysis.
     - Loading, preprocessing, and filtering datasets (e.g., real estate data).
   - **Files**: 
     - `preprocessing.py`: Handles CSV data processing.
     - Main application files: For filtering and displaying data.

---

### 2. **Streamlit**
   - **Usage**: 
     - Building the interactive user interface for the web app.
     - Displaying dropdowns, sliders, and results for predictions and forecasts.
   - **Files**: 
     - Main application file ( `UI.py`).

---

### 3. **Prophet**
   - **Usage**: 
     - Time series forecasting for predicting seasonal price trends.
     - Identifying the best and worst months for investment.
   - **Files**: 
     - `seasonal_forecasting.py`: Implements seasonal forecasting models.

---

### 4. **Scikit-learn**
   - **Usage**: 
     - Machine learning for real estate price predictions.
     - **RandomForestRegressor**: Used to build a regression model for predicting property prices based on location, type, and nature.
     - Encoding categorical data (e.g., `LabelEncoder`).
   - **Files**: 
     - `price_prediction.py`: Trains and uses the Random Forest model.

---

### 5. **Asyncio**
   - **Usage**: 
     - Enables asynchronous programming to efficiently scrape data from the **TunisieAnnonces** website.
   - **Files**: 
     - `tunisieannonces.py`: Implements asynchronous web scraping.

---

### 6. **Pyppeteer**
   - **Usage**: 
     - Automates a headless browser for dynamic website scraping, allowing interaction with JavaScript-rendered pages.
   - **Files**: 
     - `tunisieannonces.py`: Handles navigation, content rendering, and interaction on the **TunisieAnnonces** website.

---

### 7. **BeautifulSoup** (from `bs4`)
   - **Usage**: 
     - HTML parsing and extraction of relevant data during web scraping.
   - **Files**: 
     - `tunisieannonces.py`: Extracts data like property titles, prices, and descriptions.

---

### 8. **Requests**
   - **Usage**: 
     - Makes HTTP requests to fetch data from web pages.
   - **Files**: 
     - `tunisieannonces.py`: Retrieves HTML content from the **TunisieAnnonces** website.

---

### 9. **Numpy**
   - **Usage**: 
     - Numerical operations and array manipulations.
     - Supporting data preprocessing and feature engineering tasks.
   - **Files**: 
     - Used wherever numerical calculations or array transformations are required (e.g., during preprocessing or predictions).

---

### 10. **Os**
   - **Usage**: 
     - Handling file paths and directory structures.
     - Dynamically setting the working directory for imports and file operations.
   - **Files**: 
     - Commonly used across multiple scripts.

---

### 11. **Sys**
   - **Usage**: 
     - Modifying the Python path for dynamic imports based on the project's structure.
   - **Files**: 
     - Commonly used in entry-point files.

---

### 12. **Datetime** (from Python Standard Library)
   - **Usage**: 
     - Handling date and time operations, such as extracting the current month for forecasting insights.
   - **Files**: 
     - Main application file: Displays insights for the current month.
    

---

To run the app type in the command : streamlit run MainPackage/Pages/UI.py

You can find the demo here : https://youtu.be/AS_XeFh-4fQ
