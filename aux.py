import sqlite3
from bs4 import BeautifulSoup as Soup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import time

DB_file = "sampleDB.db"

def RetrieveSensors():

    try:
        connection = sqlite3.connect(DB_file)
        cursor = connection.cursor()

        cursor.execute("SELECT Id, Local from Sensores;")
        data = cursor.fetchall()

        connection.close()
        return data

    except sqlite3.Error as e:
        connection.close()
        print("An error has ocurred: ", e)

def RetrieveSensorData(sensorId):

    DataList = []

    try:
        connection = sqlite3.connect(DB_file)
        cursor = connection.cursor()

        cursor.execute(f"SELECT Valor FROM Registros WHERE (Sensor={sensorId} AND Tipo=1) ORDER BY TimeStamp DESC LIMIT 5;")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT TimeStamp FROM Registros WHERE (Sensor={sensorId} AND Tipo=1) ORDER BY TimeStamp DESC LIMIT 5;")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT Valor FROM Registros WHERE (Sensor={sensorId} AND Tipo=2) ORDER BY TimeStamp DESC LIMIT 5;")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT TimeStamp FROM Registros WHERE (Sensor={sensorId} AND Tipo=2) ORDER BY TimeStamp DESC LIMIT 5;")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT Valor FROM Registros WHERE (Sensor={sensorId} AND Tipo=3) ORDER BY TimeStamp DESC LIMIT 5;")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT TimeStamp FROM Registros WHERE (Sensor={sensorId} AND Tipo=3) ORDER BY TimeStamp DESC LIMIT 5;")
        DataList.append(cursor.fetchall())

        connection.close()
        return DataList

    except sqlite3.Error as e:
        connection.close()
        print("An error has ocurred: ", e)


def AddSensors(HTML_file):

    SensorList = RetrieveSensors()
    soup = Soup(HTML_file)
    list = soup.find("ul")


    for i in range(0, len(SensorList)):
        li = soup.new_tag("li")
        li['class'] = "nav-item p-2 mb-1 m-auto"
        list.append(li)

    list_pointer = 0
    li_tags = soup.find_all("li")

    for li in li_tags:
        button = soup.new_tag("button")
        li["id"] = SensorList[list_pointer][0]
        button.string = f"{SensorList[list_pointer][0]} - {SensorList[list_pointer][1]}"
        button["onclick"] = f"setCurrentId('{SensorList[list_pointer][0]}')"
        button["class"] = "btn btn-info"
        list_pointer += 1

        li.append(button)

    return str(soup)

def GetActiveSensors():
    try:
        connection = sqlite3.connect(DB_file)
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT(Sensor) from Transmissions where (strftime('%s','now') - TimeStamp)<1800;")
        activeSensors = cursor.fetchall()
        activeSensors = [item[0] for item in activeSensors]

        connection.close()
        return activeSensors

    except:
        connection.close()
        print("an error has ocurred in the DB")

def InsertTransmissionRow(SensorId):
    try:
        connection = sqlite3.connect(DB_file)
        cursor = connection.cursor()

        # primeiro verificar se já existe registro para o sensor na tabela Transmissions
        cursor.execute(f"Select * from Transmissions where Sensor={SensorId};")
        if(cursor.fetchall() == ([]) ):
            # nesse caso ainda não há registro e precisamos criar um
            cursor.execute(f"Insert into Transmissions(TimeStamp,Sensor) values ({int(time.time())},{SensorId})")
        else:
            # nesse caso já existe um registro e precisamos alterar o timestamp
            cursor.execute(f"Update Transmissions set TimeStamp={int(time.time())} where Sensor={SensorId};")

        connection.commit()
        connection.close()
        return True
    except Exception as e:
        connection.close()
        print(e)
        return False


def CreateRegistryRow(json_data):
    try:
        connection = sqlite3.connect(DB_file)
        cursor = connection.cursor()
        command = f"""
            Insert into Registros(Valor, Sensor, Tipo, TimeStamp)
            values
            ({json_data["Valor"]}, {json_data["Sensor"]}, {json_data["Tipo"]}, {json_data["TimeStamp"]});
            """
        cursor.execute(command)
        connection.commit()
        connection.close()

        print("Registro feito")

        if( not(InsertTransmissionRow(int(json_data["Sensor"]))) ):
            raise RuntimeError("Erro no registro da transmissão")


        MakeGraphsForSensor(int(json_data["Sensor"]))
        print("Made graphs")

        return True # indica que registro foi criado

    except Exception as e:
        print(e)
        return False


def MakeGraphsForSensor(sensorId):

    DataList = RetrieveSensorData(sensorId)
    # Colunas: 0-Valores tipo 1; 1-TimeStamps tipo 1; 2-Valores tipo 2; 3-TimeStamps tipo 2; 4-Valores tipo 3; 5-TimeStamps tipo 3

    ValoresTipo1 = DataList[0]
    TimesTipo1 = DataList[1]
    DateTimes1 = [datetime.fromtimestamp(t[0]) for t in TimesTipo1]

    print(DateTimes1)

    plt.plot(DateTimes1, ValoresTipo1)
    plt.xlabel("Mes-Dia Hora:Minuto")
    plt.ylabel("Valor")
    plt.title("Medidas de temperatura")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.savefig(f"static/tempGraph/{sensorId}.png")
    plt.clf()

    ValoresTipo2 = DataList[2]
    TimesTipo2 = DataList[3]
    DateTimes2 = [datetime.fromtimestamp(t[0]) for t in TimesTipo2]

    plt.plot(DateTimes2, ValoresTipo2)
    plt.xlabel("Mes-Dia Hora:Minuto")
    plt.ylabel("Valor")
    plt.title("Medidas de poeira")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.savefig(f"static/dustGraph/{sensorId}.png")
    plt.clf()

    ValoresTipo3 = DataList[4]
    TimesTipo3 = DataList[5]
    DateTimes3 = [datetime.fromtimestamp(t[0]) for t in TimesTipo3]

    plt.plot(DateTimes3, ValoresTipo3)
    plt.xlabel("Mes-Dia Hora:Minuto")
    plt.ylabel("Valor")
    plt.title("Medidas de umidade")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()
    plt.savefig(f"static/umiGraph/{sensorId}.png")
    plt.clf()

    return

def PlotAllGraphs():

    SensorList = RetrieveSensors()
    for sensor in SensorList:
        MakeGraphsForSensor(sensor[0]) # tupla (Id, local)

    return
    

    
    