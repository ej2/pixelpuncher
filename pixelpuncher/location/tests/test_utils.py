from unittest import TestCase

from pixelpuncher.location.factories import LocationFactory
from pixelpuncher.location.utils import assign_starting_locations, unlock_location


class LocationUtilsTest(TestCase):
    def setUp(self):
        self.location = LocationFactory()

    def test_assign_starting_locations(self):

        pass
        #assign_starting_locations(player)


    def test_unlock_location(self):
        pass

        #unlock_location(player, location)

