import http.server
import socketserver
import os
import cgi

PORT = 8001
DIRECTORY = "/scripts"

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Change the current working directory to the specified path
        os.chdir(DIRECTORY)
        super().do_GET()

    def do_POST(self):
        # Change the current working directory to where you want to save uploaded files
        os.chdir(DIRECTORY)
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            file_content = fields.get('file')
            if file_content:
                with open('uploaded_file', 'wb') as f:
                    f.write(file_content[0])
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"File uploaded successfully.")
            else:
                self.send_error(400, "File not found in the request.")
        else:
            self.send_error(400, "Content-Type not supported.")

# Set up the HTTP server
with socketserver.TCPServer(("", PORT), ServerHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()