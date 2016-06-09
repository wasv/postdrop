def md5(data):
    import hashlib
    h = hashlib.md5()
    h.update(bytes(data, 'utf8'))
    return h.hexdigest()