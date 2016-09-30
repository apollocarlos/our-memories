from django.shortcuts import render

from .models import Location


def world_map(request):
    locations = Location.objects.order_by('name')
    return render(request, 'trips/world_map.html', {'locations': locations})


def location_detail(request, location_name):
    location = Location.objects.get(name='location_name')
    return render(request, 'trips/location_detail.html', {'location': location})
