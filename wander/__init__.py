import os

from flask import Flask
from . import db
from . import auth
from . import overview
from . import retention

# works when project is started with 'flask run' from top-level dir
import data_sources_example


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wander.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(overview.bp)
    app.register_blueprint(retention.bp)
    app.add_url_rule('/', endpoint='overview.overview')

    data_sources_example.init_data_sources(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
