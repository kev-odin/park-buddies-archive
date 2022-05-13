import requests

# API_KEY = "rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"
# make request to session token 
API_KEY = "P8tQHRp3dvGMLzBQeXOwHQmi456Eyo3zgGpYI8Gw"
STATE = "id"

# endpoint = f"https://developer.nps.gov/api/v1/parks?stateCode={STATE}&api_key={API_KEY}"
target = "webcams"
endpoint = f"https://developer.nps.gov/api/v1/"+target+f"?limit=3&api_key={API_KEY}"


response = requests.get(endpoint)
data = response.json()
print(data)
parks = data["data"]


park_code = {}
for entry in parks:
    park_code[entry["parkCode"]] = (entry["states"], entry["fullName"])

# print(park_code)
