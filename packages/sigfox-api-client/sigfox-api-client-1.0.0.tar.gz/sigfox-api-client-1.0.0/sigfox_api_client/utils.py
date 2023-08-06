import re

def _convert(s):
    a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
    return a.sub(r'_\1', s).lower()

def _convertArray(a):
    newArr = []
    for i in a:
        if isinstance(i,list):
            newArr.append(_convertArray(i))
        elif isinstance(i, dict):
            newArr.append(_convertJSON(i))
        else:
            newArr.append(i)
    return newArr

def _convertJSON(j):
    out = {}
    for k in j:
        newK = _convert(k)
        if isinstance(j[k],dict):
            out[newK] = _convertJSON(j[k])
        elif isinstance(j[k],list):
            out[newK] = _convertArray(j[k])
        else:
            out[newK] = j[k]
    return out

def ConvertToModel(data, model_type):
    result = {}
    data = _convertJSON(data)
    for key in data.keys():
        if key in model_type.attribute_map.keys():
            result.update({key:data[key]})
    return model_type(**result)

def ConvertToListOfModels(response, model_type):
    data = response['data']
    result = []
    for mod in data:
        result.append(ConvertToModel(mod, model_type))
    return result