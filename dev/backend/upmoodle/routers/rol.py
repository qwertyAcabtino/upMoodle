from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import authenticated, method
from upmoodle.routers.response.factory import ResponseFactory
from upmoodle.services.rol import RolService


@zero_exceptions
@authenticated
@method('GET')
def roles_list(request, **kwargs):
    roles = RolService.get_roles_list()
    return ResponseFactory().ok().body(obj=roles).build()
