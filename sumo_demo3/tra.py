# coding=utf-8
import time

import traci

sumoCmd = ["sumo-gui", "-c", "con.sumocfg"]
traci.start(sumoCmd)

maxcap = 2000

wait = []
charge = []
cache = {}
step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    step += 1
    for i in range(len(vehicles)):
        vehid = vehicles[i]
        rembat = float(traci.vehicle.getParameter(vehid, "device.battery.actualBatteryCapacity"))
        print(rembat)
        if (rembat < 600 and (vehid not in wait) and (vehid not in charge)):
            target = traci.vehicle.getRoute(vehid)
            target = target[len(target) - 1]
            cache[vehid] = target
            traci.vehicle.changeTarget(vehid, "E4")
            wait.append(vehid)
        if (vehid in wait):

            wait.remove(vehid)
            charge.append(vehid)
        if (vehid in charge):
            charge.remove(vehid)
            traci.vehicle.changeTarget(vehid, cache[vehid])

    time.sleep(0.001)

traci.close()
