import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- [1] الهيكل الأساسي والهيدر الثابت ---
# ملاحظة: استخدمت الهيدر الخاص بك ليكون موحداً وثابتاً في كل الموقع
COMMON_HEADER = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        body, html { margin: 0; padding: 0; width: 100%; background-color: #f7f8fa; font-family: 'Segoe UI', Tahoma, sans-serif; scroll-behavior: smooth; }
        
        /* تثبيت الهيدر الرفيع بالملي */
        .sticky-header {
            position: fixed; top: 0; left: 0; z-index: 9999; width: 100%;
            background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        .sticky-header img { width: 100%; display: block; }
        
        .spacer { margin-top: 60px; } /* مساحة عشان المحتوى ما يختفيش تحت الهيدر */

        /* تأثير الأزرار التفاعلية */
        .interactive-btn { position: relative; cursor: pointer; transition: transform 0.2s; -webkit-tap-highlight-color: transparent; }
        .interactive-btn:active { transform: scale(0.94); filter: brightness(0.9); }
        .full-link { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 20; }
        
        /* تنسيقات صفحة الاستعلام (نحت كامل) */
        .page-wrapper { max-width: 1000px; margin: 0 auto; padding: 20px; text-align: right; }
        .breadcrumb { font-size: 13px; color: #888; margin: 20px 0; }
        .service-title { color: #b0914f; font-size: 28px; font-weight: bold; margin-bottom: 25px; }
        .form-container { background: white; border-radius: 8px; padding: 35px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #eee; }
        
        .tabs { display: flex; gap: 5px; margin-bottom: 30px; border-bottom: 2px solid #f0f0f0; }
        .tab-btn { flex: 1; padding: 15px; text-align: center; background: #fcfcfc; border: 1px solid #eee; border-bottom: none; border-radius: 8px 8px 0 0; cursor: pointer; font-weight: bold; color: #777; }
        .tab-btn.active { background: #b0914f; color: white; border-color: #b0914f; }

        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #444; }
        select, input { width: 100%; padding: 14px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; box-sizing: border-box; outline: none; background: #fff; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        
        .btn-search { width: 100%; padding: 18px; background: #b0914f; color: white; border: none; border-radius: 5px; font-size: 20px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="sticky-header">
        <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg" alt="Header">
    </div>
    <div class="spacer"></div>
'''

# --- [2] مسار الصفحة الرئيسية (كاملة بالملي كما أرسلتها) ---
@app.route('/')
def home():
    content = '''
    <div class="page-content" style="display: flex; flex-direction: column; width: 100%;">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg" alt="Nav">
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg" alt="Section 2">

        <div class="interactive-btn" onclick="location.href='/search'">
            <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg" alt="ابدأ الخدمة">
        </div>

        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg" alt="Section 4">

        <div class="interactive-btn">
            <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg" alt="مستخدم جديد">
        </div>

        <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg" alt="Section 6">
        <img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg" alt="Section 7">
        <img src="https://static.wixstatic.com/media/a9f3d9_a4395e1857c74368b9e7460f40c83938~mv2.jpg" alt="Section 8">
        <img src="https://static.wixstatic.com/media/a9f3d9_70831b816d864befb4b42fa1ffeca8f8~mv2.jpg" alt="Section 9">
    </div>
    '''
    return COMMON_HEADER + content + "</body></html>"

# --- [3] مسار صفحة الاستعلام (نحت كامل بدون اختصار) ---
@app.route('/search')
def search():
    content = '''
    <div class="page-wrapper">
        <div class="breadcrumb">الرئيسية / الخدمات الإلكترونية / <span style="color:#b0914f;">بيانات الاستعلام</span></div>
        <div class="service-title">استعلام عن المخالفات المرورية</div>
        
        <div class="form-container">
            <div class="tabs">
                <div class="tab-btn active">بيانات اللوحة</div>
                <div class="tab-btn">الرمز المروري</div>
                <div class="tab-btn">بيانات الرخصة</div>
            </div>

            <div class="input-group">
                <label><span style="color:red;">*</span> الإمارة</label>
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

            <div class="grid">
                <div class="input-group">
                    <label><span style="color:red;">*</span> مصدر اللوحة</label>
                    <select>
                        <option>خصوصي / Private</option>
                        <option>تجاري / Commercial</option>
                        <option>أجرة / Taxi</option>
                        <option>دراجة نارية / Motorcycle</option>
                        <option>تصدير / Export</option>
                        <option>حافلة عامة</option>
                        <option>مقطورة</option>
                    </select>
                </div>
                <div class="input-group">
                    <label><span style="color:red;">*</span> فئة اللوحة</label>
                    <select>
                        <option value="" selected disabled>اختر الفئة</option>
                        <optgroup label="الفئات الرقمية">
                            <option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option>10</option><option>11</option><option>12</option><option>13</option><option>14</option><option>15</option><option>16</option><option>17</option><option>50</option>
                        </optgroup>
                        <optgroup label="الفئات الحرفية">
                            <option>A</option><option>B</option><option>C</option><option>D</option><option>E</option><option>F</option><option>G</option><option>H</option><option>I</option><option>J</option><option>K</option><option>L</option><option>M</option><option>N</option><option>O</option><option>P</option><option>Q</option><option>R</option><option>S</option><option>T</option><option>U</option><option>V</option><option>W</option><option>X</option><option>Y</option><option>Z</option>
                        </optgroup>
                        <optgroup label="الفئات المزدوجة">
                            <option>AA</option><option>BB</option><option>CC</option><option>DD</option><option>EE</option><option>FF</option><option>GG</option><option>HH</option><option>II</option><option>JJ</option><option>KK</option><option>LL</option><option>MM</option><option>NN</option><option>OO</option><option>PP</option><option>QQ</option><option>RR</option><option>SS</option><option>TT</option><option>UU</option><option>VV</option><option>WW</option><option>XX</option><option>YY</option><option>ZZ</option>
                        </optgroup>
                    </select>
                </div>
            </div>

            <div class="input-group">
                <label><span style="color:red;">*</span> رقم اللوحة</label>
                <input type="number" placeholder="أدخل رقم اللوحة">
            </div>

            <button class="btn-search" onclick="location.href='/checkout'">استعلام</button>
        </div>
    </div>
    '''
    return COMMON_HEADER + content + "</body></html>"

@app.route('/checkout')
def checkout():
    return COMMON_HEADER + '<div class="page-wrapper"><h1 style="text-align:center;">جاري تجهيز صفحة الدفع...</h1></div></body></html>'

# --- [4] سطر التشغيل الذكي لحل مشكلة الكلام الأحمر ---
if __name__ == '__main__':
    # الكود ده بيسحب البورت اللي السيرفر عايزه تلقائياً
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
