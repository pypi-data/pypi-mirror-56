def get_dict(obj):
    if hasattr(obj, '__dict__'):
        odict = get_dict_obj(obj)
    elif type(obj) is list:
        odict = get_dict_list(obj)
    else:
        odict = obj
    return odict


def get_dict_obj(obj):
    odict = {}
    attributes = vars(obj).keys()
    for a in attributes:
        value = getattr(obj, a)
        if hasattr(value, '__dict__'):
            odict[a] = get_dict_obj(value)
        elif type(value) is list:
            odict[a] = get_dict_list(value)
        else:
            odict[a] = value
    return odict


def get_dict_list(obj):
    olist = []
    for l in obj:
        if hasattr(l, '__dict__'):
            olist.append(get_dict_obj(l))
        elif type(l) is list:
            olist.append(get_dict_list(l))
        else:
            olist.append(l)
    return olist