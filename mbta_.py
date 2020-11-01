import urllib.request
import urllib.parse
import json
from pprint import pprint


# MY API KEYS
MAPQUEST_API_KEY = 'nuQhpfoH3OuWrwtAhp9xvV1qO4UkZ8Ha'
MBTA_API_KEY = '9fc50701870a41cea584be3a83ab4f9c'

# URL
url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location=Babson%20College'

def req_json(url):
    """
    url is the URL of the json
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    # pprint(response_data)

    return response_data

def extract_latLng(location_name):
    """
    location_name is the name of the location
    """
    location_name = location_name.replace(" ","%20")
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={location_name}'

    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    location = response_data["results"][0]["locations"][0]['latLng']
    location_tuple = tuple(location.values()) 
    
    return location_tuple

def extract_closest_station(lat, lng):
    url = f'https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&filter[latitude]={lat}&filter[longitude]={lng}&sort=distance'
    closest_station_json = req_json(url)

    wheelchair_boarding_station = closest_station_json['data'][0]['attribute']['name'],closest_station_json['data'][0]['attribute']['wheelchair_boarding']

    return wheelchair_boarding_station

def main():
    location_name = "Babson College"
    print(extract_latLng(location_name))

    lat = str(extract_latLng(location_name)[0])
    lng = str(extract_latLng(location_name)[1])

    print(extract_closest_station(lat, lng))

if __name__ == "__main__":
    main()
