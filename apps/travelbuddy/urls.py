from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^schedule$', views.schedule, name='schedule'),
    url(r'^createTrip$', views.createTrip, name='createTrip'),
    url(r'^show/(?P<id>\d+)$', views.show, name='reveal'),
    url(r'^join/(?P<id>\d+)$', views.join, name='joinTrip')
]