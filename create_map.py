import argparse
import sys

from staticmap import StaticMap, CircleMarker
from geopy.geocoders import Nominatim
from pprint import pprint

url_template = 'http://a.tile.osm.org/{z}/{x}/{y}.png'

def main(argv):
    parser = argparse.ArgumentParser(
        prog='create_map',
    )

    arg_group = parser.add_argument_group('Arguments')
    arg_group.add_argument('--verbose', '-v', action='count', help='Set verbose output', default=0)
    arg_group.add_argument('-i', help="Address List Table (address.lst)", type=str, dest="infile", default='address.lst')
    arg_group.add_argument('-o', help="PNG file to create (marker.png)", type=str, dest="outfile", default='marker.png')
    arg_group.add_argument('-n', help="Your/Company Name (default)", type=str, dest="name", default='default')
    arg_group.add_argument("--img_w", help="Width of the output image (400)", type=int, dest="width", default=400)
    arg_group.add_argument("--img_h", help="Height of the output image (400)", type=int, dest="height", default=400)
    arg_group.add_argument('-z', help="Image Zoom factor (10)", type=int, dest="zoom", default=10)

    args = parser.parse_args(argv)

    home_lat = 47.412279
    home_lon = -122.692318

    m = StaticMap(width=args.width, height=args.height, url_template=url_template)
    m.add_marker(CircleMarker((home_lon, home_lat), 'blue', 12))
    with open(args.infile) as f:
        lines = f.readlines()
        geolocator = Nominatim(user_agent=args.name)
        pprint(lines)
        for line in lines:
            parts = line.strip().split(':')
            address = parts[0]
            color = parts[1] if len(parts) > 1 else 'blue'
            cm_w = int(parts[2]) if len(parts) > 2 else 12
            pprint([address, color, cm_w])
            location = geolocator.geocode(address)
            pprint(location)
            m.add_marker(CircleMarker((location.longitude, location.latitude), color, cm_w))

    image = m.render(zoom=args.zoom)
    image.save('marker.png')

if __name__ == '__main__':
    main(sys.argv[1:])