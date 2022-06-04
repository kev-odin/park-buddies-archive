from typing import Optional
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


def activities_parks(ids: Optional[list[str]], qry: str = None) -> list:
    """Retrieve national parks that are related to particular categories
    of activity (astronomy, hiking, wildlife watching, etc.).

    Returns:
        dict: all activities codified by NPS with associated parks
    """
    if not ids and (not qry or qry == ''):
        return []

    global params
    request_url = base_url + "activities/parks"
    p = params.copy()
    if ids is not None and ids != "":
        # XXX gross workaround: NPS API requires that multiple "id" values
        # be passed as a single string formatted as comma-separated list;
        # it does not support the standard alternative of multiple "id" params.
        # Meanwhile, Python requests library insists on URL-encoding everything
        # in params dict; and furthermore, thinks comma needs to be encoded.
        # This encoding can be circumvented by including query-string in URL.
        # Additional params can still be specified and will be correctly
        # appended with ampersand instead of question-mark.
        # p["id"] = ids
        request_url = f"{request_url}?id={','.join(ids)}"
    if qry is not None and qry != "":
        p["q"] = qry
    response = requests.get(request_url, params=p)
    return response.json()["data"]


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
