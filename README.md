# SQL-Alchemy-Challenge
Week 10 Module Challenge

Part 1: Analyse and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

Use the SQLAlchemy create_engine() function to connect to your SQLite database.
Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
Link Python to the database by creating a SQLAlchemy session.

Precipitation Analysis
Find the most recent date in the dataset.
Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
Select only the "date" and "prcp" values.
Load the query results into a Pandas DataFrame, and set the index to the "date" column.
Sort the DataFrame values by "date".
Plot the results by using the DataFrame plot method.
Use Pandas to print the summary statistics for the precipitation data.

Station Analysis
Design a query to calculate the total number of stations in the dataset.
Design a query to find the most-active stations (that is, the stations that have the most rows)
Design a query to get the previous 12 months of temperature observation (TOBS) data.

------------------------------------------------------------------------
Part 2: Design Your Climate App
Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed.
1. Home page - /
2. Precipitation - /api/v1.0/precipitation
3. Stations - /api/v1.0/stations
4. Temperature - /api/v1.0/tobs
5. Temperature on Specific Dates - /api/v1.0/<start> and /api/v1.0/<start>/<end>
