from rest_framework.renderers import JSONRenderer
import json


class CustomJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):

        errors = ['errors', 'error', 'ERROR', 'ERRORS']

        if isinstance(data, dict) and any([True if _ in data else False for _ in errors]):
            return json.dumps({'metadata': data})
        elif isinstance(data, dict) and 'non_field_errors' in data:
            return json.dumps({'metadata': data})
        elif isinstance(data, dict) and 'detail' in data:
            return json.dumps({'metadata': data})
        elif isinstance(data, dict) and 'metadata' in data:
            return json.dumps(data)
        elif isinstance(data, list) and all([isinstance(i, dict) and 'non_field_error' in i for i in data]):
            return json.dumps({
                'metadata': {
                    'errors': [i['non_field_error'] for i in data]
                }
            })
        else:
            return json.dumps({
                'data': data
            })
