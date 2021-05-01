from staticmap import StaticMap, CircleMarker
from geopy.geocoders import Nominatim
from pprint import pprint

geolocator = Nominatim(user_agent="Please_Edit_This_Text")

m = StaticMap(200, 200, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
home_lat = 47.412279
home_lon = -122.692318
coordinates = [(home_lon,home_lat)]
with open("address.lst") as f:
    lines = f.readlines()
    pprint(lines)
    for line in lines:
        address = line.strip()
        pprint(address)
        location = geolocator.geocode(address)
        pprint(location)
        coordinates.append((location.longitude, location.latitude))
pprint(coordinates)
for coord in coordinates:
    marker = CircleMarker(coord, '#0036FF', 12)
    m.add_marker(marker)

image = m.render(zoom=8)
image.save('marker.png')
