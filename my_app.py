from flask import Flask, request, send_file
from main import generate_qr_code, resize_qr_code, apply_logo, generate_and_save_qr_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        qr_code_stream = generate_and_save_qr_code(data)

        return send_file(qr_code_stream, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

    return '''
    <!doctype html>
    <title>QR Code Generator</title>
    <form method=post enctype=multipart/form-data>
      Data: <input type=text name=data><br>
      <input type=submit value=Generate>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)