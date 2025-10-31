import sqlite3
from bs4 import BeautifulSoup as Soup
import matplotlib.pyplot as plt

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

        cursor.execute(f"SELECT Valor FROM Registros WHERE (Sensor={sensorId} AND Tipo=1);")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT TimeStamp FROM Registros WHERE (Sensor={sensorId} AND Tipo=1);")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT Valor FROM Registros WHERE (Sensor={sensorId} AND Tipo=2);")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT TimeStamp FROM Registros WHERE (Sensor={sensorId} AND Tipo=2);")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT Valor FROM Registros WHERE (Sensor={sensorId} AND Tipo=3);")
        DataList.append(cursor.fetchall())

        cursor.execute(f"SELECT TimeStamp FROM Registros WHERE (Sensor={sensorId} AND Tipo=3);")
        DataList.append(cursor.fetchall())

        connection.close()
        print(DataList)
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
        list.insert_after(li)

    list_pointer = 0
    li_tags = soup.find_all("li")

    for li in li_tags:
        button = soup.new_tag("button")
        button.string = f"{SensorList[list_pointer][0]} - {SensorList[list_pointer][1]}"
        button["onclick"] = f"setCurrentId('{SensorList[list_pointer][0]}')"
        button["class"] = "btn btn-warning"
        list_pointer += 1

        li.append(button)

    return str(soup)

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
        return True # indica que registro foi criado

    except:
        return False


def MakeGraphsForSensor(sensorId):

    DataList = RetrieveSensorData(sensorId)
    # Colunas: 0-Valores tipo 1; 1-TimeStamps tipo 1; 2-Valores tipo 2; 3-TimeStamps tipo 2; 4-Valores tipo 3; 5-TimeStamps tipo 3

    ValoresTipo1 = DataList[0]
    TimesTipo1 = DataList[1]

    plt.plot(TimesTipo1, ValoresTipo1)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Valor")
    plt.title("Medidas de temperatura")
    plt.savefig(f"static/tempGraph/{sensorId}.png")
    plt.clf()

    ValoresTipo2 = DataList[2]
    TimesTipo2 = DataList[3]

    plt.plot(TimesTipo2, ValoresTipo2)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Valor")
    plt.title("Medidas de poeira")
    plt.savefig(f"static/dustGraph/{sensorId}.png")
    plt.clf()

    ValoresTipo3 = DataList[4]
    TimesTipo3 = DataList[5]

    plt.plot(TimesTipo3, ValoresTipo3)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Valor")
    plt.title("Medidas de umidade")
    plt.savefig(f"static/umiGraph/{sensorId}.png")
    plt.clf()

    return

def PlotAllGraphs():

    SensorList = RetrieveSensors()
    for sensor in SensorList:
        MakeGraphsForSensor(sensor[0]) # tupla (Id, local)

    return
    

    
    