# INF142-assignment1-Groupe-14

## PROJECT ARCHITECTURE: 

![](Documentation/FMI%20Architecture%20.png | width=100)

## Demo

https://user-images.githubusercontent.com/53192344/138603265-29035420-35d0-4971-a4a2-c3b8e27c3473.mov


## PROJECT EXPLANATION:
The project consists of three main parts: Weather Stations, Storage and FMI.
#### **Weather Stations:**
There are three weather stations, one in Bergen, one in Trondheim and one in Oslo, which all sends data through a individual UDP connection to Storage. The three weather stations collects its data from a station simulator. 
#### **Storage:**
Storage consists of two parts. The storage connector and MongoDB. The storage connector acts as a middle man and server for both TCP/UDP requests. The input is forwarded to MongoDB, a cloudbased database where the data is stored.
#### **FMI:**
We chose Flask to visualize the data. The web server makes sure the requests forwarded to storage and MongoDB are uniform and easy to handle. Flask communicates with storage through a TCP-connection. Request and response, between Flask and Storage, are both sent through TCP as a json-string.

We have fulfilled the MVP requirements:
- It consists of at least three Python scripts, one for each of the aforementioned processes.
- At least one TCP socket is used.
- At least one UDP socket is used.
- The provided script station.py is used by the weather stations processes to simulate the readings of weather sensors.
- The storage server process periodically stores data in a file or database.
- The storage server process provides remote access to the stored data.
- The FMI process (user agent) runs in a CLI and, upon request, displays all the data available in the storage server.

We have added these extra features:
- Flask
- MongoDB

## PREREQUISITES:
Before running the program you have to download all the pythonpackages written in requirements.txt by running the code:
- **Mac:** pip install -r requirements.txt
- **Windows:** python -m pip install -r requirements.txt


## RUNNING: 

We've been able to create a run-file for Mac, unfortunaltly it is not fuctioning properly for Windows. So for mac, you only have to run the python script run.py. This file will open a new termial window for each of the files that needs to be executed (storage_server.py, bergen.py, oslo.py, etc.). The terminal windows might be hiding behind each other, so they should be dragged to different locations.

The program will take some time to simulate the weather data, around 10 min (depending on the computer), so be patient. If you check January or All first, you will be able to visualize the first data sent from the weather stations. However, if you check a month that has not yet have been generated, it will not work.

### MAC: 
- Step 1: Run run.py from terminal:

        python3 run.py

- Step 2: Open the url presented by the terminal (or open browser and go to http://localhost:5000/)
- Step 3: Enjoy weather data :) 

### WINDOWS: 
- Step 1: Run storage_server.py (found in Storage) from terminal:

        python Storage\storage_server.py

- Step 2: Run the following weather station files (each from separate terminals):

        python WeatherStations\bergen.py 
        python WeatherStations\trondheim.py
        python WeatherStations\oslo.py

- Step 3: Run Flask from new terminal by using these commands in order: 

        cd FMI\flask
        $env:FLASK_APP = "app.py"
        python -m flask run

- Step 4: Open the url presented by the terminal (or open browser and go to http://localhost:5000/)
- Step 5: Enjoy weather data :) 



