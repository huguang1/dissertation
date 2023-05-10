# coding=utf-8
import time
import traci

sumoCmd = ["sumo-gui", "-c", "con.sumocfg"]
traci.start(sumoCmd)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    time.sleep(0.01)

traci.close()
