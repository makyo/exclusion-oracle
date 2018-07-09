from datetime import datetime
import json

from django.http import HttpResponse


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super(DateTimeEncoder, self).default(o)


def success(obj):
    return HttpResponse(json.dumps({
        'status': 'success',
        'message': 'ok',
        'result': obj,
    }, cls=DateTimeEncoder), content_type='application/json')


def error(message, obj):
    result = {
        'status': 'error',
        'message': message,
    }
    if obj is not None:
        result['result'] = obj
    return HttpResponse(json.dumps(result, cls=DateTimeEncoder),
                        content_type='application/json')
