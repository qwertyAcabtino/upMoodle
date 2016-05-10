from django.core.exceptions import ObjectDoesNotExist

from upmoodle.models import Level
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.jsonResponse import JsonResponse
from upmoodle.models.utils.requestException import RequestException, RequestExceptionByCode
from upmoodle.services.orm.serializers import LevelSerializer


class LevelService:

    def __init__(self):
        pass

    @staticmethod
    def __get_level_object(level_id=None):
        if not level_id:
            level = Level.objects.filter(parent=None, visible=True)
        else:
            level = Level.objects.filter(parent=level_id, visible=True)
        return LevelSerializer(level, many=True).data

    @staticmethod
    def get_tree(level_id=None):
        return LevelService.__get_tree_from_id(level_id)

    @staticmethod
    def __get_tree_from_id(level_id=None):
        level_object = LevelService.__get_level_object(level_id=level_id)

        if not level_id:
            for item in level_object:
                item['children'] = LevelService.__get_tree_from_id(item.get('id'))
            return JsonResponse(body=level_object)
        else:
            for item in level_object:
                item['children'] = LevelService.__get_tree_from_id(item.get('id'))
                if not item['children'] or len(item['children']) is 0:
                    del item['children']
            return level_object

    @staticmethod
    def get_level_children_ids_list(level_id=None):
        try:
            return LevelService.__get_ids_tree(level_id)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def __get_ids_tree(level_id=None):
        if not level_id:
            subjects = Level.objects.filter(parent=None, visible=True)
            ids = []
            for subject in subjects:
                ids.append(subject.id)
                ids.extend(LevelService.__get_ids_tree(subject.id))
            return list(set(ids))
        else:
            subjects = Level.objects.filter(parent=level_id, visible=True)
            ids = [level_id]
            for subject in subjects:
                ids.append(subject.id)
                ids.extend(LevelService.__get_ids_tree(subject.id))
            return list(set(ids))
