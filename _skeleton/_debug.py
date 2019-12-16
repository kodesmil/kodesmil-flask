from flask import Flask
from .views import sample_service  # CHANGE

# main file for testing
# simply run this as flask app
# happy debugging! ;)

app = Flask(__name__)
app.register_blueprint(sample_service)  # CHANGE
