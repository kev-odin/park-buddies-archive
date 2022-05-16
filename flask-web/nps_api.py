import requests

base_url = f"https://developer.nps.gov/api/v1/"
params = {"api_key": "rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"}


def _address_string(addresses: dict):
    return f"{addresses[0]['line1']}, {addresses[0]['city']}, {addresses[0]['stateCode']} {addresses[0]['postalCode']}"


def activities():
    """
    Returns list of activities that can be enjoyed at every park
    [activity_1, ...]
    """
    request_url = base_url + "activities"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    activites = [x["name"] for x in data]
    return activites


def webcams():
    """
    Returns list of active webcams at each park
    [(webcam_title, url_link, related_parks)]
    """
    params["limit"] = 500
    request_url = base_url + "webcams"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    webcams = [
        (x["title"], x["url"], x["relatedParks"])
        for x in data
        if x["status"] == "Active"
    ]
    return webcams


def parks(state_code: str = "WA"):
    """
    Returns a list of parks in a provided state
    [(state_name, park_code, park_address, park_images)]
    """
    request_url = base_url + "parks"
    params["stateCode"] = state_code
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    parks = [
        (x["fullName"], x["parkCode"], _address_string(x["addresses"]), x["images"])
        for x in data
    ]
    return parks

