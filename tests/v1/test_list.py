from http import HTTPStatus

from app import RestApp
from app.utils.time import format_date
from app.v1.user.models import UserModel


class TestListIndex:
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

        self.content_type = "application/json"
        self.endpoint = "v1/lists"

    def test_get_lists(self, lists):
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
                "id": app_list.id,
                "author_id": app_list.author_id,
                "title": app_list.title,
                "date_created": format_date(app_list.date_created),
                "date_updated": format_date(app_list.date_updated),
            }
            for app_list in lists
        ]
        assert expected_response == response.json

    def test_get_lists_unauthorized(self, lists):
        response = self._app_client.get(
            self.endpoint,
            content_type=self.content_type,
        )

        assert HTTPStatus.UNAUTHORIZED == response.status_code
        assert {"message": "Unauthorized"} == response.json


class TestListShow:
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

        self.content_type = "application/json"
        self.endpoint = "v1/lists/{id}"

    def test_get_list(self, lists):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.get(
            self.endpoint.format(id=lists[0].id),
            content_type=self.content_type,
        )

        assert HTTPStatus.OK == response.status_code
        expected_response = {
            "id": lists[0].id,
            "author_id": lists[0].author_id,
            "title": lists[0].title,
            "date_created": format_date(lists[0].date_created),
            "date_updated": format_date(lists[0].date_updated),
        }
        assert expected_response == response.json

    def test_get_list_not_found(self, lists):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.get(
            self.endpoint.format(id=-1),
            content_type=self.content_type,
        )

        assert HTTPStatus.NOT_FOUND == response.status_code
        assert {"message": "Not Found"} == response.json

    def test_get_list_unauthorized(self, lists):
        response = self._app_client.get(
            self.endpoint.format(id=lists[0].id),
            content_type=self.content_type,
        )

        assert HTTPStatus.UNAUTHORIZED == response.status_code
        assert {"message": "Unauthorized"} == response.json


class TestListCreation:
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

        self.content_type = "application/json"
        self.endpoint = "v1/lists"

    def test_create_list(self, users, lists):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.post(
            self.endpoint,
            content_type=self.content_type,
            json={"title": "Test Title"},
        )

        assert HTTPStatus.OK == response.status_code
        user = [user for user in users if user.username == "user1"].pop()
        expected_response = {
            "author_id": user.id,
            "title": "Test Title",
        }
        assert response.json.pop("date_created", None) is not None
        assert response.json.pop("date_updated", None) is not None
        assert response.json.pop("id", None) is not None
        assert expected_response == response.json

    def test_create_lists_unauthorized(self, lists):
        response = self._app_client.post(
            self.endpoint, content_type=self.content_type, json={}
        )

        assert HTTPStatus.UNAUTHORIZED == response.status_code
        assert {"message": "Unauthorized"} == response.json


class TestUpdateList:
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

        self.content_type = "application/json"
        self.endpoint = "v1/lists/{id}"

    def test_update_list_item(self, lists):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.patch(
            self.endpoint.format(id=lists[0].id),
            content_type=self.content_type,
            json={"title": "Hakuna Matata"},
        )

        assert HTTPStatus.OK == response.status_code
        assert response.json.pop("date_created", None) is not None
        assert response.json.pop("date_updated", None) is not None
        assert response.json.pop("id", None) is not None
        expected_response = {
            "author_id": lists[0].author_id,
            "title": "Hakuna Matata",
        }
        assert expected_response == response.json

    def test_update_list_item_not_found(self, lists):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.patch(
            self.endpoint.format(id=-1),
            content_type=self.content_type,
            json={},
        )

        assert HTTPStatus.NOT_FOUND == response.status_code
        assert {"message": "Not Found"} == response.json

    def test_update_list_item_unauthorized(self, lists):
        response = self._app_client.patch(
            self.endpoint.format(id=lists[0].id),
            content_type=self.content_type,
            json={},
        )

        assert HTTPStatus.UNAUTHORIZED == response.status_code
        assert {"message": "Unauthorized"} == response.json


class TestDeleteList:
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

        self.content_type = "application/json"
        self.endpoint = "v1/lists/{id}"

    def test_delete_list_item(self, lists):
        self._app_client.post(
            "v1/login",
            content_type=self.content_type,
            json={
                "username": "user1",
                "password": "password1",
            },
        )

        response = self._app_client.post(
            "v1/lists/",
            content_type=self.content_type,
            json={"title": "Test Title"},
        )
        list_id = response.json["id"]

        response = self._app_client.delete(
            self.endpoint.format(id=list_id),
            content_type=self.content_type,
            json={"title": "Hakuna Matata"},
        )

        assert HTTPStatus.NO_CONTENT == response.status_code

        response = self._app_client.get(
            self.endpoint.format(id=list_id),
            content_type=self.content_type,
        )
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_update_list_item_unauthorized(self, lists):
        response = self._app_client.delete(
            self.endpoint.format(id=lists[0].id),
            content_type=self.content_type,
            json={},
        )

        assert HTTPStatus.UNAUTHORIZED == response.status_code
        assert {"message": "Unauthorized"} == response.json
