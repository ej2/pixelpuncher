from annoying.functions import get_object_or_None

from pixelpuncher.game.utils.game_settings import RELATIONSHIP_GOOD_POINTS, \
    RELATIONSHIP_BEST_POINTS, RELATIONSHIP_BAD_POINTS, RELATIONSHIP_HORRIBLE_POINTS
from pixelpuncher.npc.models import NPCRelationship, RelationshipLevels


def adjust_relationship_score(relationship, score):
    relationship.score += score

    if relationship.score > RELATIONSHIP_BEST_POINTS:
        relationship.relationship_level = RelationshipLevels.BEST
    elif relationship.score > RELATIONSHIP_GOOD_POINTS:
        relationship.relationship_level = RelationshipLevels.GOOD
    elif relationship.score < RELATIONSHIP_HORRIBLE_POINTS:
        relationship.relationship_level = RelationshipLevels.HORRIBLE
    elif relationship.score < RELATIONSHIP_BAD_POINTS:
        relationship.relationship_level = RelationshipLevels.BAD
    else:
        relationship.relationship_level = RelationshipLevels.NETURAL

    relationship.save()


def create_relationship(player, npc):
    relationship = NPCRelationship(player=player, npc=npc, relationship_type=npc.default_relationship_type)
    relationship.current_energy = npc.total_energy
    relationship.current_health = npc.total_health
    relationship.avatar = npc.avatar
    relationship.score = 0
    relationship.save()

    return relationship


def get_relationship(player, npc):
    relationship = get_object_or_None(NPCRelationship, player=player, npc=npc)

    if relationship is None:
        relationship = create_relationship(player, npc)

    return relationship
