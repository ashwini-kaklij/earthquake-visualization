"""
This is a utility class used as factory to perform repetitive operations to avoid code duplication.
"""


def get_day_slot(hour):
    if hour < 5:
        return 'Night'
    elif hour > 5 and hour < 12:
        return 'Morning'
    elif hour > 12 and hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

