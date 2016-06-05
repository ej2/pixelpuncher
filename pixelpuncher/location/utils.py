from pixelpuncher.location.models import Location


def assign_starting_locations(player):
    locations = Location.objects.filter(starting_location=True)

    for location in locations.all():
        unlock_location(player, location)


def unlock_location(player, location):
    location.players.add(player)
    location.save()

