import random


def perform_npc_action(player, npc, action):
    result = ""

    if action == 'punch':
        result = punch_npc(player, npc)
    elif action == 'high-five':
        pass
    else:
        pass

    return result


def punch_npc(player, npc):
    return "You punch {} in the face".format(npc.name)

    result = random.randint()

    if result == 0:
        # discount
        pass

    elif result == 1:
        # increase prices
        pass
    elif result == 2:
        # relationship
        pass
    elif result == 3:
        #
        pass

    # RELATIONSHIP_TYPE = (
    #     ('RIVL', 'Rival',),
    #     ('FRND', 'Friend',),
    #     ('CUST', 'Customer',),
    #     ('ROMC', 'Romantic',),
    # )
    #
    # RELATIONSHIP_LEVEL = (
    #     ('BS', 'Best',),
    #     ('GD', 'Good',),
    #     ('NT', 'Netural',),
    #     ('BD', 'Bad',),
    #     ('HR', 'Horrible',),
    # )
    #



        # Possible outcomes:
    #  Grant temporary discount
    #  Raise prices
    #  Increase/Decrease relationship
    #  change status - Friend/Enemy/Business/Stranger/Best Friend/Nemesis
