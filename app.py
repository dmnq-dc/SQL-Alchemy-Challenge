#Import and Set-Up Dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Create engine from sqlalchemy module
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Create Base using automapping
Base = automap_base()

Base.prepare(engine, reflect=True)

#Reflect tables from the database -hawaii.sqlite
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Create web app using Flask
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes for Hawaii Weather Data:<br/><br>"
        f"Precipitation: /api/v1.0/precipitation><br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Most Active Station Data on Temperature:/api/v1.0/tobs<br/>"
        f"Temperature from the start date: /api/v1.0/yyyy-mm-dd <br/>"
        f"Temperature from start to end dates: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the database
    session = Session(engine)

    """Return a list of all daily precipitation totals for the last year"""
    
    # Query and summarize daily precipitation across all stations for the last year of available data
    sel = [measurement.date, measurement.prcp]
    result = session.query(*sel).all()
   
    session.close()

    # Return a dictionary with the date as key and the daily precipitation total as value
    precipitation= []

    for date, prcp in result:
        prcp_dict = {}
        prcp_dict ["Date"] = date
        prcp_dict ["Precipitation"] = prcp
        precipitation.append(prcp_dict)
    
    #return the JSonified list
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the active Weather stations in Hawaii"""
    # Return a list of active weather stations in Hawaii
    sel = [measurement.station]
    active_stations = session.query(*sel).\
        group_by(measurement.station).all()
    session.close()

    # Convert list of tuples into normal list and return the JSonified list
    list_of_stations = list(np.ravel(active_stations)) 
    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the last 12 months of temperature observation data for the most active station
    date_str = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(date_str, '%Y-%m-%d') #conversion to datetime
    query_date = dt.date(latest_date.year -1, latest_date.month, latest_date.day)

    sel = [measurement.date, measurement.tobs]

    result = session.query(*sel).filter(measurement.date >= query_date).all()

    session.close()

    # Return a dictionary with the date as key and the daily temperature observation as value
    temperature = []

    for date, tobs in result:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Tobs"] = tobs

        temperature.append(temp_dict)

    #return the JSonified list
    return jsonify(temperature)

@app.route("/api/v1.0/<start>")
def trip_start(start):
    session = Session(engine)
    start = '2016-08-23'
    query_all = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    session.close()

    temp_all = []
    for min, avg, max in query_all:
        temp_all_dict = {}
        temp_all_dict ["Min"] = min
        temp_all_dict ["Average"] = avg
        temp_all_dict ["Max"] = max

        temp_all.append(temp_all_dict)
    
    #return the JSonified list
    return jsonify(temp_all)

@app.route('/api/v1.0/<start>/<end>')
def trip_start_end (start,end = '2017-08-23'):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    tobsall = []
    for min,avg,max in query_result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)
  
if __name__ == '__main__':
    app.run(debug=True)