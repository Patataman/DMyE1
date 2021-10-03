from flask import Flask, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

from src.models import db, User, Role
from src.views.main import main_module


app = Flask(__name__)
jinja_env = app.jinja_env
jinja_env.add_extension("jinja2.ext.do")

app.config.from_pyfile('config/config.cfg')
app.static_url_path='/src/static'
app.static_folder=app.root_path + app.static_url_path

app.register_blueprint(main_module, url_prefix='')

# db.app = app
# db.init_app(app)
# db.create_all()

# logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


@app.errorhandler(404)
def page_not_found(e):
    session.pop('_flashes', None)
    flash(gettext("Unknown path"), "warning")
    return redirect("/")