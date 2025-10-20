from http.server import BaseHTTPRequestHandler, HTTPServer
from aux import AddSensors, CreateRegistryRow
import json

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if(self.path == "/"):

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            index_file = open("templates/base.html", 'r')
            index_data = index_file.read()
            index_file.close()

            index_data = AddSensors(index_data)

            self.wfile.write(index_data.encode())

        elif("static" in self.path ):
            self.send_response(200)
            self.send_header("Content-type","image/png")
            self.end_headers()

            with open(self.path[1:] , 'rb') as f:
                img_data = f.read()

            self.wfile.write(img_data)

        else:
            self.send_response(404)
            self.wfile.write(b"<p> Page not found </p>")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(content_length)
        data = json.loads(data)
        print(data)
        rowWasCreated = CreateRegistryRow(data)
        
        if(rowWasCreated):
            self.send_response(201)
            return_msg = "Row was created"
        else:
            self.send_response(500)
            return_msg = "<p>An error has ocurred</p>"

        self.end_headers()
        self.wfile.write(return_msg.encode())


PORT = 8000
with HTTPServer(("", PORT), MyHandler) as server:
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()