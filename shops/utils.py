LAST_NAME_PART = 0
FIRST_NAME_PART = 1
MIDDLE_NAME_PART = 2


def get_full_name_part(full_name, part):
    if isinstance(full_name, str):
        parts = full_name.split(" ")
        try:
            return parts[part]
        except IndexError:
            return ""

    return ""
