from types import SimpleNamespace


class KayakoParser(SimpleNamespace):
    def __init__(self, kwarg: dict):
        def from_json(target, json_value):
            for key, value in json_value.items():
                if type(value) == dict:
                    setattr(target, key, SimpleNamespace())
                    child = getattr(target, key)
                    from_json(child, value)
                else:
                    setattr(target, key, value)
        from_json(self, kwarg)
