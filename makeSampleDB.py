import sqlite3
from aux import PlotAllGraphs
import os

# tuplas (Id, Local)
sensors = [
    (1, "LINF"),
    (2, "LABCE"),
    (3, "CASESO"),
]

# tuplas (Valor, Tipo, TimeStamp, Sensor)
data = [
    (10, 1, 120, 1),
    (20, 1, 130, 1),
    (15, 1, 420, 1),

    (10, 2, 120, 1),
    (15, 2, 130, 1),
    (50, 2, 140, 1),

    (50, 3, 50, 1),
    (20, 3, 100, 1),
    (1, 3, 190, 1),

    # dados para sensor 2
    (40, 1, 120, 2),
    (30, 1, 130, 2),
    (18, 1, 420, 2),

    (100, 2, 120, 2),
    (150, 2, 130, 2),
    (150, 2, 140, 2),

    (30, 3, 50, 2),
    (29, 3, 100, 2),
    (3, 3, 190, 2),

    # dados para sensor 3
    (13, 1, 120, 3),
    (22, 1, 130, 3),
    (5, 1, 420, 3),

    (80, 2, 120, 3),
    (69, 2, 130, 3),
    (30, 2, 140, 3),

    (40, 3, 50, 3),
    (70, 3, 100, 3),
    (15, 3, 190, 3),

]

if(os.path.exists("sampleDB.db")):
    os.remove("sampleDB.db")

file = open("sampleDB.db", 'w')
file.close()
    
connection = sqlite3.connect("sampleDB.db")
cursor = connection.cursor()

db_creation_script = open("db_script.txt", 'r')
db_creation_command = db_creation_script.read().split("--")

cursor.execute(db_creation_command[0])
cursor.execute(db_creation_command[1])

db_creation_script.close()

for sensor in sensors:
    cursor.execute(f"Insert into Sensores(Id, Local) values ({sensor[0]}, '{sensor[1]}');")

for record in data:
    cursor.execute(f"Insert into Registros(Valor, Tipo, TimeStamp, Sensor) values ({record[0]}, {record[1]}, {record[2]}, {record[3]});")

connection.commit()
connection.close()

PlotAllGraphs()
