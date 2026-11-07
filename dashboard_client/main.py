import serial as ser                           # - Pyserial, Used for data ingestion
import re                                      # - Regex, 'Regular Expressions' will parse through the overall string
import matplotlib.pyplot as plt                # - Used to plot and display the information
import matplotlib.animation as anim            # - Used to display the information in real-time as opposed to static

 # - Establishing the connection, hardcoded values for now
PORT = "COM3"
BAUD_RATE = 115200
cnx = ser.Serial(PORT, BAUD_RATE)
# Time: 1474000 ms, Pres: 25 hPa, Stat: 1, Temp: 78.0 C

data_pattern = r"Time: (\d+) ms, Pres: ([\d\.]+) hPa, Stat: (\d), Temp: ([\d\.]+) C" # - The pattern used by re to parse the telemetry stream

packets = {                 # - Packet dictionary stores the data pulled from the stream
    "timestamps"            : [],
    "pressure_readings"     : [],
    "status_updates"        : [],
    "temperature_readings"  : []}

def core(frame):
    # - Grabbing the signal from the board, decoding it into human-readable language and removing carriage return and line feed characters
    data_stream = cnx.readline().decode('utf-8').strip()
    print(data_stream)
    match = re.search(data_pattern, data_stream) # - Scouring the data stream for potential matches

    # - Match groups
    if match:
        timestamp = float(match.group(1)) # - Grabs the first set of ()
        timestamp = (timestamp / 1000) # -  Converting to seconds
        timestamp = (timestamp / 60) # -  Converting to seconds
        packets["timestamps"].append(timestamp) # - Adding the latest time to the list
        
        pres_read = float(match.group(2))
        packets["pressure_readings"].append(pres_read) 

        sys_status = int(match.group(3)) 
        packets["status_updates"].append(sys_status) 

        temp_read = float(match.group(4))
        packets["temperature_readings"].append(temp_read) 

    ax.clear()
    ax.plot(packets["timestamps"],packets["temperature_readings"])

fig, ax = plt.subplots()
animated = anim.FuncAnimation(fig, core, interval=100)
plt.show()