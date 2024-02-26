import urllib.parse

from flask import Flask, request, send_file
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

    return '''
<!doctype html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
        function submitForm(event) {
            event.preventDefault();
            var data = document.getElementById('data').value;
            var logo = document.getElementById('logo').value;
            var url = '/' + '?data=' + encodeURIComponent(data);
            if (logo) {
                url += '&logo=' + encodeURIComponent(logo);
            }
            window.location.href = url;
        }
    </script>
</head>
<body>
    <title>QR Code Generator</title>
    <form onsubmit="submitForm(event)">
        URL to QR-Codify: <input type="text" id="data" name="data" value="https://thedwelling.church"><br>
        Logo: <input type="text" id="logo" name="logo" placeholder="Leave Blank for dwelling logo"><br>
        <input type="submit" value="Generate">
    </form>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)