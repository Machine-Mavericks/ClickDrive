import time
from networktables import NetworkTables
import json

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

""" 
  I am thinking that we can build functionality into ClickDrive so you can 
  save paths to disk. 
  Then add a selector of saved paths to publish to the network tables.
  Then in the robot initialize, read those paths and create a sendablechooser 
  with the list of paths. 
  Then all you have to do is select a path,  throw the robot in auto and it does the path! 
"""


# These would be a list of coordinates that are saved to disk
waypointList1 = [[.1,.1], [.2,.2], [.3,.3]]
waypointList2 = [[3,5], [1,2],[4,5],[1,1],[7,3]]

# In the ClickDrive code we would build this json
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


# Initialize the NetworkTables
NetworkTables.initialize() # we will eventually put the ip address of the robot here
sd = NetworkTables.getTable("SmartDashboard/ClickDrive") #we are writing to a subfolder of the SmartDashboard called ClickDrive


#write the paths out to the NetworkTables
i = 0
while True:
    sd.putString("trajectories",json.dumps(paths))
    time.sleep(1)
    i += 1