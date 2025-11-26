from http.server import BaseHTTPRequestHandler, HTTPServer
from aux import AddSensors, CreateRegistryRow, GetActiveSensors, InsertTransmissionRow, DeleteSensor, RenameSensor
import json, re as regex

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

        elif( regex.search( r"\/static\/.*", self.path) ):
            self.send_response(200)
            self.send_header("Content-type","image/png")
            self.end_headers()

            with open(self.path[1:] , 'rb') as f:
                img_data = f.read()

            self.wfile.write(img_data)

        elif( regex.search(r"\/activeSensors", self.path) ):
            activeSensors = GetActiveSensors()  
            json_dict = json.dumps({'sensors':activeSensors}).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(json_dict)))
            self.end_headers()

            self.wfile.write(json_dict)

        else:
            self.send_response(404)
            self.wfile.write(b"<p> Page not found </p>")

    def do_POST(self):

        if( regex.search(r"\/createRow", self.path) ):

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

        elif( regex.search(r"\/receiveTransmission", self.path) ):
            content_length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(content_length)
            data = json.loads(data)
            print(data)

            recordWasCreated = InsertTransmissionRow(int(data["sensor"]))
            if(recordWasCreated):
                self.send_response(201)
                return_msg = "Row was created"
            else:
                self.send_response(500)
                return_msg = "<p>An error has ocurred</p>"

            self.end_headers()
            self.wfile.write(return_msg.encode())
        elif( regex.search(r"\/deleteSensor", self.path) ):
            content_length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(content_length)
            data = json.loads(data)
            print("Delete request:", data)

            try:
                ok = DeleteSensor(int(data.get("sensor")))
                if ok:
                    self.send_response(200)
                    return_msg = "Sensor deleted"
                else:
                    self.send_response(500)
                    return_msg = "Failed to delete sensor"
            except Exception as e:
                print(e)
                self.send_response(500)
                return_msg = "Error processing request"

            self.end_headers()
            self.wfile.write(return_msg.encode())
        elif( regex.search(r"\/renameSensor", self.path) ):
            content_length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(content_length)
            data = json.loads(data)
            print("Rename request:", data)

            try:
                sensor_id = int(data.get("sensor"))
                new_name = data.get("name")
                if new_name is None:
                    raise ValueError("Missing name")

                ok = RenameSensor(sensor_id, new_name)
                if ok:
                    self.send_response(200)
                    return_msg = "Sensor renamed"
                else:
                    self.send_response(500)
                    return_msg = "Failed to rename sensor"
            except Exception as e:
                print(e)
                self.send_response(500)
                return_msg = "Error processing rename request"

            self.end_headers()
            self.wfile.write(return_msg.encode())
        else:
            self.send_response(404)
            self.wfile.write(b"<p> Page not found </p>")


PORT = 8000
with HTTPServer(("", PORT), MyHandler) as server:
    print(f"Server running on http://localhost:{PORT}")
    server.serve_forever()