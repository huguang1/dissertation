from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import matplotlib.pyplot as plt
from xml.etree.ElementTree import parse
from collections import defaultdict

from matplotlib.ticker import MaxNLocator

from sumolib import checkBinary
import traci

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    print(tools)
    sys.path.append(tools)
else:
    sys.exit('Declare environment variable "SUMO_HOME"')


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("-N", "--episodenum",
                         default=30, help="numer of episode to run qlenv")
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run commandline version of sumo")
    options, args = optParser.parse_args()
    return options


def get_toedges(net, fromedge):
    # calculate reachable nextedges
    tree = parse(net)
    root = tree.getroot()
    toedges = []
    for connection in root.iter("connection"):
        if connection.get("from") == fromedge:
            toedges.append(connection.get("to"))
    return toedges


def get_alledges(net):  # 这个函数是获取所有有用的道路的信息
    # get plain edges by parsing net.xml
    tree = parse(net)
    root = tree.getroot()
    alledgelists = root.findall("edge")
    edgelists = [edge.get("id") for edge in alledgelists if ':' not in edge.get("id")]
    return edgelists


def generate_detectionfile(net, det):
    # generate det.xml file by setting a detector at the end of each lane (-10m)
    with open(det, "w") as detections:
        alledges = get_alledges(net)
        alllanes = [edge + '_0' for edge in alledges]
        alldets = [edge.replace("E", "D") for edge in alledges]

        pos = -10
        print('<additional>', file=detections)
        for i in range(len(alledges)):
            print(' <e1Detector id="%s" lane="%s" pos="%i" freq="30" file="cross.out" friendlyPos="x"/>'
                  % (alldets[i], alllanes[i], pos), file=detections)
        print('</additional>', file=detections)
        return alldets


def calculate_connections(edgelists, net):
    # calculate dictionary of reachable edges(next edge) for every edge
    tree = parse(net)
    root = tree.getroot()

    dict_connection = defaultdict(list)
    dict_connection.update((k, []) for k in edgelists)

    for connection in root.iter("connection"):
        curedge = connection.get("from")
        if ':' not in curedge:
            dict_connection[curedge].append(connection.get("to"))

    for k, v in dict_connection.items():
        if len(v) == 0:
            dict_connection[k] = ['', '', '']
        elif len(v) == 1:
            dict_connection[k].append('')
            dict_connection[k].append('')
        elif len(v) == 2:
            dict_connection[k].append('')
    return dict_connection


##########@경로 탐색@##########
# 1. random routing : routing randomly by calculating next route(edge) when the current edge is changed.
def random_run(sumoBinary, sumocfg, edgelists):
    traci.start([sumoBinary, "-c", sumocfg, "--tripinfo-output", "tripinfo.xml"])  # start sumo server using cmd

    step = 0
    traci.route.add("rou1", ["E0", "E1"])  # default route
    traci.vehicle.add("veh1", "rou1")
    print('[ Veh0 Random Routes ]')
    traci.simulationStep()
    beforelane = traci.vehicle.getLaneID("veh1")
    # beforeedge = traci.lane.getEdgeID(beforelane)
    # print(beforeedge, end=' -> ')  # start point

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1
    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    net = "simple.net.xml"
    det = "simple.det.xml"
    sumocfg = "simple.sumocfg"
    # veh = "veh0"
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    alldets = generate_detectionfile(net, det)  # generate detector file
    edgelists = get_alledges(net)
    dict_connection = calculate_connections(edgelists, net)

    """Run Simulation"""
    # 1) Run randomly
    random_run(sumoBinary, sumocfg, edgelists)



