from upmoodle.models import User
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.message.okMessage import OkMessage
from upmoodle.services.utils.randoms import RandomStringsService
from upmoodle.services.utils.zero_exception_decorator import zero_exceptions


class UserService:
    def __init__(self):
        pass

    @staticmethod
    @zero_exceptions
    def get_me(session_token=None, **kwargs):
        return User.objects.get(sessionToken=session_token)

    @staticmethod
    @zero_exceptions
    def delete_me(session_token=None, **kwargs):
        deleting_user = User.objects.get(sessionToken=session_token)
        deleting_user.name = 'RemovedUser ' + str(deleting_user.id)
        deleting_user.nick = 'RemovedUser ' + str(deleting_user.id)
        deleting_user.email = 'deprecated+' + deleting_user.email
        deleting_user.password = RandomStringsService.random_password()
        deleting_user.profilePic = 'static/default_update_avatar_pic.jpeg'
        deleting_user.banned = True
        deleting_user.confirmedEmail = False
        deleting_user.save()
        return OkMessage.Type.USER_REMOVED

    @staticmethod
    @zero_exceptions
    def update_me(session_token=None, data=None):
        auth_user = User.objects.get(sessionToken=session_token)
        try:
            assert data['password']
            if not auth_user.password == data['oldPassword']:
                raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA)
        except KeyError:
            pass
        fields = ['nick', 'name', 'password', 'email']
        updated_user = User.parse(data, fields=fields, optional=True)
        auth_user.update(updated_user, fields)
        auth_user.save()
        return OkMessage.Type.USER_UPDATED

    @staticmethod
    @zero_exceptions
    def update_me_subjects(session_token=None, data=None):
        if data['ids']:
            subjects = data['ids']
        else:
            subjects = []
        updating_user = User.objects.get(sessionToken=session_token)
        updating_user.update_subjects(subjects)
        updating_user.save()
        return OkMessage.Type.USER_UPDATED

    @staticmethod
    @zero_exceptions
    def update_me_avatar(session_token=None, files=None):
        avatar = files['avatar']
        if "image/" not in avatar.content_type:
            raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA)
        else:
            auth_user = User.objects.get(sessionToken=session_token)
            auth_user.profilePic = avatar
            auth_user.save()
            return OkMessage.Type.USER_UPDATED

    @staticmethod
    @zero_exceptions
    def get_user_by_id(user_id=None):
        return User.objects.get(id=user_id)

    @staticmethod
    @zero_exceptions
    def get_users_by_rol(rol_id=None):
        return User.objects.filter(rol=rol_id, banned=False)
