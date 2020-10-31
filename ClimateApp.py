from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from pprint import pprint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import and_, or_, extract
import os

from flask import Flask, jsonify

Base = declarative_base()

engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")
session = Session(engine)
conn = engine.connect()

class meas(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)
    
class sta(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

Measurement = meas
Station = sta

# Get date one year from last date in the dataset
one_year = dt.timedelta(days=365)
max_date = session.query(func.max(Measurement.date)).first()[0]
start_date = max_date - one_year
start_date = start_date.isoformat()

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        "Welcome to the Hawaii Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).all()

    dict_precip = {}
    for i in precipitation:
        dict_precip[str(i[0])] = i[1]

    return jsonify(dict_precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
   
    # Get all temperature observations (tobs) from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= start_date).all()

    temps_12months = f"SELECT m.station, m.date, m.tobs FROM measurement as m WHERE m.date >= '{start_date}';"
    most_tobs = """SELECT m.station, count(m.tobs) FROM measurement as m
        GROUP BY m.station
        ORDER BY count(m.tobs) DESC;
        """
    df_most_tobs = pd.read_sql(most_tobs, conn)
    station_highest_count_tobs = df_most_tobs["station"][0]

    tobs_12mo = f"""SELECT m.tobs FROM measurement as m 
        WHERE m.date >= '{start_date}'
        and m.station == '{station_highest_count_tobs}';
        """
    df_tobs_12mo = pd.read_sql(tobs_12mo, conn)

    temps = list(np.ravel(df_tobs_12mo))

    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start when no end date provided
        results = session.query(*sel).\
            filter(Measurement.date >= start_date).all()
        # send results to a list
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)
