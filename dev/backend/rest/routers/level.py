from rest.controllers.requests import authenticated, method
from rest.services.level import LevelService, SubjectService


@authenticated
@method('GET')
def level_tree(request):
    return LevelService.get_tree()


@authenticated
@method('GET')
def subject_files_list(request, pk):
    return SubjectService.get_files_list(pk)
