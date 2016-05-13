from upmoodle.controllers.decorators.exceptions import map_exceptions
from upmoodle.models import Rol


class RolService:

    def __init__(self):
        pass

    @staticmethod
    @map_exceptions
    def get_roles_list():
        return Rol.objects.all()
