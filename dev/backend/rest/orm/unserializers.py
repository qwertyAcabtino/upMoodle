from rest.models import User


def get_value(form, key):
    try:
        return form[key]
    except KeyError as k:
        return ''


def unserialize_user(form, cookie):
    user = User()
    user.email = get_value(form, 'email')
    user.password = get_value(form, 'password')
    user.nick = get_value(form, 'nick')
    user.sessionToken = cookie
    return user