# Copyright (C) 2016 University of Zurich.  All rights reserved.
#
# This file is part of MSRegistry Backend.
#
# MSRegistry Backend is free software: you can redistribute it and/or
# modify it under the terms of the version 3 of the GNU Affero General
# Public License as published by the Free Software Foundation, or any
# other later version.
#
# MSRegistry Backend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the version
# 3 of the GNU Affero General Public License for more details.
#
# You should have received a copy of the version 3 of the GNU Affero
# General Public License along with MSRegistry Backend.  If not, see
# <http://www.gnu.org/licenses/>.

__author__ = "Filippo Panessa <filippo.panessa@uzh.ch>"
__copyright__ = ("Copyright (c) 2016 S3IT, Zentrale Informatik,"
" University of Zurich")


from Crypto.PublicKey import RSA

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mongoalchemy import MongoAlchemy
from flask_environments import Environments
from flask_mail import Mail, Message
from flask import jsonify
from flask import _app_ctx_stack as stack

from app.exceptions import InvalidUsage

bootstrap = Bootstrap()
db = MongoAlchemy()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    env = Environments(app, default_env=config_name)
    app.config.from_object(env.from_yaml('config.yml'))

    certfile = app.config['OAUTH_CERTIFICATE_PATH']
    with open(certfile, 'r') as fd:
        kt = fd.read()
    key = RSA.importKey(kt)
    app.oauth_certificate = key.publickey().exportKey()
    
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
