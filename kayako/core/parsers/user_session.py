from kayako.core.parser import KayakoParser


class KayakoUserSession(KayakoParser):
    def __init__(self, kwarg: dict):
        super().__init__(kwarg)
