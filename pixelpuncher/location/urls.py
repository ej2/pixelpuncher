from django.conf.urls import url

from pixelpuncher.location import views

urlpatterns = [
    url(r'^visit/(?P<location_id>[\w.@+-]+)/$', views.visit_location, name="visit"),
    url(r'^visit/(?P<location_id>[\w.@+-]+)/purchase/(?P<locationitem_id>[\w.@+-]+)$', views.purchase, name="purchase"),
]
