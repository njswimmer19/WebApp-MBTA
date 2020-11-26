from flask import Flask, render_template, request
from mbta_helper import find_stop_near


app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route('/nearest/', methods=['GET','POST'])
def nearest():

    if request.method == "POST":
        place_name = str(request.form['place'])
        mbta_station = find_stop_near(place_name)
        station = mbta_station[0]
        wheelchair_accessible = mbta_station[1]

        if mbta_station:
            return render_template(
                "result.html",
                place_name = place_name,
                station = station,
                wheelchair_accessible = wheelchair_accessible
            )
        else:
            return render_template("form.html", error = True)

    return render_template("form.html", error = None)

if __name__ == '__main__':
    app.run()