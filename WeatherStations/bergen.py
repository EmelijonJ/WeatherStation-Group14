from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM
from station import StationSimulator

if __name__ == "__main__":

    # Instantiate a station simulator
    station = StationSimulator(simulation_interval=1, location= "Bergen")
    
    # Turn on the simulator
    station.turn_on()
    
    # Two lists for months and days
    months = list(station._days_of_month.keys())
    days = list(station._days_of_month.values())

    # Instantiate the UDP-socket
    socket = socket(AF_INET, SOCK_DGRAM)

    # Capture data for 365 days
    for i in range(len(months)):
        for j in range(days[i]):

            # Sleep for 1 second to wait for new weather data to be simulated
            sleep(1)
            
            #Collected data
            data = {}
            data.update({
            'location': station.location,
            'month': months[i],
            'day': (j+1),
            'temperature': station.temperature,
            'precipitation': station.rain,  
            })

            ## Send to storage with UDP
            text = str(data) # dict to string
            socket.sendto(text.encode(), ('localhost', 55554)) # Send data to the socket. Return the number of bytes sent.
            msg, adr = socket.recvfrom(2048)
            print(msg.decode())
        
    # Shut down the simulation
    station.shut_down()