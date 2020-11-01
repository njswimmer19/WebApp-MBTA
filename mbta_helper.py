import urllib.request
import urllib.parse
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = 'nuQhpfoH3OuWrwtAhp9xvV1qO4UkZ8Ha'
MBTA_API_KEY = '9fc50701870a41cea584be3a83ab4f9c'

# URL
url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location=Babson%20College'

# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    # pprint(response_data)

    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    place_name = place_name.replace(" ","%20")
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}'

    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    location = response_data["results"][0]["locations"][0]['latLng']
    location_tuple = tuple(location.values()) 

    return location_tuple

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url = f'{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance'
    closest_station_json = get_json(url)

    wheelchair_boarding_station = closest_station_json['data'][0]['attribute']['name'],closest_station_json['data'][0]['attribute']['wheelchair_boarding']

    return wheelchair_boarding_station


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    latLng = get_lat_long(place_name)
    latitude = latLng[0]
    longitude = latLng[1]

    return get_nearest_station(latitude, longitude)


def main():
    """
    You can test all the functions here
    """
    place_name = "Babson College"
    print(get_lat_long(place_name))

    lat = str(get_lat_long(place_name)[0])
    lng = str(get_lat_long(place_name)[1])

    print(get_nearest_station(lat, lng))


if __name__ == '__main__':
    main()
