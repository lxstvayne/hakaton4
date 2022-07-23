from . import parse
from . import fill_test_data


def fill_all():
    parse.fill_db()
    parse.parse_complexes_ratings()
    fill_test_data.create_random_clients()
    fill_test_data.fill_commercial_rooms()
