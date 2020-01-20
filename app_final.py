
#dependency
import numpy as np
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect
import datetime as dt
from flask import Flask, jsonify
#db setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
#reflect
Base.prepare(engine,reflect=True)
#Save references
Measurement = Base.classes.measurement
Station = Base.classes.station
#Session
session=Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"-When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns a list of amounts of precipitation with dates"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23','2017-08-23')).order_by(Measurement.date).all()
    p_dict= {date:prcp for date,prcp in results}
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(p_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of stations"""
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(stations.to_dict())


@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a list of amounts of tobs with dates"""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()
    tobs_dict= {date:tobs for date,tobs in results}
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(day_temp_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(multi_day_results)

if __name__ == '__main__':
    app.run(debug=True)
    






