from core.security.password_hasher import PasswordHasher
from core.security.token_manager import TokenManager, TokenPair
from core.unit_of_work import UnitOfWork, transactional

from ..exceptions import common as DomainExceptions
from ..repositories import UserRepository


class AuthService:

    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
        uow: UnitOfWork,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_manager = token_manager
        self._uow = uow

    @transactional
    async def signup(self, login: str, nickname: str, password: str) -> TokenPair:
        hashed_password = self._password_hasher.hash(password)
        try:
            user_id = await self._user_repo.add(
                login=login, nickname=nickname, hashed_password=hashed_password
            )
            # TODO: That's not a domain exception. It's better to extract it to another file.
        except DomainExceptions.UniqueConstraintError as e:
            raise DomainExceptions.LoginAlreadyExistsError from e

        refresh_token = self._token_manager.create_refresh_token(user_id)
        access_token = self._token_manager.create_access_token(user_id)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def login(self, login: str, password: str) -> TokenPair:
        user = await self._user_repo.get_by("login", login)
        if not user:
            raise DomainExceptions.UserNotFoundError(f"There is no user with login \"{login}\"")
        
        is_password_correct = self._password_hasher.verify(password, user.hashed_pass)
        if not is_password_correct:
            raise DomainExceptions.WrongCredentialsError("Wrong username or password")
        
        access_token = self._token_manager.create_access_token(user.id)
        refresh_token = self._token_manager.create_refresh_token(user.id)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
    
