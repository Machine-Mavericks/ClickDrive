import time
from networktables import NetworkTables
import json

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

#here is a named list of waypoints

waypointList1 = [[.1,.1], [.2,.2], [.3,.3]]
waypointList2 = [[3,5], [1,2],[4,5],[1,1],[7,3]]
paths = {
        "allPaths":[{
            "pathname":"LoopDeLoop",
            "waypoints": json.dumps(waypointList1)
        }
         ,
         {
         "pathname":"ZigZag",
         "waypoints": json.dumps(waypointList2)
         }]
        }

# we will eventually put the ip address of the robot here
NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard/ClickDrive") #we are writing to a subfolder of the SmartDashboard called ClickDrive

i = 0
while True:
    sd.putString("trajectories",json.dumps(paths))
    time.sleep(1)
    i += 1