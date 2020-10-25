from flask_marshmallow.fields import Hyperlinks
from marshmallow import fields


class DictHyperlinks(Hyperlinks, fields.Dict):
    pass
