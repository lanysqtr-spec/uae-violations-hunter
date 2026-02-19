import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- [1] الهيكل والتنسيقات المتقدمة (CSS) ---
COMMON_HEADER = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html { margin: 0; padding: 0; width: 100%; background-color: #f7f8fa; font-family: 'Segoe UI', Tahoma, sans-serif; scroll-behavior: smooth; }
        
        /* الهيدر الثابت */
        .sticky-header { position: fixed; top: 0; left: 0; z-index: 9999; width: 100%; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .sticky-header img { width: 100%; display: block; }
        .spacer { margin-top: 65px; }

        /* تنسيق الصفحة الرئيسية كصورة واحدة مقسمة */
        .page-content { position: relative; width: 100%; display: flex; flex-direction: column; }
        .page-content img { width: 100%; height: auto; display: block; margin: 0; padding: 0; border: none; }

        /* تحديد مكان الأزرار الشفافة بالضبط فوق الصور */
        .btn-overlay {
            position: absolute;
            width: 100%; /* العرض كامل */
            height: 80px; /* ارتفاع الزرار التقريبي */
            background: rgba(255, 255, 255, 0); /* شفاف تماماً */
            cursor: pointer;
            z-index: 100;
        }
        /* مكان زرار ابدأ الخدمة (يعدل حسب ترتيب الصور) */
        .start-service-pos { top: 950px; } 
        /* مكان زرار مستخدم جديد */
        .new-user-pos { top: 1450px; }

        /* تنسيقات صفحة الاستعلام والتبويبات */
        .page-wrapper { max-width: 1000px; margin: 40px auto; padding: 20px; direction: rtl; text-align: right; }
        .service-title { color: #b0914f; font-size: 28px; font-weight: bold; margin-bottom: 25px; }
        .form-container { background: white; border-radius: 8px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #eee; }
        
        .tabs { display: flex; gap: 5px; margin-bottom: 30px; border-bottom: 2px solid #f0f0f0; }
        .tab-btn { flex: 1; padding: 15px; text-align: center; background: #fcfcfc; border: 1px solid #eee; border-bottom: none; border-radius: 8px 8px 0 0; cursor: pointer; font-weight: bold; color: #777; transition: 0.3s; }
        .tab-btn.active { background: #b0914f; color: white; border-color: #b0914f; }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        .input-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #444; }
        select, input { width: 100%; padding: 15px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; box-sizing: border-box; outline: none; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .btn-search { width: 100%; padding: 18px; background: #b0914f; color: white; border: none; border-radius: 5px; font-size: 20px; font-weight: bold; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="sticky-header">
        <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
    </div>
    <div class="spacer"></div>
'''

# --- [2] الصفحة الرئيسية (الأزرار الشفافة فوق الصور) ---
@app.route('/')
def home():
    content = '''
    <div class="page-content">
        <img src="https://static.wixstatic.com/media/a9f3d9_c1d337bf7a804573a004f115b6c69d23~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_d8f02563f4e2475fa5e4fcc5b2daaaf5~mv2.jpg">
        
        <div class="btn-overlay start-service-pos" onclick="location.href='/search'"></div>
        <img src="https://static.wixstatic.com/media/a9f3d9_d0dcb4c088a84089afa337a46bc21bf7~mv2.jpg">

        <img src="https://static.wixstatic.com/media/a9f3d9_dc754b0143e14766a16919be2a1ee249~mv2.jpg">

        <div class="btn-overlay new-user-pos"></div>
        <img src="https://static.wixstatic.com/media/a9f3d9_0596c91fd65d49a9b3598f7d4ff5a811~mv2.jpg">

        <img src="https://static.wixstatic.com/media/a9f3d9_1347280275a14cada9eef8982ee5a375~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_662e4c074fe94f80940882c18cd51a87~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_a4395e1857c74368b9e7460f40c83938~mv2.jpg">
        <img src="https://static.wixstatic.com/media/a9f3d9_70831b816d864befb4b42fa1ffeca8f8~mv2.jpg">
    </div>
    '''
    return COMMON_HEADER + content + "</body></html>"

# --- [3] صفحة الاستعلام (برمجة التبويبات + كل المصادر) ---
@app.route('/search')
def search():
    content = '''
    <div class="page-wrapper">
        <div class="service-title">استعلام عن المخالفات المرورية</div>
        
        <div class="form-container">
            <div class="tabs">
                <div class="tab-btn active" onclick="openTab(event, 'plate-data')">بيانات اللوحة</div>
                <div class="tab-btn" onclick="openTab(event, 'tc-number')">الرمز المروري</div>
                <div class="tab-btn" onclick="openTab(event, 'license-data')">بيانات الرخصة</div>
            </div>

            <div id="plate-data" class="tab-content active">
                <div class="input-group">
                    <label><span style="color:red;">*</span> الإمارة</label>
                    <select>
                        <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                        <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option>
                        <option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
                    </select>
                </div>
                <div class="grid">
                    <div class="input-group">
                        <label><span style="color:red;">*</span> مصدر اللوحة</label>
                        <select>
                            <option>خصوصي / Private</option><option>تجاري / Commercial</option>
                            <option>أجرة / Taxi</option><option>دراجة نارية / Motorcycle</option>
                            <option>تصدير / Export</option><option>حافلة عامة / Public Bus</option>
                            <option>مقطورة / Trailer</option><option>شرطة / Police</option>
                            <option>تحت التجربة / Under Test</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label><span style="color:red;">*</span> فئة اللوحة</label>
                        <select>
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
            </div>

            <div id="tc-number" class="tab-content">
                <div class="input-group">
                    <label><span style="color:red;">*</span> رقم الرمز المروري (T.C. Number)</label>
                    <input type="number" placeholder="أدخل رقم الرمز المروري">
                </div>
            </div>

            <div id="license-data" class="tab-content">
                <div class="input-group">
                    <label><span style="color:red;">*</span> إمارة الرخصة</label>
                    <select><option>أبوظبي</option><option>دبي</option></select>
                </div>
                <div class="input-group">
                    <label><span style="color:red;">*</span> رقم الرخصة</label>
                    <input type="number" placeholder="أدخل رقم الرخصة">
                </div>
            </div>

            <button class="btn-search" onclick="location.href='/checkout'">استعلام</button>
        </div>
    </div>

    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; }
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
    </script>
    '''
    return COMMON_HEADER + content + "</body></html>"

@app.route('/checkout')
def checkout():
    return COMMON_HEADER + '<div class="page-wrapper"><h1 style="text-align:center;">جاري التحميل...</h1></div></body></html>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
