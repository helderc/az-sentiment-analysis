def load_key(fn):
    print('Loading API Key')
    api_lst = []
    with open(fn, 'r') as f:
        for l in f:
            if len(l) == 0: continue
            endpoint, key = l.strip().split(',')
            api_lst.append([endpoint, key])
    return api_lst
