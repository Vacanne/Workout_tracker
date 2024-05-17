import requests
from datetime import datetime
import os

# Define constants and environment variables
GENDER = YOUR_GENDER
WEIGHT_KG = YOUR_WEIGHT
HEIGHT_CM = YOUR_HEIGHT
AGE = YOUR_AGE

APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]
SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]
TOKEN = os.environ["TOKEN"]

# Define endpoints
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

# Get exercise input from user
exercise_text = input("Tell me which exercises you did: ")

# Prepare headers and parameters for the API request
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Send request to Nutritionix API
response = requests.post(EXERCISE_ENDPOINT, json=parameters, headers=headers)
result = response.json()

# Get current date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Prepare authorization header for Google Sheets API
bearer_headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Iterate through each exercise and send data to Google Sheets
for exercise in result["exercises"]:
    sheet_data = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(SHEET_ENDPOINT, json=sheet_data, headers=bearer_headers)
    print(sheet_response.text)
