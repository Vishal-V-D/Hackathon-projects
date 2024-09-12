import requests
import json

# Your API key
api_key = ''

# Endpoint URL
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

inp = input("enter a general qurey: ")
data = {
    "contents": [
        {
            "parts": [
                {"text": f"5 keyword to describee {inp}"}
            ]
        }
    ]
}

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check the response status
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
