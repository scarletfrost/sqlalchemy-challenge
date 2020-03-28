from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)



@app.route("/")
def home():
     return (
        f"Be prepared for your long vacation in Honolulu, Hawaii! Here is a climate analysis on the area to help with your trip planning.<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Precipitation readings:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations (tobs) for the previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"List of the min temperature, the average temperature, and the max temperature for a given start or start-end range:<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )



# 4. Define what to do when a user hits the route
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    all_prcp = []
    for date, prcp in results:
        all_dict = {}
        all_dict["date"] = date
        all_dict["prcp"] = prcp
        all_prcp.append(all_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    last=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    laststr=str(last[0])
    lastdate=datetime.strptime(laststr , '%Y-%m-%d')
    year_ago = lastdate - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).filter(Measurement.date <= lastdate).order_by(Measurement.date).all()
    all_tobs = []
    for date, tobs in results:
        all_dict = {}
        all_dict["date"] = date
        all_dict["tobs"] = tobs
        all_tobs.append(all_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def weather(start):

    session = Session(engine)
    resultsdate = session.query(Measurement.date)
    all_dates = list(np.ravel(resultsdate))
    results = session.query(func.min(Measurement.tobs).label('min_tobs'), func.avg(Measurement.tobs).label('avg_tobs'), func.max(Measurement.tobs).label('max_tobs')).filter(Measurement.date>=start).all()
    all_results = list(np.ravel(results))
    return jsonify(all_results)

    

@app.route("/api/v1.0/<start>/<end>")
def weather2(start, end):

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs).label('min_tobs'), func.avg(Measurement.tobs).label('avg_tobs'), func.max(Measurement.tobs).label('max_tobs')).filter(Measurement.date>=start).filter(Measurement.date <= end).all()
    all_results = list(np.ravel(results))
    return jsonify(all_results)


if __name__ == "__main__":
    app.run(debug=True)
