import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add the path of the directory containing the index.py file to the system PATH
app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(app_root))

from api.routes.index import bp
from api.auth_middleware import token_required

# This function used for unit test
def create_app():
    return app

app = Flask(__name__)
CORS(app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)
# Middleware token required
app.before_request_funcs = {
    'TR-System': [token_required]
}
app.register_blueprint(bp, url_prefix='/api/v1')

@app.route('/')
def home():
    return jsonify({'response': 'TR System Api homepage'})

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='localhost')