import traci
from collections import defaultdict


class Vehicle:
    def __init__(self, name, route_name, route):
        self.name = name
        self.route_name = route_name
        self.route = route


class dqnEnv():
    def __init__(self, sumoBinary, net_file: str, cfg_file: str, edgelists: list, alldets: list, dict_connection,
                 destination: str, state_size: int, action_size: int, use_gui: bool = True,
                 begin_time: int = 0, num_seconds: int = 3600, max_depart_delay: int = 10000):
        self.sumoBinary = sumoBinary
        self.net = net_file
        self.sumocfg = cfg_file
        self.edgelists = edgelists
        self.alldets = alldets
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
        name = "veh0"
        route_name = "rou0"
        route = ["E2", "E3", "E4"]
        veh0 = Vehicle(name, route_name, route)
        name = "veh1"
        route_name = "rou1"
        route = ["E2", "E3", "E4"]
        veh1 = Vehicle(name, route_name, route)
        self.veh_list.append(veh0)
        # self.veh_list.append(veh1)
        self.sumo.route.add(self.veh_list[0].route_name, self.veh_list[0].route)
        self.sumo.vehicle.add(self.veh_list[0].name, self.veh_list[0].route_name)
        # self.sumo.route.add(self.veh_list[1].route_name, self.veh_list[1].route)
        # self.sumo.vehicle.add(self.veh_list[1].name, self.veh_list[1].route_name)
        self.dict_edgelengths, self.list_edgelengths = self.get_edgelengths()
        destlane = self.destination + '_0'
        self.destCord = self.sumo.lane.getShape(destlane)[0]

    def sumo_step(self):
        self.sumo.simulationStep()

    def sumoclose(self):
        self.sumo.close()

    def reset(self):

        self.episode += 1
        self.start_simulation()

        curlane = self.get_curlane(self.veh_list[0].name)
        while curlane == '':
            curlane = self.get_curlane(self.veh_list[0].name)
            self.sumo.simulationStep()

    def get_curlane(self, veh):
        curlane = self.sumo.vehicle.getLaneID(veh)
        return curlane

    def get_curedge(self, curlane):
        curedge = self.sumo.lane.getEdgeID(curlane)
        return curedge

    def get_done(self, curedge):
        done = False
        if curedge == self.destination:
            done = True
        return done

    def get_RoadID(self, veh):
        return traci.vehicle.getRoadID(veh)

    def get_reward(self, curedge):
        traveltime = self.sumo.edge.getTraveltime(curedge)
        reward = -traveltime
        return reward

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

    def step(self, curedge):
        beforeedge = curedge
        done = self.get_done(curedge)
        reward = self.get_reward(curedge)
        if done:
            return reward, done
        while self.sumo.simulation.getMinExpectedNumber() > 0:
            vehicle_ids = self.sumo.vehicle.getIDList()
            curedge = self.get_RoadID(self.veh_list[0].name)
            done = self.get_done(curedge)
            if done:
                break
            self.sumo.simulationStep()
            if curedge in self.edgelists and curedge != beforeedge:
                break
        return reward, done
