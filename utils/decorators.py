import functools

from flask import abort
from flask_login import current_user


def roles_required(*roles):
    """
    Этот декоратор используется перед маршрутами,
    чтобы убедиться, что текущий_пользователь имеет право
    доступа к этому маршруту.
    """
    def holder(action):
        @functools.wraps(action)
        def wrapper(*args, **kwargs):
            nonlocal roles
            if current_user.is_authenticated and current_user.has_roles(*roles):
                return action(*args, **kwargs)
            return abort(401)

        return wrapper

    return holder
