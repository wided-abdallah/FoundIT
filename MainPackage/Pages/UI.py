import sys
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Found-it', page_icon=':house_with_garden:', layout='centered')

video_html = """
		<style>

		#myVideo {
		  position: fixed;
		  right: 0;
		  bottom: 0;
		  min-width: 100%; 
		  min-height: 100%;
		}

		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(0, 0, 0, 0.5);
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
		}

		</style>	
		<video autoplay muted loop id="myVideo">
		  <source src="https://videos.pexels.com/video-files/3129957/3129957-hd_1280_720_25fps.mp4")>
		  Your browser does not support HTML5 video.
		</video>
        """

st.markdown(video_html, unsafe_allow_html=True)
st.title('Found-it : Real Estate Assistant')

# Custom CSS styles
css = """
<style>
/* Transparent background for select boxes */
div[data-baseweb="select"]>div {
    background-color: rgba(0, 0, 0, 0.7) !important; /* Adjust opacity as needed */
</style>
"""

# Apply the custom CSS styles
st.markdown(css, unsafe_allow_html=True)


# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import custom functions from ML_models
from MainPackage.ML_models.price_prediction import predict_price, model, encoder

# Load the preprocessed data and rename the 'Text' column to 'Contact'
data = pd.read_csv('../../Data/data-preprocessed.csv')

# Load the forecasting data
forecasting_data = pd.read_csv('../../Data/forecasting.csv')


# Get unique values for dropdown menus
regions = sorted(data['Region'].unique())
natures = sorted(data['Nature'].unique())
property_types = sorted(data['Type'].unique())

# Dropdown menus for region, nature, and property type
region = st.selectbox('Select Region', [None] + regions)
nature = st.selectbox('Select Nature', [None] + natures)
property_type = st.selectbox('Select Property Type', [None] + property_types)

# Predict button
if st.button('Predict Price'):
    # Get the predicted price
    if region is not None and nature is not None and property_type is not None:
        predicted_price = predict_price(region, nature, property_type, model, encoder)
        rounded_price = round(predicted_price)
        st.success(f"Predicted price for [{region}, {nature}, {property_type}]: {rounded_price}")

        # Get the current month
        current_month = pd.Timestamp.now().strftime('%B')

        # Check if the current month is significant for investment
        if current_month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
            if current_month in forecasting_data[(forecasting_data['Region'] == region) & (forecasting_data['Nature'] == nature) & (forecasting_data['Type'] == property_type)]['Highest Price Month'].values:
                st.warning(f"The current month ({current_month}) is significant for investment as it is one of the highest price months.")
            elif current_month in forecasting_data[(forecasting_data['Region'] == region) & (forecasting_data['Nature'] == nature) & (forecasting_data['Type'] == property_type)]['Lowest Price Month'].values:
                st.warning(f"The current month ({current_month}) is significant for investment as it is one of the lowest price months.")
            else:
                # Check if there are rows in forecasting_data that match the filtering conditions
                if not forecasting_data.empty and len(forecasting_data[(forecasting_data['Region'] == region) & (forecasting_data['Nature'] == nature) & (forecasting_data['Type'] == property_type)]) > 0:
                    # Get the indices of the highest and lowest price months within the year
                    highest_month_index_in_year = (forecasting_data[(forecasting_data['Region'] == region) & (forecasting_data['Nature'] == nature) & (forecasting_data['Type'] == property_type)]['Highest Price Month'] == current_month).idxmax()
                    lowest_month_index_in_year = (forecasting_data[(forecasting_data['Region'] == region) & (forecasting_data['Nature'] == nature) & (forecasting_data['Type'] == property_type)]['Lowest Price Month'] == current_month).idxmax()

                    # Get the index of the current month within the year
                    current_month_index_in_year = pd.Timestamp.now().month - 1

                    # Calculate the differences between the current month's index and the indices of the highest and lowest price months
                    diff_to_highest = highest_month_index_in_year - current_month_index_in_year
                    diff_to_lowest = lowest_month_index_in_year - current_month_index_in_year

                    # Adjust differences if they are negative
                    if diff_to_highest < 0:
                        diff_to_highest += 12
                    if diff_to_lowest < 0:
                        diff_to_lowest += 12

                    if diff_to_lowest < diff_to_highest:
                        st.info(f"The current month ({current_month}) is not significant for investment. Consider waiting until the closest lowest price month ({forecasting_data.loc[lowest_month_index_in_year, 'Lowest Price Month']}) before investing.")
                    else:
                        st.info(f"The current month ({current_month}) is not significant for investment. Consider investing before the closest highest price month ({forecasting_data.loc[highest_month_index_in_year, 'Highest Price Month']}).")

                        # Display the best and worst months for investment
                        st.info(f"Best month to invest: {forecasting_data.loc[lowest_month_index_in_year, 'Lowest Price Month']}")
                        st.info(f"Worst month to invest: {forecasting_data.loc[highest_month_index_in_year, 'Highest Price Month']}")
                else:
                    st.warning("No data available for the selected region, nature, and property type.")


# Search
# Filter data based on user input
filtered_data = data[
    ((data['Region'] == region) | (region is None)) &  # Filter by region
    ((data['Nature'] == nature) | (nature is None)) &  # Filter by nature
    ((data['Type'] == property_type) | (property_type is None))  # Filter by property type
]

# Determine min and max price values based on selected nature
if nature:
    min_price = filtered_data[filtered_data['Nature'] == nature]['Price'].min()
    max_price = filtered_data[filtered_data['Nature'] == nature]['Price'].max()
else:
    min_price = filtered_data['Price'].min()
    max_price = filtered_data['Price'].max()

# Ensure min_price and max_price are not NaN
if pd.notnull(min_price) and pd.notnull(max_price):
    # Price slider
    price_range = st.slider('Price Range', min_value=min_price, max_value=max_price, value=(min_price, max_price))
    # Filter data based on price range
    filtered_data = filtered_data[(filtered_data['Price'] >= price_range[0]) & (filtered_data['Price'] <= price_range[1])]
    # Display filtered data
    if not filtered_data.empty:
        st.write(filtered_data)
    else:
        st.warning("No data available for the selected filters.")