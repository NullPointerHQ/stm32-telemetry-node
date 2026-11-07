import serial as ser # - Used for data ingestion

 # - Establishing the connection, hardcoded values for now
PORT = "COM3"
BAUD_RATE = 115200
cnx = ser.Serial(PORT, BAUD_RATE)

# - Printing the raw feed to the console
while 1:
    # - Grabbing the signal from the board, decoding it into human-readable language and removing carriage return and line feed characters
    telemetry = cnx.readline().decode('utf-8').strip()
    print(telemetry)