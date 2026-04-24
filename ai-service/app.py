from flask import Flask, jsonify
from routes.describe import describe_bp
from routes.recommend import recommend_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
