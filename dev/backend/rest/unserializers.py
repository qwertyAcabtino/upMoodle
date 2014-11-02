from rest.models import User


def unserialize_user(form):
    user = User()
    user.email = form['email']
    user.password = form['password']
    user.nick = form['nick']
    return user

