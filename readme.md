# QR Code Generator
This is a simple QR code generator using Python and the qrcode library.

## Product Requirements
- The user should be able to input a string and generate a QR code.
- Output to either PNG or SVG file format.
- Should be able to specify the quality of the QR code.
- Should be able to add a logo to the QR code.
- Use bootstrap for the UI.


Deploying:
1. Clone the repository
2. Ensure you have Docker installed
3. cd to the project directory
4. Run `docker build -t qr-maker .`
5. docker run -p 80:80 -v $(pwd):/app --env tunnel_key=<your key from cloudflare> --env SERVER_NAME=<full hostname for named tunnel on cloudflare> qr-maker:latest 