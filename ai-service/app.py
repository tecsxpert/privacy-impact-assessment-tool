from flask import Flask
from routes.describe import describe_bp
from routes.recommend import recommend_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)

@app.route('/')
def home():
    return {"message": "AI Service Running"}

if __name__ == '__main__':
    app.run(port=5000, debug=True)