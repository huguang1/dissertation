import os
import sys
import subprocess
import traci
import sumolib


def run():
    # start sumo as a subprocess
    sumoBinary = sumolib.checkBinary('sumo')
    sumoProcess = subprocess.Popen([sumoBinary, "-c", "simple.sumocfg"], stdout=sys.stdout, stderr=sys.stderr)

    # connect to sumo using traci
    traci.init(host="localhost", port=8813)
    step = 0
    while step < 3600:
        traci.simulationStep()
        step += 1

    # close the connection to sumo
    traci.close()


if __name__ == '__main__':
    run()
