from geopy.geocoders import HereV7

def AddressToLagLong(address):
    locator = HereV7(apikey="mQ3A_-TTvCNNwH5OZ9S6PkImzlx2K1UPQQU3V_ko8kQ",user_agent="map_converter")
    location = locator.geocode(address+', Santos')
    return location