from flask import  Blueprint

# Declaring Blueprint instance
api_blueprint = Blueprint("orders", __name__, url_prefix='/orders')

# Need import views to make them visible
from . import views
from . import models