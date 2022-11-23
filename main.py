from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)


stations = pd.read_csv("data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route('/')
def home():
	return render_template("home.html", data=stations.to_html())


# One Specific Date and Station
@app.route('/api/v1/<station>/<date>')
def data(station, date):
	# READING DATA FILES
	filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
	df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
	# GET CERTAIN CELL (TEMPRERATURE) FROM DATA FRAME
	temperature = df.loc[df['    DATE']==date]['   TG'].squeeze() / 10
	return {"station":station,
	        "date":date,
	        "temperature":temperature}


# One Specific Station and whole period
@app.route('/api/v1/<station>')
def for_station(station):
	# READING DATA FILES
	filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
	df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
	result = df.to_dict(orient="records")
	return result


# One Specific Station and Year
@app.route('/api/v1/yearly/<station>/<year>')
def for_year(station, year):
	# READING DATA FILES
	filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
	df = pd.read_csv(filename, skiprows=20)
	df["    DATE"] = df["    DATE"].astype(str)
	result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
	return result



if __name__=="__main__":
    app.run(debug=True)