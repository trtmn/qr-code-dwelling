from flask import Flask, request, send_file, render_template

import main
from main import generate_qr_code, resize_qr_code, apply_logo, generate_and_save_qr_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        #URL encode the data
        data = urllib.parse.quote_plus(data)
    else:
        data = request.args.get('data', default=None, type=str)

    logo = request.args.get('logo', default=None, type=str)

    if data is not None:
        qr_code_stream = generate_and_save_qr_code(data, logo)
        return send_file(qr_code_stream, mimetype='image/png')
    icons = main.scan_icons_folder()
    return render_template('index.html', icons=icons)

if __name__ == '__main__':
    app.run(debug=True)