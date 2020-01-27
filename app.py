import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#creating database and reflections
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#create session
session = Session(engine)
    
Measurement = Base.classes.measurement
Station = Base.classes.station


# setup flask & routes
app = Flask(__name__)
#list available routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipinfo = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date > last_year).\
        order_by(Measurements.date).all()

    precip_totals = []
    for i in precipinfo:
        row = {}
        row["date"] = precipinfo[0]
        row["prcp"] = precipinfo[1]
        precip_totals.append(row)
    return jsonify(precip_totals)

@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature_observations = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date > last_year).\
        order_by(Measurements.date).all()

    temperature_totals = []
    for i in temperature_observations:
        row = {}
        row["date"] = temperature_observations[0]
        row["tobs"] = temperature_observations[1]
        temperature_totals.append(row)

    return jsonify(temperature_totals)

@app.route("/api/v1.0/<start>")
#eturn a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

def startdateonly(start):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

def startandend(start,end):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == '__main__':
    app.run(debug=True)