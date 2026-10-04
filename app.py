from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# رابط Google Apps Script الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx857KTdEUzSjoEiapFKbDlvTSx8YF7GnPo048LIedxWDroexICRfSmto9ONm5Jfnzt/exec"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    try:
        response = requests.get(f"{SCRIPT_URL}?action=getSchedule")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/update-status', methods=['POST'])
def update_status():
    try:
        data = request.json
        response = requests.post(SCRIPT_URL, json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
