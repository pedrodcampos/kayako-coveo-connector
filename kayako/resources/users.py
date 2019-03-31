from kayako.core.endpoint import KayakoEndpoint
from kayako.core.requests import KayakoRequests
from kayako.resources.users_filters import FilterCollections, FilterPredicate, FilterProposition


class KayakoUsers(KayakoEndpoint):

    __resource_endpoint__ = 'users'
    __filters_endoint__ = 'filter'
    __fields_endpoint__ = 'fields'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    @property
    def fields(self):
        return self.__get_fields()

    def __get_fields(self):
        url = self._build_url(self.__fields_endpoint__)
        params = {'fields': 'key,options(values(translation))',
                  'include': 'field_option, locale_field'}
        fields = self._requests.get(url, params=params)
        mapped_fields = {field['key']: {'id': field['id'],
                                        'options': field['options']}
                         for field in fields}
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

    def get_by_role(self, role, fields=None, include=None):
        params = self._bulk_build_params(locals())
        url = self._build_url()
        return self._requests.get(url, params=params)

    def get(self, id: int = None, fields: list = None, include: list = None):
        params = self._bulk_build_params(locals(), ['id'])
        url = self._build_url(id or '')
        return self._requests.get(url, params)

    def get_many(self, ids: list = None, fields: list = None, include: list = None):
        params = self._bulk_build_params(locals())
        if type(ids) == list:
            params.update = {'ids': ','.join(ids)}
        url = self._build_url()
        return self._requests.get(url, params)

    def filter(self, predicate_operator, collections_operator, filter_predicates, fields: list = None, include: list = None):
        params = self._bulk_build_params(
            locals(), ['predicate_operator', 'collections_operator', 'filter_predicates'])

        col = FilterCollections(collections_operator)
        col.propositions = filter_predicates
        filter_predicates = FilterPredicate(predicate_operator, [col])

        data = filter_predicates.json()

        url = self._build_url(self.__filters_endoint__)
        response = self._requests.post(url, data, params)
        return response

    def update(self, id, json={}):
        url = self._build_url(id)
        return self._requests.put(url, json=json)

    def cases(self, agent_id: int = None, status=None, priority=None,
              tags: list = None, fields=None, include=None):

        params = self._bulk_build_params(locals(), ['agent_id'])
        url = self._build_url(agent_id, 'cases')
        return self._requests.get(url, params)
