"""
This is a utility class used as factory to perform repetitive operations to avoid code duplication.
"""


def get_day_slot(hour):
    if hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    else:
        return 'evening'
