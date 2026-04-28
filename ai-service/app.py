import time
from collections import deque
from flask import Flask, jsonify, g, request
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.health import health_bp

app = Flask(__name__)

# Application state
app.config['START_TIME'] = time.time()
app.config['REQUEST_TIMES'] = deque(maxlen=100) # Keep last 100 requests

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time') and request.endpoint in ['describe.describe', 'recommend.recommend', 'generate_report.generate_report']:
        elapsed = time.time() - g.start_time
        app.config['REQUEST_TIMES'].append(elapsed)
    return response

# Register Blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
