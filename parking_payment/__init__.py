import os
from flask import Flask
from . import db, vehicles

def create_app() -> None:
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'parking.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(vehicles.bp)
    app.add_url_rule('/', endpoint='index')
    
    return app
