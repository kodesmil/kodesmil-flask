import os
from flask import Flask, jsonify
from kodesmil_common.auth import AuthError
# import flask_monitoringdashboard as dashboard

app = Flask(__name__)

from . import database

db = database.Database(app).db

from . import views

app.register_blueprint(views.products)

# from . import docs

# docs = docs.Documentation(app)

# dashboard.bind(app)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
