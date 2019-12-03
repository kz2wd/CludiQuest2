def check_presence(value, list_to_check):
    presence = False
    for element in list_to_check:
        if value == element:
            presence = True

    return presence
