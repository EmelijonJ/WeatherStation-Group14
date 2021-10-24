import pickle
from flask import Flask, render_template, request, redirect, url_for
from socket import create_connection
from statistics import mean
from bson.json_util import dumps


app = Flask(__name__)


months = ['January', "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


@app.route("/", methods=["GET", "POST"])
def index():
    """
    This is the home page and will send you to the another route based on the selection of the end-user.
    """
    if request.method == "POST":
        city, month, view = request.form["city"], request.form["month"], request.form["view"]
        if view == "table":
            return redirect(url_for("table", city=city, month=month))
        elif view == "graph":
            return redirect(url_for("graph", city=city, month=month))
    return render_template("index.html", months=months)


@app.route("/graph/<city>/<month>")
def graph(city, month):
    """
    Selection from the end-user is passed here and average temp and precipitation is sendt to html page.
    This route gives us the graph page.
    """
    # send a query based on the the selection of end-user
    if month == "All":
        query = {"location": city.capitalize()}
        data = tcp_client(query)
    else:
        query = {"location": city.capitalize(), "month": month}
        data = tcp_client(query)

    # Labels and data is beeing stored as list
    labels = [str(i["day"]) + "" + i["month"] for i in data]
    values = [i["temperature"] for i in data]
    values1 = [i["precipitation"] for i in data]

    # Calculating average
    avg_temp = round(mean([i["temperature"] for i in data]), 2)
    avg_prec = round(mean([i["precipitation"] for i in data]), 2)

    return render_template("graph.html", labels=labels, values=values, values1=values1,
                           avg_temp=avg_temp, avg_prec=avg_prec, city=city.capitalize(), month=month)


def tcp_client(query):
    """
    This is the tcp client which will connect with storage.
    The TCP client will send a json string which hold the information about what is requested.
    The tcp Server will then send back a message that will tell the client how big the string is.
    The tcp client will run until the whole message is received.
    """
    header = 10

    sock = create_connection(("localhost", 5550))
    json_t = dumps(query)

    sock.send(json_t.encode())
    print(json_t, 'was sent!')

    while True:
        full_msg = b""
        new_msg = True
        while True:
            msg = sock.recv(1024)
            if new_msg:
                msg_len = int(msg[:header])
                new_msg = False

            full_msg += msg

            if len(full_msg) - header == msg_len:
                Json = pickle.loads(full_msg[header:])

                new_msg = True
                full_msg = b""
                return Json


@app.route("/table/<city>/<month>")
def table(city, month):
    """
    Gets data based on end-user request.
    This function is for the table
    """
    query = {"location": city.capitalize(), "month": month}
    if month == "All":
        all_data = tcp_client({"location": city.capitalize()})
        avg_temp = round(mean([i["temperature"] for i in all_data]), 2)
        avg_prec = round(mean([i["precipitation"] for i in all_data]), 2)
        return render_template("table.html", all_data=all_data, avg_temp=avg_temp,
                               avg_prec=avg_prec, city=city.capitalize())
    else:
        if month in months:
            month_data = tcp_client(query)
            avg_temp = round(mean([i["temperature"] for i in month_data]), 2)
            avg_prec = round(mean([i["precipitation"] for i in month_data]), 2)
            return render_template("table.html", all_data=month_data,
                                   avg_temp=avg_temp, avg_prec=avg_prec, city=city.capitalize(), month=month)
        else:
            return redirect(url_for("/"))
