def get_dict(obj):
    if hasattr(obj, '__dict__'):
        odict = get_dict_obj(obj)
    elif type(obj) is dict:
        odict = get_dict_dict(obj)
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


def get_dict_dict(obj):
    dict_dict = {}
    attributes = obj.keys()
    for a in attributes:
        value = obj[a]
        if hasattr(value, '__dict__'):
            dict_dict[a] = get_dict_obj(value)
        elif type(value) is dict:
            dict_dict[a] = get_dict_dict(value)
        elif type(value) is list:
            dict_dict[a] = get_dict_list(value)
        else:
            dict_dict[a] = value
    return dict_dict


def get_dict_list(obj):
    list_dict = []
    for l in obj:
        if hasattr(l, '__dict__'):
            list_dict.append(get_dict_obj(l))
        elif type(l) is dict:
            list_dict.append(get_dict_dict(l))
        elif type(l) is list:
            list_dict.append(get_dict_list(l))
        else:
            list_dict.append(l)
    return list_dict