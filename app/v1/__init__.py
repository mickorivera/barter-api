from flask_rebar import SwaggerV3Generator, Tag
from flask_rebar.rebar import HandlerRegistry

from app.common.schemas import ErrorSchema
from app.v1.listing.resources import (
    create_item,
    delete_item,
    get_brand_list,
    get_category_list,
    get_item_details,
    get_tag_list,
    get_user_item_list,
    update_item,
)
from app.v1.listing.schemas import (
    BrandSchema,
    CategorySchema,
    ItemSchema,
    TagSchema,
)
from app.v1.user.resources import (
    create_user,
    get_user_details,
    get_user_list,
    login,
    logout,
)
from app.v1.user.schemas import UserSchema, UserLoginSchema, UserSignUpSchema
from config import get_config


swagger_generator = SwaggerV3Generator(
    version="1.0.0",
    title="Barter API V1",
    description="API for Barter Application",
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
    get_user_details,
    rule="/users/<id>",
    method="GET",
    response_body_schema={
        200: UserSchema(),
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
    tags=["User"],
)

# Item Endpoints
version_1_registry.add_handler(
    get_user_item_list,
    rule="/users/<user_id>/items",
    method="GET",
    response_body_schema={
        200: ItemSchema(many=True),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    get_item_details,
    rule="/items/<id>",
    method="GET",
    response_body_schema={
        200: ItemSchema(),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    create_item,
    rule="/items",
    method="POST",
    request_body_schema=ItemSchema(),
    response_body_schema={
        200: ItemSchema(),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    update_item,
    rule="/items/<id>",
    method="PATCH",
    request_body_schema=ItemSchema(partial=True),
    response_body_schema={
        200: ItemSchema(),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    delete_item,
    rule="/items/<id>",
    method="DELETE",
    response_body_schema={
        204: ErrorSchema(),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    get_brand_list,
    rule="/brands",
    method="GET",
    response_body_schema={
        200: BrandSchema(many=True),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    get_category_list,
    rule="/categories",
    method="GET",
    response_body_schema={
        200: CategorySchema(many=True),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
version_1_registry.add_handler(
    get_tag_list,
    rule="/tags",
    method="GET",
    response_body_schema={
        200: TagSchema(many=True),
        401: ErrorSchema(),
        404: ErrorSchema(),
        500: ErrorSchema(),
    },
    tags=["Item"],
)
