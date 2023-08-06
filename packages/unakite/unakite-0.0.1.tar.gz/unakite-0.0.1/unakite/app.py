from unakite import handlers
from firenado import tornadoweb


class UnakiteComponent(tornadoweb.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/', handlers.IndexHandler),
        ]
