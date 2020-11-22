import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

################################
#Database Setup
################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base= automap_base()
Base.prepare(engine, reflect=True)

#tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

################################
#flask setup
################################
app = Flask(__name__)

################################
#Flask Routes
################################

#for the home page, List all routes that are available.
@app.route("/")
def home():
    return(f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")
 

#Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    precDictionary = list(np.ravel(precipitation))
    
    return jsonify(precDictionary)
         
    
#Return a JSON list of stations from the dataset.   
@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.station, Station.name).all()
    stationDictionary = list(np.ravel(station))
    return jsonify(stationDictionary)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    MAstation= 'USC00519281'
    tobs = session.query(Measurement.date, Measurement.tobs).\
           filter(Measurement.date>="2016-08-23").\
           filter(Measurement.date<="2017-08-23").\
           filter(Measurement.station == MAstation).all()
    tobsDictionary = list(np.ravel(tobs))
    return jsonify(tobs)
    
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def start(start):
    start_day = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    group_by(Measurement.date).all()

    # Convert List of Tuples Into Normal List
    start_day_list = list(start_day)
        
    return jsonify(start_day_list)
    

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    start_end_day = session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    group_by(Measurement.date).all()
    
    # Convert List of Tuples Into Normal List
    start_end_day_list = list(start_end_day)
        
    return jsonify(start_end_day_list)
    
    
if __name__ == "__main__":
    app.run(debug=True)
