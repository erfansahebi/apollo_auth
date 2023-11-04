import pytest
from apollo_shared.exception import BadRequest, Unauthorized
from auth.dal import AuthDAL
from auth.service import AuthService
from unittest.mock import patch
from unittest import mock


@pytest.fixture
def user_data_sample() -> dict:
    return {
        'username': 'erfan_username',
        'password': "password_erfan",
    }


class TestAuth:
    def test_can_register(
            self, auth_controller, user_data_sample,
    ):
        auth_controller.register(
            user_data_sample
        )

    def test_register_should_failed_duplicate(
            self, auth_controller, user_data_sample,
    ):
        auth_controller.register(
            user_data_sample
        )

        with pytest.raises(
                BadRequest,
                match="this username already has been registered"
        ):
            auth_controller.register(
                user_data_sample
            )

    def test_login_positive(self, auth_controller, user_data_sample):
        auth_controller.register(
            user_data_sample
        )
        auth_controller.login(user_data_sample)

    def test_login_negative(self, auth_controller, user_data_sample):
        payload = user_data_sample
        auth_controller.register(
            payload
        )

        # User not found
        payload['username'] = "mamad"
        with pytest.raises(
                BadRequest,
                match="user or password is wrong"
        ):
            auth_controller.login(payload)

        # Wrong password
        payload['username'] = "erfan_username"
        payload['password'] = "shet"
        with pytest.raises(
                BadRequest,
                match="user or password is wrong"
        ):
            auth_controller.login(payload)

    def test_logout(self, auth_controller, context):
        auth_controller.logout({
            "token": context['token']
        })

    @mock.patch('auth.controller.AuthDAL')
    def test_authenticate_positive(self, mock_auth_dal, auth_controller, context):
        auth_dal_instance = mock_auth_dal.return_value
        auth_dal_instance.get_from_redis.return_value = "salam_user_id"

        response = auth_controller.authenticate({
            "token": context['token']
        })

        assert response['user_id'] == "salam_user_id"

    @mock.patch('auth.controller.AuthDAL')
    def test_authenticate_negative(self, mock_auth_dal, auth_controller, context):
        auth_dal_instance = mock_auth_dal.return_value
        auth_dal_instance.get_from_redis.return_value = None

        with pytest.raises(Unauthorized, match="Unauthorized"):
            auth_controller.authenticate({
                "token": context['token']
            })
