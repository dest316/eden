class LoginAlreadyExistsError(Exception):
    pass


class UniqueConstraintError(Exception):
    pass


class EntityNotFoundError(Exception):
    pass


class WrongCredentialsError(Exception):
    pass


class LinkExpiredError(Exception):
    pass


class ForbiddenError(Exception):
    pass
