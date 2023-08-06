"""Search logic for Simple Search."""
from simplesearch import db_helper


def search_simple_index(values):
    """Search documents that contains any of the values, ordered
    by number of matches.
    """
    db = db_helper.SimpleIndexDB()
    location_count = {}
    for value in values:
        locations = db.get_locations_list(value)
        for location in locations:
            if location_count.get(location) is None:
                location_count[location] = 0
            location_count[location] += 1

    ordered_locations = sorted(
        location_count, key=lambda x: location_count[x], reverse=True)
    return ordered_locations
