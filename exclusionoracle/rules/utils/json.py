import json

from django.http import HttpResponse


def success(obj):
    return HttpResponse(json.dumps({
        'status': 'success',
        'message': 'ok',
        'result': obj,
    }), content_type='application/json')


def error(message, obj):
    result = {
        'status': 'error',
        'message': message,
    }
    if obj is not None:
        result['result'] = obj
    return HttpResponse(json.dumps(result),
                        content_type='application/json')
