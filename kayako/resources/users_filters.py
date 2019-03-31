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
