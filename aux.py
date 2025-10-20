import sqlite3
from bs4 import BeautifulSoup as Soup

def RetrieveSensors():
    DB_file = "database.db"

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

def AddSensors(HTML_file):

    SensorList = RetrieveSensors()
    soup = Soup(HTML_file)
    list = soup.find("ul")


    for i in range(0, len(SensorList)):
        li = soup.new_tag("li")
        li['class'] = "nav-item p-2 mb-1"
        list.insert_after(li)

    list_pointer = 0
    li_tags = soup.find_all("li")

    for li in li_tags:
        button = soup.new_tag("button")
        button.string = f"{SensorList[list_pointer][0]} - {SensorList[list_pointer][1]}"
        button["onclick"] = f"setCurrentId('{SensorList[list_pointer][0]}')"
        list_pointer += 1

        li.insert_after(button)

    return str(soup)