from common import get_model_id_of


def populate(insert):
    for name, model_id in get_model_id_of().items():
        insert([model_id, name])
