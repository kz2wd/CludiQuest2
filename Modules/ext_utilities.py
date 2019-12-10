def check_presence(value, list_to_check):
    presence = False
    for element in list_to_check:
        if value == element:
            presence = True

    return presence


def divide_to_superior(value, divisor):
    value = int(value / divisor) + 1
    return value


def cycle(value, value_max):
    if value > value_max:
        value -= value_max
    return value
