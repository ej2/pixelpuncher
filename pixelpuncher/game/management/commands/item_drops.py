from sys import stdout

from annoying.functions import get_object_or_None
from django.core.management import BaseCommand

from pixelpuncher.item.models import ItemType, ItemDrop, DropTable


class Command(BaseCommand):
    help = "Create item drops based on item_type level_requirements"

    def handle(self, *args, **options):
        added_count = 0
        drop_tables = DropTable.objects.filter(name__startswith="Level")

        for drop_table in drop_tables:
            item_types = ItemType.objects.filter(level_requirement=drop_table.recommended_level)

            for item_type in item_types:
                drop = get_object_or_None(ItemDrop, drop_table=drop_table, item_type=item_type)

                if drop is None:
                    drop = ItemDrop()
                    drop.item_type = item_type
                    drop.drop_table = drop_table
                    drop.drop_rate = 50
                    drop.save()

                    added_count += 1

        stdout.write("\nTotal drops added {0}\n\n".format(added_count))

