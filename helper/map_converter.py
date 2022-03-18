from geopy.geocoders import Nominatim

def AddressToLagLong(address):
    locator = Nominatim(user_agent="map_converter")
    location = locator.geocode("Avenida Bartholomeu de Gusmão, 114")
    return location