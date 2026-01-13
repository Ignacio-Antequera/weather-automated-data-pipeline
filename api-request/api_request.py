import requests

api_key = "9756743d52904661fd143d62f2943d32"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"

def fetch_data():
    print("Fetiching data from Weatherstack API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API respnse received successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise
    

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2026-01-12 09:08', 'localtime_epoch': 1768208880, 'utc_offset': '-5.0'}, 'current': {'observation_time': '02:08 PM', 'temperature': 0, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'], 'weather_descriptions': ['Sunny'], 'astro': {'sunrise': '07:19 AM', 'sunset': '04:50 PM', 'moonrise': '02:03 AM', 'moonset': '11:54 AM', 'moon_phase': 'Waning Crescent', 'moon_illumination': 37}, 'air_quality': {'co': '215.85', 'no2': '15.15', 'o3': '58', 'so2': '7.85', 'pm2_5': '6.55', 'pm10': '7.35', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 17, 'wind_degree': 285, 'wind_dir': 'WNW', 'pressure': 1023, 'precip': 0, 'humidity': 51, 'cloudcover': 0, 'feelslike': -4, 'uv_index': 1, 'visibility': 16, 'is_day': 'yes'}}