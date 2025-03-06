from flask import Flask
from controllers.data_controller import data_bp
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
app = Flask(__name__)

# Initialize MongoDB

# Register blueprints
app.register_blueprint(data_bp, url_prefix='/api')

@app.route('/')
def hello_world():
    return 'IoT Backend API'

if __name__ == '__main__':
    app.run(debug=True)