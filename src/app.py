from model.model import Model
from view.view import View
from controller.controller import Controller


class Application(Model, Controller, View):
    NAME = 'SyncBooker'
    VERSION = '3.6alpha'

    def __init__(self, debug=False):
        if not debug:
            Model.__init__(self, app=self)
            Controller.__init__(self, app=self)
            View.__init__(self, app=self)
