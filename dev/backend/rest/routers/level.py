from rest.routers.decorators.routing_decorators import authenticated, method
from rest.services.level import LevelService, SubjectService


@authenticated
@method('GET')
def level_tree(request, **kwargs):
    return LevelService.get_tree()


@authenticated
@method('GET')
def subject_files_list(request, pk, **kwargs):
    return SubjectService.get_files_list(pk)
