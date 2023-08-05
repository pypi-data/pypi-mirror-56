def check_interval(value: str):
    if not value:
        return True

    parts = value.split(',')
    if len(parts) != 2:
        return False

    left = int(parts[0])
    right = int(parts[1])

    if left != '' and right != '' and left > right:
        return False

    return True
