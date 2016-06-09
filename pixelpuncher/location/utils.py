import random

from pixelpuncher.location.models import Location


def assign_starting_locations(player):
    locations = Location.objects.filter(starting_location=True)

    for location in locations.all():
        unlock_location(player, location)


def unlock_location(player, location):
    location.players.add(player)
    location.save()


def purchase_service(player, service, price):
    if player.pixels < price:
        return "You don't have enough to purchase that."

    if price > 0:
        player.pixels -= price
        player.save()

    result = perform_service(player, service)

    return result


def perform_service(player, service):
    successful = random.randint(1, 100)
    if successful <= service.success_rate:
        amount = random.randint(service.min_amount, service.max_amount)

        if service.service_type == 'HEALMAX':
            result = player.adjust_to_max_health()
        elif service.service_type == 'RESTMAX':
            result = player.adjust_to_max_energy()
        elif service.service_type == 'HEAL':
            result = player.adjust_health(amount)
        elif service.service_type == 'REST':
            result = player.adjust_energy(amount)
        elif service.service_type == 'GMB':
            player.pixels += amount
            result = "You win {} pixels!".format(amount)

        player.save()
        return "{} {}".format(service.success_text, result)
    else:
        return service.failure_text
