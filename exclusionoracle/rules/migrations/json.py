import json


def success(obj):
    return json.dumps({
        'status': 'success',
        'message': 'ok',
        'result': obj,
    })


def error(message, obj):
    result = {
        'status': 'error',
        'message': message,
    }
    if obj is not None:
        result['result'] = obj
    return json.dumps(result)
