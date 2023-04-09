import requests
import json

# Define the JSON data you want to send
data = {"key":"hello"}
url="http://13.50.241.7//webhook"
# Convert the data to a JSON string
json_data = json.dumps(data)

# Set the content type header to indicate that you are sending JSON data
headers = {"Content-Type": "application/json"}

# Send the request
response = requests.post(url, headers=headers, data=json_data)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    print("Sbu")
    print(response.text)
else:
    # Request failed
    print(response.text)
