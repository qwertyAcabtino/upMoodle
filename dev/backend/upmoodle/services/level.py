from django.core.exceptions import ObjectDoesNotExist

from upmoodle.models import Level
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage


class LevelService:

    def __init__(self):
        pass

    @staticmethod
    def __get_level_json_object(level_id=None):
        levels = Level.objects.filter(parent=level_id, visible=True).order_by('name')
        return Level.get_flatten_object(data=levels, collection=True)

    @staticmethod
    def get_tree(level_id=None):
        return LevelService.__get_tree_from_id(level_id)

    @staticmethod
    def __get_tree_from_id(level_id=None):
        level_json = LevelService.__get_level_json_object(level_id=level_id)

        if not level_id:
            for item in level_json:
                item['children'] = LevelService.__get_tree_from_id(item.get('id'))
            return level_json
        else:
            for item in level_json:
                item['children'] = LevelService.__get_tree_from_id(item.get('id'))
                if not item['children'] or len(item['children']) is 0:
                    del item['children']
            return level_json

    @staticmethod
    def get_level_children_ids_list(level_id=None):
        try:
            return LevelService.__get_ids_tree(level_id)
        except ObjectDoesNotExist or OverflowError or ValueError:
            raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA)

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

    @staticmethod
    def __get_child_parents(level_id=None):
        if not level_id:
            return None
        else:
            parent_id = Level.objects.get(id=level_id).parent_id
            ids = []
            if parent_id:
                ids = LevelService.__get_child_parents(parent_id)
                ids.append(parent_id)
            return ids

    @staticmethod
    def get_ids_tree_from_childrens(subjects=None):
        ids = []
        for subject in subjects:
            ids.append(subject.id)
            ids.extend(LevelService.__get_child_parents(subject.id))
        return tuple(ids)
