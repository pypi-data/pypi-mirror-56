def check_interval(self=None, value: str=None, *args, **kwargs):
    if not value:
        return True

    parts = value.split(',')
    if len(parts) != 2:
        return False

    left = parts[0]
    right = parts[1]

    if left != '' and right != '' and len(left) > len(right):
        return False

    return True
