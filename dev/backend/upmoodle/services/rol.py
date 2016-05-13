from upmoodle.models import Rol
from upmoodle.services.utils.zero_exception_decorator import zero_exceptions


class RolService:

    def __init__(self):
        pass

    @staticmethod
    @zero_exceptions
    def get_roles_list():
        return Rol.objects.all()
