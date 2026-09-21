from functools import wraps

from flask import abort
from flask_login import current_user


def roles_requeridos(*roles):

    def decorador(func):

        @wraps(func)
        def funcion_protegida(*args, **kwargs):

            if not current_user.is_authenticated:
                abort(401)

            if current_user.rol not in roles:
                abort(403)

            return func(*args, **kwargs)

        return funcion_protegida

    return decorador