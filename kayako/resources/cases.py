from kayako.core.endpoint import KayakoEndpoint
from kayako.core.requests import KayakoRequests


class KayakoCases(KayakoEndpoint):

    __resource_endpoint__ = 'cases'
    __fields_endpoint__ = 'fields'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    @property
    def fields(self):
        return self.__get_fields()

    def __get_fields(self):
        url = self._build_url(self.__fields_endpoint__)
        params = {'fields': 'is_system,key,options(values(translation))',
                  'include': 'field_option, locale_field'}
        fields = self._requests.get(url, params=params)
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

        params = self._bulk_build_params(locals(), ['id'])
        url = self._build_url(id)
        return self._requests.get(url, params)

    def update(self, id: int, subject=None, requester_id=None, assigned_team_id=None,
               brand_id=None, assigned_agent_id=None, status_id=None, priority_id=None,
               type_id=None, form_id=None, tags=None):

        data = self._bulk_build_params(locals(), ['id'])
        url = self._build_url(id)
        return self._requests.put(url, json=data)

    def update_many(self, ids: list, subject=None, requester_id=None, assigned_team_id=None,
                    brand_id=None, assigned_agent_id=None, status_id=None, priority_id=None,
                    type_id=None, form_id=None, tags=None):

        data = self._bulk_build_params(locals(), ['id'])
        params = {'ids': ','.join(map(str, ids))}
        url = self._build_url()
        return self._requests.put(url, json=data, params=params)
