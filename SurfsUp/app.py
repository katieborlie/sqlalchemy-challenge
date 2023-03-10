# Import Dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#1
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Here are the Available Routes:<br/>"
        f"<br/>"
        f"Precipitation Data for the Last 12 Months:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"A List of Weather Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"The Dates/Temperature Observations of the Most-Active Station for the Previous Year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The Minimum, Average, and Maximum Temperature for a specified Start Date (Format:yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"The Minimum, Average, and Maximum Temperatures for a specified Start and End Date (Format:yyyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/<start>/<end>"
    )

#2
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    # Retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago_date).all()
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary 
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)
        
    return jsonify(prcp_data)

#3
@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Retrieve data for all stations
    stations = session.query(Station.name, Station.station, Station.elevation, Station.latitude, Station.longitude).all()
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary 
    station_data = []
    for name, station, elevation, latitude, longitude in stations:
        station_dict = {}
        station_dict["Name"] = name
        station_dict["Station ID"] = station
        station_dict["Elevation"] = elevation
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_data.append(station_dict)
        
    return jsonify(station_data)

#4
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set
    year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    # Retrieve the dates and temperature observations of the most active station for the previous year of data
    active_station = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                            filter(measurement.date >= year_ago_date).all()
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary
    most_active = []
    for date, temp in active_station:
        active_dict = {}
        active_dict[date] = temp
        most_active.append(active_dict)
        
    return jsonify(most_active)

#5a
@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Retrieve the minimum, maximum, and average temperature for a specified start date to the end of the dataset
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).all()
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary
    start_date = []
    for min, max, avg in query_results:
        start_dict = {}
        start_dict["Minimum Temperature"] = min
        start_dict["Maxium Temperature"] = max
        start_dict["Average Temperature"] = avg
        start_date.append(start_dict)
        
    return jsonify(start_date)

#5b
@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Retrieve the minimum, maximum, and average temperature for a specified start date to the end of the dataset
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary 
    range_date = []
    for min, max, avg in query_results:
        range_dict = {}
        range_dict["Minimum Temperature"] = min
        range_dict["Maxium Temperature"] = max
        range_dict["Average Temperature"] = avg
        range_date.append(range_dict)
        
    return jsonify(range_date)
    
if __name__ == '__main__':
    app.run(debug=True)