from flask import Flask, request, flash, redirect, url_for, session
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

from app.views.main import main_module


app = Flask(__name__)
jinja_env = app.jinja_env
jinja_env.add_extension("jinja2.ext.do")

app.config.from_pyfile('config/config.cfg')
app.static_url_path='/static'
app.static_folder=app.root_path + app.static_url_path

app.register_blueprint(main_module, url_prefix='')

# Compilation & minification of .scss files
# and minification of .js files it is done in the view
assets = Environment(app)

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
    flash("Unknown path", "warning")
    return redirect("/")