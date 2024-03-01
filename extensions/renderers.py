from rest_framework.renderers import JSONRenderer
import json


class CustomJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and ('errors' or 'error' or 'ERROR') in data:
            return json.dumps({'metadata': data})
        elif isinstance(data, dict) and 'non_field_errors' in data:
            return json.dumps({'metadata': data})
        elif isinstance(data, dict) and 'detail' in data:
            return json.dumps({'metadata': data})
        elif isinstance(data, list) and all([isinstance(i, dict) and 'non_field_error' in i for i in data]):
            return json.dumps({
                'metadata': {
                    'errors': [i['non_field_error'] for i in data]
                }
            })
        elif isinstance(data, dict) and 'metadata' in data:
            return json.dumps(data)
        else:
            return json.dumps({
                'data': data
            })
