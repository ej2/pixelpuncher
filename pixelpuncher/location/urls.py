from django.conf.urls import url

from pixelpuncher.location import views

urlpatterns = [
    url(r'^visit/(?P<location_id>[\w.@+-]+)/$', views.visit_location, name="visit"),
    url(r'^visit/home$', views.visit_home, name="home"),
    url(r'^visit/(?P<location_id>[\w.@+-]+)/purchase/(?P<locationitem_id>[\w.@+-]+)$', views.purchase, name="purchase"),
    url(r'^visit/(?P<location_id>[\w.@+-]+)/sell/(?P<item_id>[\w.@+-]+)$', views.sell, name="sell"),
    url(r'^visit/(?P<location_id>[\w.@+-]+)/service/(?P<locationservice_id>[\w.@+-]+)$', views.service, name="service"),



]
