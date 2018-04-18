def jwt_auth(function):
    def wrap(*args, **kwargs):
        if not request.headers["authorization"]
            return{'Authorization': 'Not Authorized'}, 401
        return function(*args, **kwargs)

    return wrap