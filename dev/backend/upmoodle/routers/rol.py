from upmoodle.routers.decorators.routing_decorators import authenticated, method, response
from upmoodle.services.rol import RolService


@authenticated
@method('GET')
@response(media_type='application/json')
def roles_list(request, **kwargs):
    return RolService.get_roles_list()
