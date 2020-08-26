###importing all dependencies 

from flask import Flask, jsonify

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List of all api routes that are available for use"""
    return (
         f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Create a list of all unique stations
    # numpy ravel is used to change a 2-dimensional array into a flattened array (the station numbers)
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of relevant temperature data"""
    # Query temperature at the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    temp_obs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        temp_obs.append(tobs_dict)

    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start_temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data with start date only"""
    # Query temperature min, max, and avg from a start date
    temp_min = func.min(Measurement.tobs)
    temp_max = func.max(Measurement.tobs)
    temp_avg = func.avg(Measurement.tobs)
    avgs = [temp_min, temp_max, temp_avg]
    results = session.query(*avgs).filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of all temperatures
    temp_results = []
    for temp_min, temp_max, temp_avg in results:
        tdr_dict = {}
        tdr_dict["Lowest Temp"] = temp_min
        tdr_dict["Highest Temp"] = temp_max
        tdr_dict["Average Temp"] = temp_avg
        temp_results.append(tdr_dict)

    return jsonify(temp_results)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data with start and end dates"""
    # Query temperature min, max, and avg between a start and end date
    temp_min = func.min(Measurement.tobs)
    temp_max = func.max(Measurement.tobs)
    temp_avg = func.avg(Measurement.tobs)
    avgs = [temp_min, temp_max, temp_avg]
    results = session.query(*avgs).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of all temperatures
    temp_results2 = []
    for temp_min, temp_max, temp_avg in results:
        tdr_dict = {}
        tdr_dict["Lowest Temp"] = temp_min
        tdr_dict["Highest Temp"] = temp_max
        tdr_dict["Average Temp"] = temp_avg
        temp_results2.append(tdr_dict)

    return jsonify(temp_results2)

if __name__ == '__main__':
    app.run(debug=True)




    
