import factory
from factory.django import DjangoModelFactory

from pixelpuncher.location.models import Location


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    name = "Test Location"
    description = "Description"
    active = True
    location_type = "SHP"
    starting_location = True
