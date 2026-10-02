class LoginAlreadyExistsError(Exception):
    pass


class UniqueConstraintError(Exception):
    pass


class WrongCredentialsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass
