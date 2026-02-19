import os
import http.server
import socketserver
import json

PORT = int(os.environ.get("PORT", 8080))
API_VAL = os.environ.get("API", "your_default_key")
ENDPOINT_VAL = os.environ.get("ENDPOINT", "https://ezapi.myanmyanpay.com")

class AyeParKwarHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the main page
        if self.path == '/' or self.path == '/index.html':
            with open("index.html", "r", encoding="utf-8") as f:
                content = f.read()
            # Inject variables so fields are pre-filled
            content = content.replace("{{ API }}", API_VAL)
            content = content.replace("{{ ENDPOINT }}", ENDPOINT_VAL)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        
        # Success Page
        elif self.path == '/success':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Payment Received!</h1><p>AyeParKwar is processing your order.</p>")
        
        else:
            super().do_GET()

    def do_POST(self):
        # HANDLE THE CALLBACK
        if self.path == '/payment-callback':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Here is where you handle the secure data from MMPay
            print("--- RECEIVED PAYMENT CALLBACK ---")
            print(post_data.decode('utf-8'))
            
            # Logic: Update your database, send email, etc.
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "received"}).encode())

print(f"🚀 Server running on port {PORT}")
with socketserver.TCPServer(("", PORT), AyeParKwarHandler) as httpd:
    httpd.serve_forever()