#import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the measurement and station tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#create an app, being sure to pass __name__
app = Flask(__name__)

#define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api.v1.0/start<br/>"
        f"/api.v1.0/end<br/>"
    )

#Create a route for precipitation levels and dates using dictionary format
@app.route("/api/v1.0/precipitation")
def precipitation():
#Create a session link from Python to the database
    session = Session(engine)

    precip_query_results = session.query(Measurement.prcp, Measurement.date).all()

#Close session
    session.close()
    p = {date:prcp}
    return jsonify(p)
#create a route that returns a JSON list of stations
@app.route("/api.v1.0/stations")
def stations():

#create new session link for stations
    session = Session(engine)

    station_query_results = session.query(Station.station, Station.id).all()

#close session
    session.close()

#dictionary for query results
    station_results = []
    for station, id in station_query_results:
        station_values_dict = {}
        station_values_dict["station"] = station
        station_values_dict["id"] = id
        station_results.append(stations_values_dict)
        return jsonify (station_results)

#create a route that queries dates and temperature observations
@app.route("/api/v1.0/tobs")
def tobs():

#create new session link
    session = Session(engine)

#create a query for data and temperature data
    temp_obs_yearly = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()

    print(temp_obs_yearly)

#create dictionary for results
    temp_obs_results = []
    temp_values_dict = {}
    temp_values_dict["date"] = date
    temp_obs_results.append(temp_values_dict)

    temp_obs_start_date = dt.date(2017, 8, 23)-dt.timedelta(days = 365)
    print(temp_obs_start_date)

#define
# Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

@app.route("/api/v1.0/<start>/<end>")

# define function, set start and end dates entered by user
def start_end_date(start, end):
    session = Session(engine)

 #create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL

    start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

#create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_tobs_date_values = []
    for min, avg, max in start_end_date_tobs_results:
        start_end_tobs_date_dict = {}
        start_end_tobs_date_dict["min_temp"] = min
        start_end_tobs_date_dict["avg_temp"] = avg
        start_end_tobs_date_dict["max_temp"] = max
        start_end_tobs_date_values.append(start_end_tobs_date_dict)
        return jsonify(start_end_tobs_date_values)


if __name__ == "__main__":
    app.run(debug=True)
