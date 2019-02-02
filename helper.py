def keyByRegno(list):
    result = dict()
    for item in list:
        result[item['regno']] = item
    return result
