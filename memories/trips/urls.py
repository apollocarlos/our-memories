from django.conf.urls import url

from . import views


app_name = 'trips'
urlpatterns = [
    url(r'^$', views.world_map, name='world_map'),
    url(r'^(?P<location_name>[a-zA-Z0-9_\-]+)/$', views.location_detail, name='location_detail'),
]
