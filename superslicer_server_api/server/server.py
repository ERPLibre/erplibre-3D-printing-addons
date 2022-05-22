from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def root():
    return jsonify({
        "name": "SuperSlicer Server",
        "description": "Web Server API for SuperSlicer",
        "version": "1.0.0"
    })


@app.route('/test')
def test_function():
    return jsonify(message="Welcome to Test endpoint", status=200, category="success")


if __name__ == '__main__':
    app.run()
