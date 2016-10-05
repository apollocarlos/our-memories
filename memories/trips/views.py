from django.shortcuts import render

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geoposition import Geoposition
from geopy.geocoders import Nominatim
from os import walk, getcwd
import datetime
import random

from .models import Location, Photo


DEFAULT_LAT = 35.5980342
DEFAULT_LNG = 139.6002817
DEFAULT_COUNTRY = 'Japan'
DEFAULT_STATE = 'Kanagawa'
DEFAULT_CITY = 'Kawasaki'
DATA_PATH_BASE = '/static/trips/data'


def test(request):
    path_base_relative = '/static/trips/data'
    path_base_real = getcwd() + '/trips' + path_base_relative
    temp = []
    for (dirpath, dirnames, filenames) in walk(path_base_real):
        temp.extend(filenames)
    files = ['{}/{}'.format(path_base_relative, filename) for filename in temp]
    return render(request, 'trips/test.html', {'result': files})


def world_map(request):
    photo_set = Photo.objects.all()
    return render(request, 'trips/world_map.html', {'photo_set': photo_set})


def location_detail(request, location_id):
    location = Location.objects.get(id=location_id)
    return render(request, 'trips/location_detail.html', {'location': location})


def photo_add(request):
    path_base_relative = DATA_PATH_BASE
    path_base_real = getcwd() + '/trips' + path_base_relative
    temp = []
    for (dirpath, dirnames, filenames) in walk(path_base_real):
        temp.extend(filenames)
    files = ['{}/{}'.format(path_base_relative, filename) for filename in temp]
    files_real = ['{}/{}'.format(path_base_real, filename) for filename in temp]

    geolocator = Nominatim()
    for path, path_real in zip(files, files_real):
        img = Image.open(path_real)
        exif = get_exif_data(img)

        datetime_original = exif["DateTimeOriginal"]
        datetime_fixed = datetime.datetime.strptime(datetime_original, "%Y:%m:%d %H:%M:%S")

        lat_lng = get_lat_lng(exif)
        location = geolocator.reverse("%s, %s" % (lat_lng[0], lat_lng[1]))
        address = location.raw['address']
        country = address['country'] if 'country' in address else DEFAULT_COUNTRY
        state = address['state'] if 'state' in address else DEFAULT_STATE
        city = address['city'] if 'city' in address else DEFAULT_CITY

        loc, res_loc = Location.objects.get_or_create(
            country=country,
            state=state,
            city=city
        )
        ph, res_ph = Photo.objects.get_or_create(
            location=loc,
            lat_lng=Geoposition(lat_lng[0], lat_lng[1]),
            file_path=path,
            file_path_real=path_real,
            date_time=datetime_fixed
        )

    return render(request, 'trips/photo_add.html')


# utils below

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lng(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data"""
    r = random.uniform(-0.0001, 0.0001)
    lat = DEFAULT_LAT + r
    lng = DEFAULT_LNG + r

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lng = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lng = 0 - lng

    return lat, lng
