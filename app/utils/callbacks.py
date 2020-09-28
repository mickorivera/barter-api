from flask_rebar.errors import Unauthorized


def raise_unauthorized() -> None:
    raise Unauthorized
