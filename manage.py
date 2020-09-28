import random
import string
from flask import g, request

from app import RestApp
from app.v1.user.models import UserModel


app = RestApp()


@app.login_manager.user_loader
def load_user(user_id):
    try:
        user = UserModel.get(user_id, is_deleted=False)
    except UserModel.DoesNotExist:
        return None
    else:
        return user


@app.before_request
def log_request_info():
    log_id = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(5)
    )
    g.log_id = log_id

    # TODO: mask password
    app.logger.info(
        f"LOG ID: {g.log_id} HEADERS: {request.headers}\n"
        f"LOG ID: {g.log_id} REQUEST METHOD: {request.method}\n"
        f"LOG ID: {g.log_id} REQUEST PARAMS: {request.args}\n"
        f"LOG ID: {g.log_id} REQUEST BODY: {request.data}"
    )


@app.after_request
def log_response_info(response):
    app.logger.info(
        f"LOG ID: {g.log_id} RESPONSE STATUS: {response.status}\n"
        f"LOG ID: {g.log_id} RESPONSE DATA: {response.json}"
    )
    return response


if __name__ == "__main__":
    app.run()
