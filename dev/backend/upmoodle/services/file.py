from upmoodle.models import File, Level, User, FileType, BannedHash, OkMessage
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.services.auth import AuthService
from upmoodle.services.utils.zero_exception_decorator import zero_exceptions


class FileService:

    def __init__(self):
        pass

    @staticmethod
    @zero_exceptions
    def add(session_token=None, data=None, files=None):
        uploader_id = User.objects.get(sessionToken=session_token).id
        AuthService.is_authorized_author(session_token=session_token, author_id=uploader_id, level=True)

        Level.validate_exists_level(data['subject_id'])
        Level.validate_subject_type(data['subject_id'])
        fields = ['uploader_id', 'subject_id', 'name', 'text', 'fileType_id']
        new_file = File.parse(data, fields=fields, optional=True, binary=files['file'])
        new_file.save()
        return OkMessage.Type.FILE_UPLOADED, "id"

    @staticmethod
    @zero_exceptions
    def delete(session_token=None, file_hash=None, **kwargs):
        model = File.objects.get(hash=file_hash)
        AuthService.is_authorized_author(session_token=session_token, author_id=model.uploader_id, level=True, same=False)
        model.visible = False
        model.save()
        return OkMessage.Type.FILE_REMOVED

    @staticmethod
    @zero_exceptions
    def metadata_update(session_token=None, file_hash=None, data=None):
        file_original = File.objects.get(hash=file_hash)
        AuthService.is_authorized_author(session_token=session_token, author_id=file_original.uploader_id, level=True, same=False)

        fields = ['name', 'text', 'fileType_id']
        file_updated = File.parse(data, fields=fields, optional=True)

        file_original.update(file_updated, fields)
        file_original.lastUpdater_id = User.get_signed_user_id(session_token)
        file_original.save()
        return OkMessage.Type.FILE_UPDATED

    @staticmethod
    @zero_exceptions
    def get_by_id(file_hash=None, **kwargs):
        return File.objects.get(hash=file_hash, visible=True)

    @staticmethod
    @zero_exceptions
    def get_banned_hashes():
        return BannedHash.objects.all()

    @staticmethod
    @zero_exceptions
    def get_files_by_level_id(level_id=None):
        level = Level.objects.get(id=level_id)
        if level.is_subject():
            return File.objects.filter(subject=level_id, visible=True)
        elif not level.is_subject():
            raise MessageBasedException(message_id=ErrorMessage.Type.INVALID_LEVEL)


class FileTypeService:
    def __init__(self):
        pass

    @staticmethod
    @zero_exceptions
    def get():
        return FileTypeService.__get__file_types()

    @staticmethod
    def __get__file_types():
        return FileType.objects.all()
