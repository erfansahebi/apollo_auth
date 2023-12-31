from .models.user import UserEntity
from apollo_shared.schema import auth as auth_schema
from apollo_shared import exception
from .dal import AuthDAL
from secrets import token_hex
import bcrypt


class AuthService:

    def __init__(self, auth_dal: AuthDAL):
        self.auth_dal = auth_dal

    def register(self, data: auth_schema.RegisterSchemaRPC) -> (UserEntity, str):
        exist_user = self.auth_dal.fetch_user_by_username(data['username'])

        if exist_user is not None:
            raise exception.BadRequest("this username already has been registered")

        user = UserEntity(**data)
        user.password = self.__hashing_password(user.password)

        self.auth_dal.create_user(user)

        return user, self.__set_token(str(user.id))

    def login(self, data: auth_schema.LoginSchemaRPC) -> (UserEntity, str):
        user = self.auth_dal.fetch_user_by_username(data['username'])

        if user is None:
            raise exception.BadRequest('user or password is wrong')

        if not self.__check_password(data['password'], user.password):
            raise exception.BadRequest('user or password is wrong')

        return user, self.__set_token(str(user.id))

    def logout(self, data: auth_schema.LogoutRPC) -> None:
        key = self.__generate_key_for_token(data['token'])
        self.auth_dal.delete_from_redis(key)

    def authenticate(self, data: auth_schema.AuthenticateRPC) -> str:
        key = self.__generate_key_for_token(data['token'])

        user_id = self.auth_dal.get_from_redis(key)

        if user_id is None:
            raise exception.Unauthorized('Unauthorized')

        return user_id

    def __set_token(self, user_id: str) -> str:
        token = self.__generate_token()

        key = self.__generate_key_for_token(token)

        self.auth_dal.set_on_redis(key=key, value=user_id)

        return token

    def __generate_key_for_token(self, token: str) -> str:
        return f'token.{token}'.lower()

    def __generate_token(self, length=20) -> str:
        return token_hex(length)

    def __hashing_password(self, password: str, salt: bytes = None) -> str:
        if salt is None:
            salt = bcrypt.gensalt()

        return bcrypt.hashpw(password.encode(), salt).decode()

    def __check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
