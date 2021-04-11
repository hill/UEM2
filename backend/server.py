# TOM! Aren't you just keen to use a technology that you actually know how to use!
# just build the fucker in flask. upgrade if it becomes sucessful.
from rich.traceback import install
install()

from flask import Flask
from flask_jwt_extended import JWTManager
from flask.json import jsonify

from models import initModels
from auth import auth
from course import course

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(course, url_prefix='/course')

@app.route('/')
def index():
  return jsonify({"message":"skrrt"})

if __name__ == '__main__':
  initModels()
  app.run(debug=True)