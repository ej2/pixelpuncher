


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
    pass


    # Possible outcomes:
    #  Grant temporary discount
    #  Raise prices
    #  Increase/Decrease relationship
    #  change status - Friend/Enemy/Business/Stranger/Best Friend/Nemesis
