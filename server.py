from http.server import BaseHTTPRequestHandler, HTTPServer
from aux import AddSensors

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


PORT = 8000
with HTTPServer(("", PORT), MyHandler) as server:
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()