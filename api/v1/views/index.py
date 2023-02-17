from flask import Flask, jsonify
from api.v1 import app_views

app = Flask(__name__)

@app.route('/status')
def status():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.register_blueprint(app_views)
    app.run()

