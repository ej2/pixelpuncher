from django.conf.urls import url

from pixelpuncher.item.views import container

urlpatterns = [
    url(r'^(?P<container_id>[\w.@+-]+)$', container.open_container, name="open"),
    url(r'^take/(?P<item_id>[\w.@+-]+)$', container.take_item, name="take"),
    url(r'^discard/(?P<item_id>[\w.@+-]+)$', container.discard_item, name="discard"),
]
