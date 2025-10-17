from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"



db = SQLAlchemy(app)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(100))

    def __repr__(self):
        return f"Sensor:{self.id}"
    
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    sensor = db.Column(db.Integer, db.ForeignKey("sensor.id"), nullable=False)
    tipo = db.Column(db.Integer)

@app.route('/')
def index():

    sensors = Sensor.query.all()
    return render_template("index.html", sensorList=sensors)

if(__name__ == "__main__"):
    with app.app_context():
        db.create_all()
    app.run(debug=True)