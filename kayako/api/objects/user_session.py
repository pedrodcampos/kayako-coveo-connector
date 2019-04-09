from kayako.api.objects import KayakoObject


class KayakoUserSession(KayakoObject):

    def __init__(self, kwargs: dict):
        super().__init__(kwargs, False)
        self.id = None
        self.portal = None
        self.ip_address = None
        self.user_agent = None
        self.instance_id = None
        self.instance_name = None
        self.user = None
        self.status = None
        self.last_activity_at = None
        self.created_at = None
        self.resource_type = None
        super()._parse()
