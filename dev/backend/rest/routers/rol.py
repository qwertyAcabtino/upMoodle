from rest.controllers.requests import authenticated, method
from rest.services.rol import RolService


@authenticated
@method('GET')
def roles_list(request):
    return RolService.get_roles_list()
