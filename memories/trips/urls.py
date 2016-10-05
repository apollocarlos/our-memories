from django.conf.urls import url

from . import views


app_name = 'trips'
urlpatterns = [
    url(r'^$', views.world_map, name='world_map'),
    url(r'^(?P<location_id>[0-9]+)/$', views.location_detail, name='location_detail'),
    url(r'^photo/add/$', views.photo_add, name='photo_add'),
    url(r'^test/$', views.test, name='test'),
]
