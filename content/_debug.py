from flask import Flask
from .views import content

# main file for testing
# simply run this as flask app
# happy debugging! ;)

app = Flask(__name__)
app.register_blueprint(content)
