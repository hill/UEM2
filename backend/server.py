# TOM! just build the fucker in flask.
from datetime import timedelta
from rich.traceback import install
install()

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask
from flask_jwt_extended import JWTManager
from flask.json import jsonify
from flask_cors import CORS

from models import initModels
from auth import auth
from course import course
from resource import resource

sentry_sdk.init(
  dsn="https://9fabfac1a4874239a0c878f65e2d1adc@o454372.ingest.sentry.io/5727387",
  integrations=[FlaskIntegration()],
  traces_sample_rate=1.0,
  environment="dev"
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10) # TODO(TOM): use refresh tokens
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(course, url_prefix='/course')
app.register_blueprint(resource, url_prefix='/resource')

@app.route('/')
def index():
  return jsonify({"message":"skrrt"})

@app.route('/debug-sentry')
def trigger_error():
  division_by_zero = 1 / 0

if __name__ == '__main__':
  initModels()
  app.run(debug=True)