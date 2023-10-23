import requests
from datetime import datetime
import os

# Retrieve environment variables
APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]
sheet_endpoint = os.environ["sheet_endpoint"]
authorization_token = os.environ["Authorization"]

# Create headers for the Nutritionix API request
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

# Prepare data for the Nutritionix API request
exercise = input("Tell me which exercises you did today?")

data = {
    "query": exercise,
    "gender": "male",
    "weight_kg": 77,
    "height_cm": 182,
    "age": 23
}

# Make a POST request to the Nutritionix API
response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", json=data, headers=headers)
response.raise_for_status()
result = response.json()

# Get current date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Create headers for the Sheety API request
sheet_headers = {
    "Authorization": authorization_token
}

# Process and send data to the Sheety API
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Make a POST request to the Sheety API
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=sheet_headers)

    # Print the response from the Sheety API
    print(sheet_response.text)
