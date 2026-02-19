import os
import http.server
import socketserver

# 1. SETUP
# Railway assigns a random PORT, we must listen on it
PORT = int(os.environ.get("PORT", 8080))

# Get your custom variables
MY_API_KEY = os.environ.get("API", "")
MY_ENDPOINT = os.environ.get("ENDPOINT", "")

# 2. DEFINE THE HANDLER
class SecureInjector(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Only inject if user asks for homepage
        if self.path == '/' or self.path == '/index.html':
            try:
                # Read the original HTML file
                with open("index.html", "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace BOTH placeholders with the real environment variables
                content = content.replace("{{ API_KEY }}", MY_API_KEY)
                content = content.replace("{{ ENDPOINT_URL }}", MY_ENDPOINT)
                
                # Send it to the browser
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
                return
            except Exception as e:
                print(f"Error serving HTML: {e}")
        
        # For all other files (images, css), work normally
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# 3. START SERVER
print(f"🚀 AyeParKwar Server started on port {PORT}")

# Safety check (prints to Railway logs only)
if not MY_API_KEY: print("⚠️ WARNING: Variable 'API' is missing!")
if not MY_ENDPOINT: print("⚠️ WARNING: Variable 'ENDPOINT' is missing!")

with socketserver.TCPServer(("", PORT), SecureInjector) as httpd:
    httpd.serve_forever()