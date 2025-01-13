import pandas as pd
import re
import random
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from tunisieannonces import run_scraper  # Import the scraper function

def run_preprocessing():
    # Run the scraper to generate the CSV file
    run_scraper()

    # Load the dataset
    data = pd.read_csv('tunisie-annonces.csv')

    # Preprocess the data
    def preprocess_data(data):
        """
        Preprocesses the data by:
        1. Removing non-numeric characters from 'Price'
        2. Converting 'Price' to numeric (float), handling errors with 'coerce'
        3. Dropping rows with NaN values in 'Price' (optional, adjust as needed)
        4. Ignoring 'Modified Date' (not explicitly required for this task)
        """

        # Remove non-numeric characters from 'Price'
        pattern = r"[^\d\-+\.]"  # Match non-digits, hyphen, plus/minus, or period
        data['Price'] = data['Price'].apply(lambda x: re.sub(pattern, "", str(x)))

        # Convert 'Price' to numeric (float), handling errors with 'coerce'
        data['Price'] = pd.to_numeric(data['Price'], errors='coerce')

        # Drop rows with NaN values in 'Price'
        data.dropna(subset=['Price'], inplace=True)

        return data

    data = preprocess_data(data.copy())  # Operate on a copy

    # Rename 'Text' column to 'Contact'
    data = data.rename(columns={'Text': 'Contact'})

    # Function to generate random phone numbers
    def generate_phone_number():
        prefix = '+216 '
        first_digit = random.choice(['2', '5', '9', '7'])
        middle_digits = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return f'{prefix}{first_digit}{middle_digits}'

    # Generate the link
    link = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp'

    # Replace the 'Contact' column values with randomly generated phone numbers and the link
    data['Contact'] = data['Contact'].apply(lambda _: f'{generate_phone_number()} - [{link}]')

    # Save the preprocessed data to a new CSV
    data.to_csv('data-preprocessed.csv', index=False)

    print("Data preprocessed and saved to data-preprocessed.csv")
