import requests

API_KEY = "rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"

endpoint = f"https://developer.nps.gov/api/v1/parks?stateCode=wa&api_key={API_KEY}"

response = requests.get(endpoint)
data = response.json()
wa_parks = data["data"]

for idx, name in enumerate(wa_parks):
    print(f'Location: {wa_parks[idx]["latLong"]}')
    print(f'{wa_parks[idx]["fullName"]}\n')
