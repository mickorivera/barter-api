from flask_rebar import SwaggerV3Generator, Tag
from flask_rebar.rebar import HandlerRegistry

from app.common.schemas import ErrorSchema
from app.v1.card.resources import get_card_list
from app.v1.card.schemas import CardSchema
from app.v1.comment.resources import (
    get_all_comments,
    get_comment_replies,
)
from app.v1.comment.schemas import CommentReplySchema, CommentSchema
from app.v1.list.resources import (
    create_list,
    delete_list_item,
    get_list_item,
    get_lists,
    update_list_item,
)
from app.v1.list.schemas import ListSchema
from app.v1.user.resources import create_user, get_user_list, login, logout
from app.v1.user.schemas import UserSchema, UserLoginSchema, UserSignUpSchema
from config import get_config


swagger_generator = SwaggerV3Generator(
    version="1.0.0",
    title="Irithm API V1",
    description="Sample API for Irithm Application",
)

config = get_config()
version_1_registry = HandlerRegistry(
    default_mimetype="application/json",
    prefix="/v1",
    swagger_generator=swagger_generator,
    swagger_path="/swagger" if config.DEBUG else None,
    swagger_ui_path="/swagger/ui" if config.DEBUG else None,
)
# TODO: enable auth
# authenticator = HeaderApiKeyAuthenticator(header='X-MyApp-ApiKey')
# authenticator.register_key(key='my-secret-api-key')

# User Endpoints
version_1_registry.add_handler(
    get_user_list,
    rule="/users",
    method="GET",
    response_body_schema={
        200: UserSchema(many=True),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["User"],
)

version_1_registry.add_handler(
    create_user,
    rule="/sign-up",
    method="POST",
    request_body_schema=UserSignUpSchema(),
    response_body_schema={
        201: UserSignUpSchema(),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["User"],
)

version_1_registry.add_handler(
    login,
    rule="/login",
    method="POST",
    request_body_schema=UserLoginSchema(),
    response_body_schema={
        200: UserLoginSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["User"],
)

version_1_registry.add_handler(
    logout,
    rule="/logout",
    method="POST",
    response_body_schema={
        200: UserSchema(),
        401: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["User"],
)
