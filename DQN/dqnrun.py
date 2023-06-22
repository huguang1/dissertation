from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import time
import optparse
import random
from xml.etree.ElementTree import parse
from collections import defaultdict
from sumolib import checkBinary
from dqnenv import dqnEnv
from dqn_store import DQNLearn
import math

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    print(tools)
    sys.path.append(tools)
else:
    sys.exit('Declare environment variable "SUMO_HOME"')


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("-N", "--num_episode",
                         default=1000, help="numer of episode to run qlenv")
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run commandline version of sumo")
    optParser.add_option("--noplot", action="store_true",
                         default=False, help="save result in png")
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


def get_alledges(net):
    # get plain edges by parsing net.xml
    tree = parse(net)
    root = tree.getroot()
    alledgelists = root.findall("edge")
    edgelists = [edge.get("id") for edge in alledgelists if ':' not in edge.get("id")]
    return edgelists


def get_edgesinfo(net):
    tree = parse(net)
    root = tree.getroot()
    alledgelists = root.findall("edge")
    edgesinfo = [x.find("lane").attrib for x in alledgelists]
    return edgesinfo


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


def get_alldets(alledges):
    alldets = [edge.replace("E", "D") for edge in alledges]
    return alldets


def dqn_run(sumoBinary, num_episode, net, sumocfg, edgelists, dict_connection, destination, state_size,
            action_size):
    env = dqnEnv(sumoBinary, net_file=net, cfg_file=sumocfg, edgelists=edgelists,
                 dict_connection=dict_connection, destination=destination, state_size=state_size,
                 action_size=action_size)
    start = time.time()
    agent_dict = {}  # 每个汽车都有一个agent
    for i in range(1000):
        agent_dict["veh"+str(i)] = DQNLearn()
    for episode in range(num_episode):
        print("\n********#{} episode start***********".format(episode))
        a = time.time()
        env.reset(agent_dict)
        score, action = env.step()
        experiment_time = env.get_time()
        env.sumoclose()
        for i, v in score.items():
            passtime = v["E4"] - v["E0"]
            score[i] = passtime
        for i, v in score.items():
            agent_dict[i].store(action[i], v)
        reward = sorted(list(score.values()))
        print(sum(reward)/len(reward))
        print(reward)
        print(experiment_time)
        print("\n****episode: {} | score: {}".format(episode, score))
        print('执行时间', time.time() - a)

    end = time.time()
    print('Source Code Time: ', end - start)


if __name__ == "__main__":
    route_name = "changelight"
    net = f"Net/{route_name}.net.xml"
    sumocfg = f"{route_name}.sumocfg"
    destination = 'E4'
    successend = ["E4"]
    state_size = 64
    action_size = 3

    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo')
        # sumoBinary = checkBinary('sumo-gui')

    if options.num_episode:
        num_episode = int(options.num_episode)
    else:
        num_episode = 1000

    edgelists = get_alledges(net)  # 총 20개 출력
    dict_connection = calculate_connections(edgelists, net)

    dqn_run(sumoBinary, num_episode, net, sumocfg, edgelists, dict_connection, destination, state_size,
            action_size)
