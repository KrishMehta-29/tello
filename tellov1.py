import threading
import socket
import sys
import time
import datetime
import tkinter

FlightStartTime = datetime.datetime.now()
FormattedStartTime = FlightStartTime.strftime("%d-%m_%H-%M-%S")
FileName = "TelloFlight-" + FormattedStartTime + ".txt"
logs = open(FileName, 'w+')
logs.write("Flight Date: " + FlightStartTime.strftime("%d/%m/%Y") + '\n')
logs.write("Flight Time: " + FlightStartTime.strftime("%H:%M:%S")+ '\n\n')

host = ''
port = 9000
locaddr = (host, port)
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)

def getTimeStamp():
    time = datetime.datetime.now()
    Ftime = str(time)
    return ("[" + Ftime[11:-4] + "] ")

def recv(log = True):

    try:
        data, server = sock.recvfrom(1518)
        if (log == True):
            logs.write(getTimeStamp() + "Received: " + data.decode(encoding = "utf-8") + "\n")

        return data.decode(encoding="utf-8")

    except Exception as a:

        print(a)
        print('\nExit . . .\n')

def send(msg, log = True):
    try:
        if(log == True):
            print("Sending Command:", msg)
            logs.write(getTimeStamp() + "Sent Command: " + msg + '\n')

        sent = sock.sendto(msg.encode('utf-8'), tello_address)
        return recv(log)

    except:
        print("\nCommand Break")
        sys.exit()

def initialize():
    response = send('command', False)
    if response == 'ok':
        print("Connected to Tello")
        BatteryPercentage = send('battery?', False)
        print("Battery Percentage:", BatteryPercentage)
        logs.write("Connected to Tello\n")
        logs.write("Battery Percentage:" + BatteryPercentage + '\n' )

def sendCommand():
    cmd = input("Enter the Command")
    if (cmd == 'land' or cmd == 'quit'):
        send('land')
        logs.write(getTimeStamp() + "Flight Ended")
        logs.close()
        sys.exit()

    print(send(cmd))

initialize()

while True:
    sendCommand()
