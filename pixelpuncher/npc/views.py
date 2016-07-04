import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from pixelpuncher.location.models import Location
from pixelpuncher.npc.utils.conversation import get_response, parse_trigger_text, response_reward


@login_required
def talk(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST' and request.is_ajax():
        input_text = request.POST.get('talktext')

        trigger, text = parse_trigger_text(input_text)
        response = get_response(location.npc, text, trigger)

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
