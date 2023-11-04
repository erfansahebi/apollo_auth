from apollo_shared.schema import auth as auth_schema
from nameko.rpc import rpc
from apollo_shared.rpc.auth import AuthRPC
from nameko_sqlalchemy import Database
from apollo_shared.alembic.models import Base as DeclarativeBase
from .service import AuthService
from .dal import AuthDAL
from nameko_redis import Redis


class AuthController(AuthRPC):
    db = Database(DeclarativeBase)
    redis = Redis('auth')

    @rpc
    def register(self, data: auth_schema.RegisterSchemaRPC) -> auth_schema.RegisterSchemaRPCResponse:
        auth_service = self.__get_auth_service()
        user, token = auth_service.register(data)
        return auth_schema.RegisterSchemaRPCResponse().load({
            'user_id': str(user.id),
            'token': token,
        })

    @rpc
    def login(self, data: auth_schema.LoginSchemaRPC) -> auth_schema.LoginSchemaRPCResponse:
        auth_service = self.__get_auth_service()

        user, token = auth_service.login(data)

        return auth_schema.LoginSchemaRPCResponse().load({
            'user_id': str(user.id),
            'token': token,
        })

    @rpc
    def logout(self, data: auth_schema.LogoutRPC) -> None:
        auth_service = self.__get_auth_service()

        auth_service.logout(data)

    @rpc
    def authenticate(self, data: auth_schema.AuthenticateRPC) -> auth_schema.AuthenticateRPCResponse:
        auth_service = self.__get_auth_service()

        user_id = auth_service.authenticate(data)

        return auth_schema.AuthenticateRPCResponse().dump({
            'user_id': user_id,
        })

    def __get_auth_service(self) -> AuthService:
        auth_dal = AuthDAL(
            db_session=self.db.session,
            redis=self.redis,
        )

        return AuthService(
            auth_dal=auth_dal,
        )
