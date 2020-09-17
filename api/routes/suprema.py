from flask import (
    Blueprint
)

bp = Blueprint(
    "suprema", __name__,
    url_prefix='/suprema')


@bp.route('/', methods=['POST'])
def test():
    pass
