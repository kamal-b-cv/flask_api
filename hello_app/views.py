from datetime import datetime
from flask import Flask, render_template,request, jsonify
import hashlib
from . import app

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name = None):
#     return render_template(
#         "hello_there.html",
#         name=name,
#         date=datetime.now()
#     )

@app.route('/calculate_hash', methods=['POST'])
def calculate_hash():
    try:
        # Get data from the request
        data = request.json.get('data_batch')
        # Get columns to hash from the request
        columns_to_hash = request.json.get('columns_to_hash')

        if not columns_to_hash:
            raise ValueError("No columns specified for hashing")

        # Calculate hash values for each column
        for d in data:
            for column in columns_to_hash:
                if column in d:
                    d[column] = hashlib.sha256(d[column].encode()).hexdigest()

        # Prepare response
        response = {'hash_value': data}
        return render_template("hash_calc.html")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
