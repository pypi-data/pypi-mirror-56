def print_dict(d: dict, indent = ''):
    print(dict_to_string(d))

def dict_to_string(d: dict, indent = '', separator = '\n'):
    ret = ''
    for key, value in d.items():
        if type(value) == dict:
            ret += '{}{}:{}'.format(indent, key, separator)
            ret += dict_to_string(value, indent=indent+'  ', separator=separator)
        else:
            ret += '{}{}: {}{}'.format(indent, key, value, separator)
    return ret

def dict_to_html(d: dict, indent = 0):
    ret = ''
    for key, value in d.items():
        if type(value) == dict:
            ret += '<p style="line-height: 1.0; text-indent: {}px"><b>{}</b>:</p>\n'.format(indent, key)
            ret += dict_to_html(value, indent=indent+40)
        else:
            ret += '<p style="line-height: 1.0; text-indent: {}px"><b>{}</b>: {}</p>\n'.format(indent, key, value)
    return ret

if __name__ == '__main__':
    d = {
        'a': 1,
        'sub': {
            'c': 3,
            'd': 4,
        },
        'b': 2,
    }
    print_dict(d)
    print(dict_to_html(d))