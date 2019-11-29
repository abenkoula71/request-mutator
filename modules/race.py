def mutate(method, url, headers, cookies ):
    data = "[[requests]]\n\n\t"
    data = data + 'method = "' + method + '"\n\t'
    data = data + 'url = "' + url + '"\n\t'
    data = data + "cookies = [" + "".join('"{}={}",'.format(key, val) for (key, val) in cookies.items())[:-1] + "]\n\t"
    data = data + "headers = [" + "".join('"{}: {}",'.format(key, val) for (key, val) in headers.items())[:-1] + "]\n\t"
    data = data + "redirects = true"
    return data
