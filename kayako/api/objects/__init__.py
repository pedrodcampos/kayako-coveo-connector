 
class KayakoObject():

    def __init__(self, kwargs:dict = None, auto_parse=True):
        self.__kwargs__ = kwargs
        if auto_parse:
            self._parse()

    def _parse(self):
        if self.__kwargs__:
            self.__json_injector(self.__kwargs__)
        del self.__kwargs__
    
    def __json_injector(self,kwarg: dict):
        def from_json(target, json_value):
            for key, value in json_value.items():
                if type(value) == dict:
                    new_class_name = f'Kayako{key.capitalize()}'
                    new_obj = type(new_class_name,(KayakoObject,),value)
                    setattr(target, key,new_obj )
                else:
                    setattr(target, key, value)
        from_json(self, kwarg)

    def __repr__(self):
        def do_translate(obj):
            lst_repr = []
            attrs = obj.__dict__.items()
            for key,value in attrs:
                if '__' not in key:
                    if isinstance(value, type):
                        if issubclass(value, self.__class__.__base__):
                            s = f'"{key}" : {do_translate(value)}'
                    else:
                        s = f'"{key}" : "{value}"'
                    lst_repr.append(s)
            return "{" + ", ".join(lst_repr)+"}"
        return do_translate(self)