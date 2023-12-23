from flask import Blueprint

app = Blueprint('app',
                __name__,
                url_prefix='/',
                static_folder='static',
                template_folder='templates')

from views.app_views import *
