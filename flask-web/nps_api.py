import requests

API_KEY = "?api_key=rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"

base_url = f"https://developer.nps.gov/api/v1/"

response = requests.get(base_url)


def activity_list():
    activities_url = base_url + f"activities{API_KEY}"
    response = requests.get(activities_url)
    return response.json() 

print(activity_list())

def webcams():
    pass

def parks_info():
    pass