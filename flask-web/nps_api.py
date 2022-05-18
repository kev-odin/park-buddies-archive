import requests

base_url = f"https://developer.nps.gov/api/v1/"
params = {"api_key": "rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"}


def _address_string(addresses: dict):
    return f"{addresses['line1']}, {addresses['city']}, {addresses['stateCode']} {addresses['postalCode']}"


def activities():
    """
    Returns dictionary of all activities codified by NPS
    {activity_name : json}
    """
    request_url = base_url + "activities"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    activites = {x["name"]: x for x in data}
    return activites


def activities_parks():
    """
    Returns dictionary of all activities that can be enjoyed at each park
    {activity_name : json}
    """
    request_url = base_url + "activities/parks"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    activities_parks = {x["name"]: x for x in data}
    return activities_parks


def parks(state_code: str = None):
    """
    Returns a dictionary of parks in a provided state
    {park_code : json}
    """
    request_url = base_url + "parks"
    params["stateCode"] = state_code
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    parks = {x["parkCode"]: x for x in data}

    for parkCode in parks.items():
        parks[parkCode[0]]["address"] = _address_string(parkCode[1]["addresses"][0])
    return parks


def webcams():
    """
    Returns dict of active webcams at each park
    {park_code : json}
    """
    # params["limit"] = 500
    params["limit"] = 500 # test
    request_url = base_url + "webcams"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]
    webcams = {
        x["relatedParks"][0]["parkCode"]: x
        for x in data
        if x["status"] == "Active" and x["relatedParks"] and len(x["images"]) > 0
    }
    
    for value in webcams.items():
        related = value[1].pop("relatedParks")[0]
        webcams[value[0]]["webpage"] = related.pop("url")
        webcams[value[0]].update(related)
        z = 1

    return webcams


if __name__ == "__main__":
    test0 = activities()
    test1 = activities_parks()
    test2 = webcams()
    test3 = parks()
    x = 0
