from django.conf.urls import url

from pixelpuncher.location import views

urlpatterns = [
    url(r'^visit/(?P<location_id>[\w.@+-]+)/$', views.visit_location, name="visit"),
]
