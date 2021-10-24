import os
import subprocess

curent = os.getcwd()
stor_loc = curent + "/Storage/storage_server.py"
berg = curent + "/WeatherStations/bergen.py"
osl = curent + "/WeatherStations/oslo.py"
trond = curent + "/WeatherStations/trondheim.py"
print(curent)
subprocess.call(['sh', './FMImac.sh', curent, stor_loc, berg, osl, trond, "export FLASK_APP=FMI/flask/app.py", "flask run"])