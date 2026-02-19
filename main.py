from flask import Flask, render_template_string

app = Flask(__name__)

# --- [1] الهيدر الثابت (نحت مطابق للموقع الأصلي 100%) ---
MOI_TOP_BAR = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
    body { margin:0; font-family: 'Segoe UI', Tahoma, sans-serif; background:#f7f8fa; direction: rtl; text-align: right; }
    .header-top { background: white; border-bottom: 1px solid #eee; padding: 12px 25px; display: flex; justify-content: space-between; align-items: center; }
    .header-icons { display: flex; align-items: center; gap: 15px; color: #555; font-size: 16px; font-weight: bold; }
    .menu-box { background: #b0914f; color: white; padding: 8px 15px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; gap: 8px; }
    .main-logo-sec { background: white; text-align: center; padding: 15px 0; border-bottom: 4px solid #b0914f; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .main-logo-sec img { width: 95%; max-width: 700px; }
    .page-wrapper { max-width: 1000px; margin: 0 auto; padding: 20px; }
    .service-title { color: #b0914f; font-size: 32px; font-weight: bold; margin: 30px 0 10px; }
    .breadcrumb { font-size: 14px; color: #666; margin-top: 20px; }
</style>
<div class="header-top">
    <div class="header-icons">
        <span style="color:#b0914f; cursor:pointer;">EN | دخول</span>
        <i class="fa fa-rss"></i><i class="fa fa-phone"></i><i class="fa fa-question-circle"></i><i class="fa fa-volume-up"></i><i class="fa fa-info-circle"></i>
    </div>
    <div class="menu-box"><i class="fa fa-cog"></i><span>القائمة</span><i class="fa fa-bars"></i></div>
</div>
<div class="main-logo-sec">
    <img src="https://static.wixstatic.com/media/a9f3d9_06f1bacd5c6543efa20f319b06df8438~mv2.jpg">
</div>
'''

# --- [2] الصفحة الرئيسية (كاملة بجميع الخدمات) ---
@app.route('/')
def index():
    html = MOI_TOP_BAR + '''
    <style>
        .services-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 30px; }
        .service-card { background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; cursor: pointer; position: relative; transition: 0.3s; }
        .service-card:hover { transform: translateY(-5px); }
        .service-card img { width: 100%; display: block; }
        .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 5; background: transparent; }
    </style>
    <div class="page-wrapper">
        <div class="breadcrumb">الرئيسية / الخدمات الإلكترونية / <span style="color:#b0914f;">دفع المخالفات المرورية</span></div>
        <div class="service-title">دفع المخالفات المرورية</div>
        <div class="services-grid">
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_908f090c885e49048a1768656122557e~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_33d7195d43e545089f3050965f7c3558~mv2.png"></div>
            <div class="service-card" onclick="location.href='/search'"><div class="overlay"></div><img src="https://static.wixstatic.com/media/a9f3d9_6745f949c5e347719602e8609a32c3f9~mv2.png"></div>
        </div>
    </div>
    '''
    return render_template_string(html)

# --- [3] صفحة الاستعلام (التفصيل الممل - كل الخانات والمصادر والتبويبات) ---
@app.route('/search')
def search():
    html = MOI_TOP_BAR + '''
    <style>
        .form-container { background: white; border-radius: 12px; padding: 45px; box-shadow: 0 4px 25px rgba(0,0,0,0.06); border: 1px solid #eee; margin-top: 20px; }
        .tabs-row { display: flex; gap: 8px; margin-bottom: 35px; border-bottom: 1px solid #f0f0f0; }
        .tab-btn { flex: 1; padding: 18px; text-align: center; background: #fcfcfc; border: 1px solid #eee; border-bottom: none; border-radius: 10px 10px 0 0; cursor: pointer; font-weight: bold; font-size: 16px; color: #777; transition: 0.3s; margin-bottom: -1px; }
        .tab-btn.active { background: #b0914f; color: white; border-color: #b0914f; }
        .tab-content { display: none; padding-top: 10px; }
        .tab-content.active { display: block; }
        .input-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 10px; font-weight: 600; color: #333; font-size: 16px; }
        label span.req { color: #e31e24; margin-right: 3px; }
        input, select { width: 100%; padding: 16px; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; background: #fff; box-sizing: border-box; outline: none; transition: 0.2s; }
        input:focus { border-color: #b0914f; box-shadow: 0 0 5px rgba(176,145,79,0.3); }
        .grid-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .actions-row { display: flex; gap: 15px; margin-top: 30px; }
        .search-btn { flex: 2; padding: 20px; background: #b0914f; color: white; border: none; border-radius: 6px; font-size: 22px; font-weight: bold; cursor: pointer; }
        .clear-btn { flex: 1; padding: 20px; background: white; color: #333; border: 1px solid #ccc; border-radius: 6px; font-size: 18px; cursor: pointer; }
        .moi-note { background: #f4f6f9; padding: 15px; border-radius: 8px; border-right: 5px solid #b0914f; margin-top: 20px; font-size: 14px; color: #555; line-height: 1.6; }
        .help-icon { display: inline-block; width: 18px; height: 18px; background: #eee; border-radius: 50%; text-align: center; line-height: 18px; font-size: 12px; color: #666; margin-right: 8px; cursor: help; }
    </style>
    <div class="page-wrapper">
        <div class="breadcrumb">الرئيسية / الخدمات الإلكترونية / <span style="color:#b0914f;">بيانات الاستعلام</span></div>
        <div class="service-title">استعلام عن المخالفات المرورية</div>
        <div class="form-container">
            <div class="tabs-row">
                <div class="tab-btn active" onclick="openTab(event, 'plate')">بيانات اللوحة</div>
                <div class="tab-btn" onclick="openTab(event, 'traffic')">الرمز المروري</div>
                <div class="tab-btn" onclick="openTab(event, 'license')">بيانات الرخصة</div>
            </div>

            <div id="plate" class="tab-content active">
                <div class="input-group">
                    <label><span class="req">*</span> الإمارة</label>
                    <select>
                        <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                        <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option>
                        <option>رأس الخيمة / Ras Al Khaimah</option><option>الفجيرة / Fujairah</option>
                    </select>
                </div>
                <div class="grid-row">
                    <div class="input-group">
                        <label><span class="req">*</span> مصدر اللوحة</label>
                        <select>
                            <option>خصوصي / Private</option><option>تجاري / Commercial</option><option>دراجة نارية / Motorcycle</option>
                            <option>أجرة / Taxi</option><option>تصدير / Export</option><option>حافلة عامة / Public Bus</option>
                            <option>حافلة خاصة / Private Bus</option><option>شاحنة عامة / Public Transport</option>
                            <option>شاحنة خاصة / Private Transport</option><option>مقطورة / Trailer</option>
                            <option>معدات ثقيلة / Heavy Equipment</option><option>هيئة دبلوماسية / Diplomatic</option>
                            <option>تحت التجربة / Under Test</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label><span class="req">*</span> فئة اللوحة</label>
                        <select>
                            <option value="">اختر الفئة</option>
                            <option>1</option><option>2</option><option>3</option><option>4</option><option>5</option>
                            <option>6</option><option>7</option><option>8</option><option>9</option><option>10</option>
                            <option>11</option><option>12</option><option>13</option><option>14</option><option>15</option>
                            <option>16</option><option>17</option><option>50</option>
                            <option>A</option><option>B</option><option>C</option><option>D</option><option>E</option>
                            <option>F</option><option>G</option><option>H</option><option>I</option><option>J</option>
                            <option>K</option><option>L</option><option>M</option><option>N</option><option>O</option>
                            <option>P</option><option>Q</option><option>R</option><option>S</option><option>T</option>
                            <option>U</option><option>V</option><option>W</option><option>X</option><option>Y</option><option>Z</option>
                        </select>
                    </div>
                </div>
                <div class="input-group"><label><span class="req">*</span> رقم اللوحة <div class="help-icon">?</div></label><input type="number" placeholder="أدخل رقم اللوحة"></div>
            </div>

            <div id="traffic" class="tab-content">
                <div class="input-group"><label><span class="req">*</span> الرمز المروري (T.C. No)</label><input type="number" placeholder="أدخل الرمز المروري"></div>
                <div class="moi-note">الرمز المروري هو رقم موحد مسجل لدى النظام المروري لجميع المركبات والخدمات.</div>
            </div>

            <div id="license" class="tab-content">
                <div class="grid-row">
                    <div class="input-group">
                        <label><span class="req">*</span> مصدر الرخصة</label>
                        <select>
                            <option>أبوظبي / Abu Dhabi</option><option>دبي / Dubai</option><option>الشارقة / Sharjah</option>
                            <option>عجمان / Ajman</option><option>أم القيوين / Umm Al Quwain</option>
                        </select>
                    </div>
                    <div class="input-group"><label><span class="req">*</span> رقم الرخصة</label><input type="number" placeholder="أدخل رقم الرخصة"></div>
                </div>
            </div>

            <div class="actions-row">
                <button class="search-btn" onclick="location.href='/checkout'">استعلام</button>
                <button class="clear-btn" onclick="location.reload()">مسح</button>
            </div>
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
    return render_template_string(html)

# --- [4] مسار صفحة الدفع (مؤقت لحين كتابة الكود الكامل) ---
@app.route('/checkout')
def checkout():
    return MOI_TOP_BAR + '<div class="page-wrapper"><h1 style="text-align:center;">جاري تجهيز صفحة الدفع...</h1></div>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
