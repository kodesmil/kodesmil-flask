from flask import Flask
from .views import content, get_services
import flask_monitoringdashboard as dashboard
from flask_apispec import FlaskApiSpec

# main file for testing
# simply run this as flask app
# happy debugging! ;)

# app setup

app = Flask(__name__)
app.register_blueprint(content)

# dashboard setup
dashboard.bind(app)

# docs setup
docs = FlaskApiSpec(app)
docs.register(get_services, endpoint='get_services', blueprint='content')
