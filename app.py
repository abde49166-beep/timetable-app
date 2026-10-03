
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# ضع رابط Web App الذي نسخته من Google Apps Script بين العلامتين " "
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxrF4bv7Bb08LriRQwNtwO4Sek_QrmdMR4fHVSt7Z9uGpdD5iXvKysmEGSO5NqxaHRbfg/exec"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-current-session', methods=['GET'])
def get_current_session():
    student_group = request.args.get('group', '1 فوج')
    
    now = datetime.now()
    current_day = now.strftime('%A')
    current_time = now.strftime('%H:%M')
    
    try:
        response = requests.get(GOOGLE_SCRIPT_URL)
        data = response.json()
        
        if "error" in data:
            return jsonify({'error': data['error']}), 500
            
        schedule_rows = data['schedule'][1:]
        profs_map = data['profs']
        
        sessions = []
        for row in schedule_rows:
            group, day, start, end, subject, location, prof_email = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            
            # التصفية حسب الفوج واليوم
            if str(group).strip() == student_group.strip() and str(day).strip().lower() == current_day.lower():
                # جلب الحصص المتبقية لليوم (التي لم تنتهِ بعد)
                if str(end) >= current_time:
                    prof_status = profs_map.get(prof_email, 'حاضر')
                    sessions.append({
                        'subject': subject,
                        'location': location,
                        'prof_status': prof_status,
                        'start': start,
                        'end': end
                    })
        
        # ترتيب الحصص حسب وقت البدء
        sessions.sort(key=lambda x: x['start'])
        return jsonify(sessions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.json
    prof_email = data.get('email')
    new_status = data.get('status')

    if not prof_email or not new_status:
        return jsonify({'success': False, 'message': 'بيانات غير مكتملة'}), 400

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json={'email': prof_email, 'status': new_status})
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
