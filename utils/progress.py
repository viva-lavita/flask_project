
def progress(user):
    count = 0
    count_values = 0
    for attr, value in vars(user).items():
        count_values += 1
        if value != '--':
            count += 1
    return int(count * 100 / count_values)
