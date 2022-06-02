import requests

base_url = f"https://developer.nps.gov/api/v1/"
params = {"api_key": "rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"}


def activities():
    """Retrieve categories of activities (astronomy, hiking, wildlife watching, etc.) possible in national parks.

    Returns:
        dict: all activities codified by NPS
    """
    request_url = base_url + "activities"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]

    # Restructure as list of tuples (id, name), consistent with wtforms
    # SelectField choices, i.e. list of tuples (value, label).
    results = [(_x["id"], _x["name"]) for _x in data]
    return results


def activities_parks(ids: str = None, qry: str = None):
    """Retrieve national parks that are related to particular categories of activity (astronomy, hiking, wildlife watching, etc.).

    Returns:
        dict: all activities codified by NPS with associated parks
    """
    global params
    p = params.copy()
    if ids is not None and ids != "":
        p["id"] = ids
    if qry is not None and qry != "":
        p["q"] = qry
    request_url = base_url + "activities/parks"
    response = requests.get(request_url, params=p)
    data = response.json()["data"]

    # Response data structure is... inconvenient:
    # [ { id: <Activity1_id>, name: <Activity1_name>, parks:
    #     [ { parkCode: <Park1_code>, fullName: <Park1_name>, ... },
    #       { parkCode: <Park2_code>, fullName: <Park2_name>, ... },
    #       ... ] },
    #   { id: <Activity2_id>, name: <Activity2_name>, parks:
    #     [ { parkCode: <ParkX_code>, fullName: <ParkX_name>, ... },
    #     [ { parkCode: <ParkY_code>, fullName: <ParkY_name>, ... },
    #       ... ] },
    #   ... ]
    # Parks info is repeated under every actiity applicable to it.
    #
    # Restructure to something more convenient, a dict of dicts:
    # { <Park1_code>: { "Name": <Park1_name>,
    #                   <Activity1_name>: <bool>,
    #                   <Activity2_name>: <bool>,
    #                   ... },
    #   <Park2_code>: { "Name": <Park2_name>,
    #                   <Activity1_name>: <bool>,
    #                   ... },
    #   ... }
    #
    # A more compact representation is certainly possible,
    # but the above strikes a reasonable balance.
    a_names = [x["name"] for x in data]
    results = {}
    for activ in data:
        a_name = activ["name"]
        print(f"a_name = {a_name}")
        for park in activ["parks"]:
            p_id = park["parkCode"]
            if p_id not in results:
                results[p_id] = {"Name": park["fullName"]}
            results[p_id][a_name] = True
    for a_name in a_names:
        for p_id in results.keys():
            if a_name not in results[p_id]:
                results[p_id][a_name] = False
    return results


def parks(state_code: str = None, park_code: str = None):
    """Retrieve data about national parks (addresses, contacts, description, hours of operation, etc.).

    Args:
        state_code (str, optional): A comma delimited list of 2 character state codes. Defaults to None.
        park_code (str, optional): A comma delimited list of park codes (each 4-10 characters in length). Defaults to None.

    Returns:
        dict: all parks listed in the US
    """
    params["limit"] = 500
    params["parkCode"] = park_code
    params["stateCode"] = state_code
    request_url = base_url + "parks"

    response = requests.get(request_url, params=params)
    data = response.json()["data"]

    parks = {x["parkCode"]: x for x in data}
    for parkCode in parks.items():
        parks[parkCode[0]]["address"] = _address_string(parkCode[1]["addresses"][0])
    return parks


def webcams():
    """Retrieve metadata about National Park Service streaming and non-streaming web cams.

    Returns:
        dict: all activities codified by NPS with associated parks
    """
    params["limit"] = 500
    request_url = base_url + "webcams"

    response = requests.get(request_url, params=params)
    data = response.json()["data"]

    webcam_data = {
        x["relatedParks"][0]["parkCode"]: x
        for x in data
        if x["status"] == "Active" and x["relatedParks"] and len(x["images"]) > 0
    }
    webcams = _webcam_scrub(webcam_data)

    return webcams


def _address_string(addresses: dict):
    return f"{addresses['line1']}, {addresses['city']}, {addresses['stateCode']} {addresses['postalCode']}"


def _webcam_scrub(park_cams: dict):
    """
    Helper function to update related data for the Flask webpage
    """
    ref_parks = parks()
    new_dict = {key: ref_parks[key] for key in park_cams.keys() if key in ref_parks}
    x = 0

    for key, value in park_cams.items():
        new_images = new_dict[key]["images"]
        for image in new_images:
            park_cams[key]["images"].append(image)

        related = value.pop("relatedParks")[0]
        park_cams[key]["webpage"] = related.pop("url")
        park_cams[key].update(related)

    return park_cams


if __name__ == "__main__":
    test0 = activities()
    test1 = activities_parks()
    test2 = parks()
    test3 = webcams()

# END
