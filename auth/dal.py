from .models.user import UserEntity


class AuthDAL:

    def __init__(self, db_session, redis):
        self.db_session = db_session
        self.redis = redis

    def create_user(self, entity: UserEntity) -> None:
        self.db_session.add(entity)
        self.db_session.commit()

    def set_on_redis(self, key: str, value: str) -> None:
        self.redis.set(key, value)

    def delete_from_redis(self, key: str) -> None:
        self.redis.delete(key)

    def get_from_redis(self, key: str) -> str:
        value = self.redis.get(key)

        if value is None:
            raise Exception('key not found in redis')

        return value

    def fetch_user_by_username(self, username: str) -> UserEntity:
        result = self.db_session.query(UserEntity).filter(
            UserEntity.username == username
        ).one_or_none()

        if not result:
            raise Exception

        return result
