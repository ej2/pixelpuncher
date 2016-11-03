from chatterbot.trainers import ListTrainer
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import npc_says
from pixelpuncher.location.models import Location
from pixelpuncher.npc.models import NPC
from pixelpuncher.npc.utils.actions import punch_npc
from pixelpuncher.npc.utils.conversation import get_response, parse_trigger_text, response_reward, get_npc_greeting
from pixelpuncher.npc.utils.relationships import get_relationship
from pixelpuncher.player.decorators import player_required



@login_required
@player_required
def punch(request, player, location_id, npc_id):
    npc = get_object_or_404(NPC, id=npc_id)
    punch_npc(player, npc)

    add_game_message(player, "You punch {} in the face!".format(npc.name))

    return redirect("location:visit", location_id)


@login_required
@player_required
def talk(request, player, location_id, npc_id):
    location = get_object_or_404(Location, pk=location_id)
    npc = get_object_or_404(NPC, id=npc_id)
    relationship = get_relationship(player, npc)

    if request.method == "POST":
        player_input = request.POST["playerinput"]

        trigger, text = parse_trigger_text(player_input)
        response = get_response(player, npc, text, trigger)

        if response:
            response_reward(response, player, npc)
            add_game_message(player, npc_says(npc, response.text))
        else:
            add_game_message(player, "{} does not respond.".format(npc.name))
    else:
        add_game_message(player, get_npc_greeting(npc))

    context = {
        "user": player.user,
        "player": player,
        "npc": npc,
        "relationship": relationship,
        "location": location,
    }

    return TemplateResponse(
        request, "game/talk.html", RequestContext(request, context))


@login_required
@player_required
def talk_json(request, player, location_id):
    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST' and request.is_ajax():
        input_text = request.POST.get('talktext')

        trigger, text = parse_trigger_text(input_text)
        response = get_response(player, location.npc, text, trigger)

        #response_reward(response, player)

        return JsonResponse({'message': response.text})
    else:
        return JsonResponse({'message': 'test'})


# def lat_ajax(request):
#
#     if request.method == 'POST' and request.is_ajax():
#         name = request.POST.get('name')
#         return HttpResponse(json.dumps({'name': name}), content_type="application/json")
#     else :
#         return render_to_response('ajax_test.html', locals())



@login_required
@player_required
def chatter(request, player, location_id, npc_id):
    location = get_object_or_404(Location, pk=location_id)
    npc = get_object_or_404(NPC, id=npc_id)
    relationship = get_relationship(player, npc)

    from chatterbot import ChatBot
    chatbot = ChatBot(npc.name, read_only=True,
        storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
        database='chatterbot-database',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    if request.method == "POST":
        player_input = request.POST["playerinput"]

        response = chatbot.get_response(player_input)
        add_game_message(player, '{} says {}'.format(npc.name, response.text))

    else:
        response = chatbot.get_response("Good morning!")
        add_game_message(player, npc_says(npc, response.text))

    context = {
        "user": player.user,
        "player": player,
        "npc": npc,
        "relationship": relationship,
        "location": location,
    }

    return TemplateResponse(
        request, "game/talk.html", RequestContext(request, context))


@login_required
@player_required
def train(request, player, location_id, npc_id):
    location = get_object_or_404(Location, pk=location_id)
    npc = get_object_or_404(NPC, id=npc_id)
    relationship = get_relationship(player, npc)

    from chatterbot import ChatBot

    chatbot = ChatBot(
        npc.name,  # read_only=True,
        storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
        database='chatterbot-database',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    import os
    from django.conf import settings

    fname = os.path.join(settings.ROOT_DIR.__str__(), 'roommate.corpus.json')

    with open(fname) as f:
        content = f.readlines()

    chatbot.set_trainer(ListTrainer)
    chatbot.train(content)

    #chatbot.train("chatterbot.corpus.english")

    if request.method == "POST":
        player_input = request.POST["playerinput"]

        response = chatbot.get_response(player_input)
        add_game_message(player, npc_says(npc, response.text))

    else:
        response = chatbot.get_response("Good morning!")

        add_game_message(player, npc_says(npc, response.text))

    context = {
        "user": player.user,
        "player": player,
        "npc": npc,
        "relationship": relationship,
        "location": location,
    }

    return TemplateResponse(
        request, "game/talk.html", RequestContext(request, context))
