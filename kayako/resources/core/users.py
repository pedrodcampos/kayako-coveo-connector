from kayako.api.endpoint import KayakoEndpoint
from kayako.api.requests import KayakoRequests
import json

class FilterPredicate(object):
    def __init__(self, operator, collections):
        self.collection_operator = operator
        self.collections = collections

    def json(self):
        json_str = json.dumps({"predicates": self},
                              default=lambda obj: obj.__dict__)
        return json.loads(json_str)


class FilterCollections(object):
    def __init__(self, operator, propositions=list()):
        self.proposition_operator = operator
        self.propositions = propositions


class FilterProposition(object):
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

class KayakoUsers(KayakoEndpoint):

    __endpoint_name__ = 'users'
    __filters_endoint__ = 'filter'
    __fields_endpoint__ = 'fields'

    def __init__(self, requests: KayakoRequests):
        super().__init__(requests)

    @property
    def fields(self):
        return self.__get_fields()

    def __get_fields(self):
        url = self.__endpoint.build_url(self.__fields_endpoint__)
        params = {'fields': 'key,options(values(translation))',
                  'include': 'field_option, locale_field'}
        fields = self.__endpoint.requests.get(url, params=params)
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
        return super().get(role=role,fields=fields, include=include)

    def get(self, id: int = None, fields: list = None, include: list = None):
        return super().get(id, fields=fields, include=include)


    def get_many(self, ids: list = None, fields: list = None, include: list = None):
        return super().get(ids=ids, fields=fields, include=include)

    def filter(self, predicate_operator, collections_operator, filter_predicates, fields: list = None, include: list = None):
        params = {}
        if fields:
            params.update({'fields':fields})
        if include:
            params.update({'include':fields})

        col = FilterCollections(collections_operator)
        col.propositions = filter_predicates
        filter_predicates = FilterPredicate(predicate_operator, [col])

        data = filter_predicates.json()
        return super().post(self.__filters_endoint__, data=data, params = params )
        

    def update(self, id, payload={}):
        return super().put(id, json=payload)


    def cases(self, agent_id: int = None, status=None, priority=None,
              tags: list = None, fields=None, include=None):
        return super().get(agent_id, 'cases',status=status, 
                            priority=priority, tags=tags, 
                            fields=fields, include=include)
        