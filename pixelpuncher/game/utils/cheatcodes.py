from annoying.functions import get_object_or_None
from pixelpuncher.game.models import CheatCode


class Cheats(object):
    DAILY_RESET = 'daily'


class CheatDailyReset(object):
    def cheat(self):
        return "it worked!"


def add_cheatcode(player, code):
    cheat_code = get_object_or_None(CheatCode, code=code)

    if cheat_code:
        if player not in cheat_code.players.all():
            cheat_code.players.add(player)
            cheat_code.save()

            return True

    return False


def do_cheat(player, cheatcode):
    cheat_class = globals()[cheatcode.cheat_class]()
    message = cheat_class.cheat()

    return message


def cheat_daily_reset():
    pass
#
#
# def process_event(request_log):
#     """
#     Calls event handler based on request_log topic
#     :param request_log:
#     :return:
#     """
#     events = {
#         WebHookEventType.CUSTOMER_CREATED: customer_created_event,
#         WebHookEventType.CUSTOMER_VERIFIED: customer_verified_event,
#         WebHookEventType.CUSTOMER_SUSPENDED: customer_suspended_event,
#         WebHookEventType.CUSTOMER_VERIFICATION_DOCUMENT_NEEDED: customer_verification_document_needed_event,
#         WebHookEventType.CUSTOMER_VERIFICATION_DOCUMENT_UPLOADED: customer_verification_document_uploaded_event,
#         WebHookEventType.CUSTOMER_VERIFICATION_DOCUMENT_FAILED: customer_verification_document_failed_event,
#         WebHookEventType.CUSTOMER_VERIFICATION_DOCUMENT_APPROVED: customer_verification_document_approved_event,
#         WebHookEventType.FUNDING_SOURCE_ADDED: funding_source_added_event,
#         WebHookEventType.FUNDING_SOURCE_VERIFIED: funding_source_verified_event,
#         WebHookEventType.FUNDING_SOURCE_REMOVED: funding_source_removed_event,
#         WebHookEventType.TRANSFER_CREATED: transfer_created_event,
#         WebHookEventType.TRANSFER_COMPLETED: transfer_completed_event,
#         WebHookEventType.TRANSFER_FAILED: transfer_failed_event,
#         WebHookEventType.CUSTOMER_TRANSFER_CANCELLED: customer_transfer_cancelled,
#     }
#
#     events.get(request_log.topic, unhandled_event)(request_log)
