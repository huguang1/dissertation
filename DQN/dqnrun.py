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
from dqnagent import dqnAgent
from collections import Counter
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
    edgesinfo = [edge for edge in edgesinfo if ':' not in edge.get("id")]
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


def generate_lanedetectionfile(net, det):
    # generate det.xml file by setting a detector at the end of each lane (-10m)
    alledges = get_alledges(net)
    edgesinfo = get_edgesinfo(net)
    alllanes = [edge + '_0' for edge in alledges]
    alldets = [edge.replace("E", "D") for edge in alledges]

    with open(det, "w") as f:
        print('<additional>', file=f)
        for i, v in enumerate(edgesinfo):
            print(
                '        <laneAreaDetector id="%s" lane="%s" pos="0.0" length="%s" freq ="%s" file="dqn_detfile.out"/>'
                % (alldets[i], v['id'], v['length'], "1"), file=f)
        print('</additional>', file=f)
    return alldets


def get_alldets(alledges):
    alldets = [edge.replace("E", "D") for edge in alledges]
    return alldets


def dqn_run(sumoBinary, num_episode, net, sumocfg, edgelists, alldets, dict_connection, destination, state_size,
            action_size):
    agent_dict = {}  # 每个汽车都有一个agent
    for i in range(1000):
        agent_dict["veh"+str(i)] = dqnAgent(edgelists, dict_connection, state_size, action_size, num_episode)
    env = dqnEnv(sumoBinary, net_file=net, cfg_file=sumocfg, edgelists=edgelists, alldets=alldets,
                 dict_connection=dict_connection, destination=destination, state_size=state_size,
                 action_size=action_size, agent_dict=agent_dict)
    start = time.time()
    average_list = []
    for episode in range(num_episode):
        print("\n********#{} episode start***********".format(episode))
        a = time.time()
        env.reset()
        score = env.step()
        experiment_time = env.get_time()
        print(env.action_list)
        counter = Counter(env.action_list)
        most_common = counter.most_common(1)
        print(most_common[0][0], most_common[0][1])
        env.action_list = []
        env.sumoclose()
        for i, v in score.items():
            passtime = v["E4"] - v["E0"]
            score[i] = passtime
        for i, agent in agent_dict.items():
            # 将reward放到记录中去
            agent.append_sample(agent.state, agent.action, score[i], agent.state, True)
            # 训练
            if len(agent.memory) >= agent.train_start:
                agent.train_model()
            # 更新模型
            agent.update_target_model()
        reward = sorted([-1*i for i in list(score.values())])
        average = sum(reward)/len(reward)
        average_list.append(average)
        print(average_list)
        print(f'average time for all car: {average}')
        print('all the time of all car: ', reward)
        print('The time required for an experiment: ', experiment_time)
        print("\n****episode: {} | score: {}".format(episode, score))
        print('执行时间', time.time() - a)

    end = time.time()
    print('Source Code Time: ', end - start)
    print(average_list)


"""
100%  [1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081, 1069.081]
90% [886.38, 867.057, 877.81, 880.957, 852.013, 858.631, 899.506, 869.731, 834.675, 852.192]
80% [701.639, 700.916, 705.938, 718.093, 722.722, 742.117, 726.131, 768.65, 722.579, 746.041]
70% [690.927, 685.186, 671.987, 688.682, 679.754, 682.527, 689.587, 689.264, 677.464, 690.783]
60% [708.489, 699.986, 695.856, 696.305, 700.358, 698.452, 688.072, 702.539, 706.499, 699.437]
50% [726.531, 720.826, 722.748, 723.074, 728.552, 712.958, 720.039, 728.765, 726.42, 724.658]
"""


if __name__ == "__main__":
    route_name = "changelight"
    net = f"Net/{route_name}.net.xml"
    det = f"Add/{route_name}.det.xml"
    sumocfg = f"{route_name}.sumocfg"
    destination = 'E4'
    successend = ["E4"]
    state_size = 46
    action_size = 2

    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        # sumoBinary = checkBinary('sumo')
        sumoBinary = checkBinary('sumo-gui')
    #
    if options.num_episode:
        num_episode = int(options.num_episode)
    else:
        num_episode = 1000

    edgelists = get_alledges(net)
    dict_connection = calculate_connections(edgelists, net)
    dets = generate_lanedetectionfile(net, det)  #
    alldets = get_alldets(edgelists)

    dqn_run(sumoBinary, num_episode, net, sumocfg, edgelists, alldets, dict_connection, destination, state_size,
            action_size)
