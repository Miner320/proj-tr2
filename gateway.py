import serial
import json
import time
import http.client

SERIAL_PORT = "COM35" # porta do receptor LoRa
BAUDRATE = 9600
SERVER_IP = "127.0.0.9"  # ou IP do servidor
SERVER_PORT = 8000

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print("Gateway iniciado. Aguardando dados LoRa...")

    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue

        print(f"Recebido via LoRa: {line}")

        try:
            temp, umid = map(float, line.split(","))

            # envia temperatura
            data_temp = {
                "Valor": temp,
                "Sensor": 1,
                "Tipo": 1,
                "TimeStamp": int(time.time())
            }
            headers = {"Content-Type": "application/json"}

            conn = http.client.HTTPConnection(SERVER_IP, SERVER_PORT)
            conn.request("POST", "/createRow", body=json.dumps(data_temp), headers=headers)
            response = conn.getresponse()
            print("Temperatura enviada:", temp, "-", response.status, response.reason)
            conn.close()

            # envia umidade
            data_umid = {
                "Valor": umid,
                "Sensor": 1,
                "Tipo": 3,
                "TimeStamp": int(time.time())
            }

            conn = http.client.HTTPConnection(SERVER_IP, SERVER_PORT)
            conn.request("POST", "/createRow", body=json.dumps(data_umid), headers=headers)
            response = conn.getresponse()
            print("Umidade enviada:", umid, "-", response.status, response.reason)
            conn.close()

        except Exception as e:
            print("Erro ao processar:", e)

except serial.SerialException as e:
    print("Erro ao abrir porta serial:", e)
