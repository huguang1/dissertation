import random

import traci
from collections import defaultdict


class dqnEnv():
    def __init__(self, sumoBinary, net_file: str, cfg_file: str, edgelists: list, dict_connection,
                 destination: str, state_size: int, action_size: int, use_gui: bool = True,
                 begin_time: int = 0, num_seconds: int = 3600, max_depart_delay: int = 10000):
        self.sumoBinary = sumoBinary
        self.net = net_file
        self.sumocfg = cfg_file
        self.edgelists = edgelists
        self.use_gui = use_gui
        self.destination = destination
        self.episode = 0  # # of run time
        self.begin_time = begin_time
        self.num_seconds = num_seconds
        self.max_depart_delay = max_depart_delay
        self.action_size = action_size
        self.state_size = state_size
        self.dict_connection = dict_connection
        self.sumo = traci
        self.veh_list = []

    def start_simulation(self):
        sumo_cmd = [self.sumoBinary, '-c', self.sumocfg, '--max-depart-delay', str(self.max_depart_delay)]
        self.sumo.start(sumo_cmd)
        max_speed = 20  # 车辆的最大速度（以米/秒为单位）
        min_gap = 5  # 车辆之间的最小间距（以米为单位）
        route_list = [["E0", "E1", "E2", "E3", "E4"], ["E0", "E5", "E6", "E7", "E4"]]
        for i in range(100):
            route_name = "rou" + str(i)
            name = "veh" + str(i)
            self.sumo.route.add(route_name, random.choice(route_list))
            # self.sumo.route.add(route_name, route_list[0])
            self.sumo.vehicle.add(name, route_name)
            self.sumo.vehicle.setMaxSpeed(name, max_speed)
            self.sumo.vehicle.setMinGap(name, min_gap)
        self.dict_edgelengths, self.list_edgelengths = self.get_edgelengths()
        destlane = self.destination + '_0'
        self.destCord = self.sumo.lane.getShape(destlane)[0]

    def sumoclose(self):
        self.sumo.close()

    def reset(self):

        self.episode += 1
        self.start_simulation()
        curlane = self.get_curlane("veh0")
        while curlane == '':
            curlane = self.get_curlane("veh0")
            self.sumo.simulationStep()

    def get_curlane(self, veh):
        curlane = self.sumo.vehicle.getLaneID(veh)
        return curlane

    def get_curedge(self, curlane):
        curedge = self.sumo.lane.getEdgeID(curlane)
        return curedge

    def get_RoadID(self, veh):
        return traci.vehicle.getRoadID(veh)

    def get_reward(self, curedge_dict, reward_record):
        for i in curedge_dict.keys():
            if ":" in curedge_dict[i]:
                continue
            if curedge_dict[i] not in ["E0", "E4"]:
                continue
            if i in reward_record.keys() and curedge_dict[i] in reward_record[i].keys():
                continue
            traveltime = self.sumo.simulation.getTime()
            if i in reward_record.keys():
                reward_record[i][curedge_dict[i]] = traveltime
            else:
                reward_record[i] = {
                    curedge_dict[i]: traveltime
                }
        return reward_record

    def get_nextedge(self, curedge, action):
        nextedge = self.dict_connection[curedge][action]
        return nextedge

    def get_edgelengths(self):
        dict_edgelengths = defaultdict(float)
        list_edgelengths = []
        dict_edgelengths.update((k, 0.0) for k in self.edgelists)
        for edge in self.edgelists:
            lane = edge + '_0'
            length = self.sumo.lane.getLength(lane)
            dict_edgelengths[edge] = length
            list_edgelengths.append(length)
        return dict_edgelengths, list_edgelengths

    def get_all_curedge(self, curedge_dict):
        vehicle_ids = self.sumo.vehicle.getIDList()
        for i in vehicle_ids:
            curedge = self.get_RoadID(i)
            if curedge in ["E0", "E4"]:
                curedge_dict[i] = curedge
        return curedge_dict

    def step(self):
        reward_record = {}
        curedge_dict = {}
        while self.sumo.simulation.getMinExpectedNumber() > 0:
            curedge_dict = self.get_all_curedge(curedge_dict)
            beforeedge_dict = curedge_dict
            reward_record = self.get_reward(curedge_dict, reward_record)
            self.sumo.simulationStep()
            while self.sumo.simulation.getMinExpectedNumber() > 0:
                curedge_dict = self.get_all_curedge(curedge_dict)
                if beforeedge_dict == curedge_dict:
                    self.sumo.simulationStep()
                else:
                    break
        return reward_record

    def get_time(self):
        return self.sumo.simulation.getTime()

