import requests_cache
import pandas as pd
from retry_requests import retry
import openmeteo_requests

# Function to create descriptive text for each day's weather
def create_weather_descriptions(df):
    descriptions = []
    for index, row in df.iterrows():
        description = (f"On {row['date'].strftime('%Y-%m-%d')}, the maximum temperature is {row['temperature_2m_max']}°C, "
                      f"the minimum temperature is {row['temperature_2m_min']}°C, "
                      f"and the total rainfall is {row['rain_sum']}mm.")
        descriptions.append(description)
    return descriptions

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def fetch_weather_data(latitude=37.98, longitude=23.72): # Default coordinates for Athens, Greece
    # Define the API request parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "rain_sum"],
        "timezone": "auto"
    }

    # Make the API call
    url = "https://api.open-meteo.com/v1/forecast"
    responses = openmeteo.weather_api(url, params=params)

    # Process the response and return daily data as a DataFrame
    response = responses[0]
    daily = response.Daily()
    daily_dataframe = pd.DataFrame({
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "weather_code": daily.Variables(0).ValuesAsNumpy(),
        "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
        "temperature_2m_min": daily.Variables(2).ValuesAsNumpy(),
        "rain_sum": daily.Variables(3).ValuesAsNumpy()
    })

    return daily_dataframe

def get_weather_description(latitude, longitude):
    # Fetch the weather data
    weather_data = fetch_weather_data(latitude, longitude)
    
    # Create weather descriptions from the data
    weather_descriptions = create_weather_descriptions(weather_data)
    return ' '.join(weather_descriptions)
