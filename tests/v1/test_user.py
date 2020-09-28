import pytest
from http import HTTPStatus

from app import RestApp
from app.utils.time import format_date
from app.v1.user.models import UserModel


class TestUserLogin:
    def setup_method(self):
        app = RestApp()

        @app.login_manager.user_loader
        def load_user(user_id):
            try:
                user = UserModel.get(user_id, is_deleted=False)
            except UserModel.DoesNotExist:
                return None
            else:
                return user

        self._app_client = app.test_client()

        self.endpoint = "v1/login"
        self.content_type = "application/json"

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                {
                    "username": "user1",
                    "password": "password1",
                },
                {
                    "status_code": HTTPStatus.OK,
                    "response": {"username": "user1"},
                },
            ),
            (
                {
                    "username": "user1",
                    "password": "incorrectpassword",
                },
                {
                    "status_code": HTTPStatus.UNAUTHORIZED,
                    "response": {"message": "Unauthorized"},
                },
            ),
            (
                {
                    "username": "incorrectusername",
                    "password": "password1",
                },
                {
                    "status_code": HTTPStatus.NOT_FOUND,
                    "response": {"message": "Not Found"},
                },
            ),
        ],
    )
    def test_login(self, test_input, expected):
        response = self._app_client.post(
            self.endpoint,
            content_type=self.content_type,
            json=test_input,
        )

        assert expected["status_code"] == response.status_code
        assert expected["response"] == response.json


class TestUserIndex:
    def setup_method(self):
        app = RestApp()
        self._app_client = app.test_client()

        @app.login_manager.user_loader
        def load_user(user_id):
            try:
                user = UserModel.get(user_id, is_deleted=False)
            except UserModel.DoesNotExist:
                return None
            else:
                return user

        self.endpoint = "v1/users"
        self.content_type = "application/json"

    def test_get_user_list(self, users):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.get(
            self.endpoint,
            content_type=self.content_type,
        )

        assert HTTPStatus.OK == response.status_code
        expected_response = [
            {
                "id": user.id,
                "username": user.username,
                "email_address": user.email_address,
                "role": user.role,
                "date_created": format_date(user.date_created),
                "date_updated": format_date(user.date_updated),
            }
            for user in users
        ]
        assert expected_response == response.json
