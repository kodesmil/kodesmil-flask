import os
from flask import Flask

# import flask_monitoringdashboard as dashboard

app = Flask(__name__)

from . import database
db = database.Database(app).db

from . import views
app.register_blueprint(views.content)

# import docs
# docs = docs.Documentation(app)

# dashboard.bind(app)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
