from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/store-file', methods=['POST'])
def store_file():
    try:
        data = request.get_json()
        # Validate that both "file" and "data" are present and non-null.
        if not data or data.get('file') is None or data.get('data') is None:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400

        filename = data['file']
        file_data = data['data']

        # Ensure the persistent storage directory exists.
        os.makedirs('/preet_PV_dir', exist_ok=True)
        file_path = f'/preet_PV_dir/{filename}'

        with open(file_path, 'w') as f:
            f.write(file_data)

        return jsonify({
            "file": filename,
            "message": "Success."
        })

    except Exception:
        return jsonify({
            "file": filename if 'filename' in locals() else None,
            "error": "Error while storing the file to the storage."
        }), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        # Validate that both "file" and "product" keys are present and non-null.
        if not data or data.get('file') is None or data.get('product') is None:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400

        filename = data['file']
        file_path = f'/preet_PV_dir/{filename}'

        # Check if file exists.
        if not os.path.exists(file_path):
            return jsonify({
                "file": filename,
                "error": "File not found."
            }), 404

        # Forward request to container2.
        response = requests.post('http://container2-service:8000/calculate', json=data)
        return response.json(), response.status_code

    except Exception as e:
        return jsonify({
            "file": filename if 'filename' in locals() else None,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
