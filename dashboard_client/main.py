import serial as ser                           # - Pyserial, Used for data ingestion
import re                                      # - Regex, 'Regular Expressions' will parse through the overall string
import matplotlib.pyplot as plt                # - Used to plot and display the information
import matplotlib.animation as anim            # - Used to display the information in real-time as opposed to static
import matplotlib.ticker as ticker             # - User for better formatting of the timestamp
import matplotlib.image as img                 # - Used to display images on the figure
import sys                                     # - System level functions

 # - Establishing the connection, hardcoded values for now
PORT = "COM3"
BAUD_RATE = 115200
cnx = ser.Serial(PORT, BAUD_RATE)

data_pattern = r"Time: (\d+) ms, Pres: ([\d\.]+) hPa, Stat: (\d), Temp: ([\d\.]+) C" # - The pattern used by re to parse the telemetry stream

packets = {                 # - Packet dictionary stores the data pulled from the stream
    "timestamps"            : [],
    "pressure_readings"     : [],
    "status_updates"        : [],
    "temperature_readings"  : []}

def user_clock(x, pos):  # - Converts ms to seconds, minutes, hours and days for a nicer display
        raw_timestamp = int(x)
        # - Milliseconds
        milliseconds =  raw_timestamp % 1000    # - Gets only the leftover ms with a modulo division
        raw_timestamp = raw_timestamp // 1000   # - Removes the milliseconds from the timestamp

        # - Seconds
        seconds =  raw_timestamp % 60
        raw_timestamp = raw_timestamp // 60 
        
        # - Minutes
        minutes =  raw_timestamp % 60
        raw_timestamp = raw_timestamp // 60 

        # - Hours
        hours =  raw_timestamp % 24   

        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{int(milliseconds):03d}"
    
def core(frame):
    # - Grabbing the signal from the board, decoding it into human-readable language and removing carriage return and line feed characters
    data_stream = cnx.readline().decode('utf-8').strip()
    match = re.search(data_pattern, data_stream) # - Scouring the data stream for potential matches

    # - Match groups
    if match:
        timestamp = float(match.group(1)) # - Grabs the first set of ()
        packets["timestamps"].append(timestamp) # - Adding the latest time to the list as a raw ms count
        
        pres_read = float(match.group(2))
        packets["pressure_readings"].append(pres_read) 

        sys_status = int(match.group(3)) 
        packets["status_updates"].append(sys_status)

        temp_read = float(match.group(4))
        packets["temperature_readings"].append(temp_read) 

    # - Clearing the board
    ax_temp.clear()
    ax_pressure.clear()
    ax_sys_status.clear()
    ax_sys_status.axis('off')
    
    # - Axes Settings

    # -  Temperature Plot
    ax_temp.set_title("Temperature", color='cyan')
    ax_temp.set_xlabel("Time", color='cyan')
    ax_temp.set_ylabel("Degrees in Celsius", color='cyan')
    ax_temp.xaxis.set_major_formatter(ticker.FuncFormatter(user_clock)) # -Formats the clock for user readability
    ax_temp.plot(packets["timestamps"],packets["temperature_readings"], color='crimson') # - Plots the temps

    # - Pressure Plot
    ax_pressure.set_title("Pressure", color='cyan')
    ax_pressure.set_xlabel("Time", color='cyan')
    ax_pressure.set_ylabel("Pressure in hPa", color='cyan')
    ax_pressure.xaxis.set_major_formatter(ticker.FuncFormatter(user_clock)) # -Formats the clock for user readability
    ax_pressure.plot(packets["timestamps"],packets["pressure_readings"], color='dodgerblue')

    # - System Status Plot
    if sys_status == 1:
         status = 'System: Nominal'
         status_color = 'limegreen'
    else:
         status = 'System: Unknown'
         status_color = 'black'

    ax_sys_status.text(
         0.5, 0.5, status,
         color = status_color,
         fontweight='bold',
         fontsize = 10,
         family = 'consolas',
         ha='center', va='center',
         bbox = dict(boxstyle='round,pad=0.5', facecolor='#111111', edgecolor=status_color, lw=1.5))
           
fig, (ax_temp, ax_pressure) = plt.subplots(2,1, figsize=(14,7))
ax_sys_status = fig.add_axes([0.83, 0.02, 0.15, 0.08]) # - Adds the system status to the bottom right corner
fig.suptitle("NUCLEO - F446RE - Real-Time System Telemetry", fontsize=16, y=0.95, color='cyan', fontweight='bold', family='consolas')
fig.patch.set_facecolor('#4A4A4A')

# - Changing the colors of the plots
for ax in (ax_temp, ax_pressure):
     ax.set_facecolor('#000000') # - Sets the background color for the plots
     ax.tick_params(colors='cyan')
     ax.xaxis.label.set_color('cyan')
     ax.yaxis.label.set_color('cyan')
     ax.title.set_color('cyan')
     for spine in ax.spines.values():
          spine.set_edgecolor('#FFFFFF')

board_display = img.imread('assets/board.png')
ax_img = fig.add_axes([0.86, 0.84, 0.16, 0.16])
ax_img.imshow(board_display)
ax_img.axis('off')

# - Setting the window to full screen borderless
window_manager = fig.canvas.manager.window

window_manager.overrideredirect(True)
screen_width, screen_height = window_manager.winfo_screenwidth(), window_manager.winfo_screenheight()
window_manager.geometry(f"{screen_width}x{screen_height}+0+0")

window_manager.configure(background='#4A4A4A')

animated = anim.FuncAnimation(fig, core, interval=100, cache_frame_data=False) 
plt.show()

def on_key(event=None): # - Adding an 'EXIT' Button
    plt.close('all')
    sys.exit()

window_manager.bind("<q>", on_key)