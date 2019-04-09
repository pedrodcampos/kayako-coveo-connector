from kayako.api import KayakoAPIController, KayakoRequests, extract_params


class KayakoCases():

    __resource_name__ = 'cases'
    __fields_endpoint__ = 'fields'

    def __init__(self, requests: KayakoRequests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)

    @property
    def fields(self):
        return self.__get_fields()

    def __get_fields(self):
        params = {'fields': 'is_system,key,options(values(translation))',
                  'include': 'field_option, locale_field'}
        fields = self.__api.get(self.__fields_endpoint__, params=params)

        mapped_fields = {field['key']: {'id': field['id'],
                                        'options': field['options']}
                         for field in fields if not field['is_system']}

        for _, field in mapped_fields.items():
            if field['options'] == []:
                field['options'] = {}
            else:
                options = field['options']
                field['options'] = {}
                for option in options:
                    field['options'].update(
                        {option['id']: option['values'][0]['translation']})

        return mapped_fields

    def get(self, id: int = None, status=None, priority=None,
            tags: list = None, fields=None, include=None):

        params = extract_params(locals(), ['id'])
        return self.__api.get(id, params=params)

    def update(self, id: int, subject=None, requester_id=None, assigned_team_id=None,
               brand_id=None, assigned_agent_id=None, status_id=None, priority_id=None,
               type_id=None, form_id=None, tags=None):

        data = extract_params(locals(), ['id'])

        return self.__api.requests.put(id, json=data)

    def update_many(self, ids: list, subject=None, requester_id=None, assigned_team_id=None,
                    brand_id=None, assigned_agent_id=None, status_id=None, priority_id=None,
                    type_id=None, form_id=None, tags=None):

        data = extract_params(locals(), ['ids'])
        params = {'ids': ','.join(map(str, ids))}
        return self.__api.requests.put(json=data, params=params)
