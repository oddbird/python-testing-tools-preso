def get_level(min_grade, max_grade):
    if max_grade <= 6:
        return 'elementary'
    if min_grade > 6:
        return 'secondary'
    return None
