from rest.services.level import LevelService


def level_tree(request):
    return LevelService.get_tree(request)
