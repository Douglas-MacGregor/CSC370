from common import get_regions


def populate(insert):
    for region_id, name, country in get_regions():
        insert([region_id, name, country])
