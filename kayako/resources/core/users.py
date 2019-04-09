from kayako.api import KayakoAPIController, KayakoRequests, extract_params
import json


class FilterPredicate():
    def __init__(self, operator, collections):
        self.collection_operator = operator
        self.collections = collections

    def json(self):
        json_str = json.dumps({"predicates": self},
                              default=lambda obj: obj.__dict__)
        return json.loads(json_str)


class FilterCollections():
    def __init__(self, operator, propositions=list()):
        self.proposition_operator = operator
        self.propositions = propositions


class FilterProposition():
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value


class KayakoUsers():

    __resource_name__ = 'users'
    __filters_endoint__ = 'filter'
    __fields_endpoint__ = 'fields'

    def __init__(self, requests: KayakoRequests):
        self.__api = KayakoAPIController(self.__resource_name__, requests)

    @property
    def fields(self):
        return self.__get_fields()

    def __get_fields(self):

        params = {'fields': 'key,options(values(translation))',
                  'include': 'field_option, locale_field'}

        fields = self.__api.get(self.__fields_endpoint__, params=params)

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
        return self.__api.get(role=role, fields=fields, include=include)

    def get(self, id: int = None, fields: list = None, include: list = None):
        params = extract_params(locals(), ignore_keys=['id'])
        return self.__api.get(id, params=params)

    def get_many(self, ids: list = None, fields: list = None, include: list = None):
        params = extract_params(locals())
        return self.__api.get(params=params)

    def filter(self, predicate_operator, collections_operator, filter_predicates, fields: list = None, include: list = None):
        params = extract_params(locals(), ignore_keys=[
                                'predicate_operator', 'collections_operator', 'filter_predicates'])
        col = FilterCollections(collections_operator)
        col.propositions = filter_predicates
        filter_predicates = FilterPredicate(predicate_operator, [col])

        data = filter_predicates.json()
        return self.__api.post(self.__filters_endoint__, data=data, params=params)

    def update(self, id, payload={}):
        return self.__api.put(id, json=payload)

    def cases(self, agent_id: int = None, status=None, priority=None,
              tags: list = None, fields=None, include=None):
        params = extract_params(locals(), ignore_keys=['agent_id'])
        return self.__api.get(agent_id, 'cases', params=params)
