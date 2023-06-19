import traci
from collections import defaultdict

class dqnEnv():
    def __init__(self, sumoBinary, net_file: str, cfg_file: str, edgelists: list,alldets: list, dict_connection, veh:str, destination:str, state_size: int, action_size: int, use_gui: bool = True,
            begin_time: int =0, num_seconds:int = 3600, max_depart_delay:int = 10000):
        
        self.sumoBinary = sumoBinary
        self.net = net_file
        
        self.sumocfg = cfg_file
       
        self.edgelists = edgelists
        self.alldets = alldets

        self.use_gui = use_gui

        self.veh = veh
        
        self.destination = destination

        self.episode = 0 # # of run time 
        self.begin_time = begin_time
        self.num_seconds = num_seconds
        self.max_depart_delay = max_depart_delay

        self.action_size = action_size
        self.state_size = state_size
        
        self.dict_connection = dict_connection

        self.sumo =traci
        
    def start_simulation(self):
        sumo_cmd = [self.sumoBinary,
            '-c', self.sumocfg,
            '--max-depart-delay', str(self.max_depart_delay)]
        
        self.sumo.start(sumo_cmd)

        ## 모든 edge 별 length & speed limit 정보 얻어오기
        self.dict_edgelengths, self.list_edgelengths = self.get_edgelengths()
    
        self.dict_edgelimits = self.get_edgelimits()
        destlane = self.destination+'_0'
        self.destCord = self.sumo.lane.getShape(destlane)[0]
        #print('self.destCord: ',self.destCord)
        '''
        if self.begin_time > 0:
            sumo_cmd.append('-b {}'.format(self.begin_time))
        if self.use_gui:
            sumo_cmd.extend(['--start', '--quit-on-end'])
            traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")
        '''
    def sumo_step(self):
        self.sumo.simulationStep()

    def sumoclose(self):
        self.sumo.close()
        
    def reset(self):

        self.episode+=1 
        self.start_simulation()

        curlane = self.get_curlane(self.veh)
        while curlane=='':
            curlane = self.get_curlane(self.veh)
            self.sumo.simulationStep()


    def get_curlane(self,veh):
        curlane = self.sumo.vehicle.getLaneID(veh)
        return curlane

    def get_curedge(self,curlane): ##0217목 8pm 수정 오류 확인해봐야함  curlane ''뜨는거!!!!!!
        curedge = self.sumo.lane.getEdgeID(curlane)
        return curedge

    def get_done(self,curedge):
        done = False
        if curedge ==self.destination:
            done = True
        return done
    
    def get_RoadID(self, veh):
        return traci.vehicle.getRoadID(veh)

    def get_reward(self, curedge, nextedge):
        traveltime = self.sumo.edge.getTraveltime(curedge)
        reward = -traveltime
        return reward
    
    def get_nextedge(self, curedge, action):
        nextedge = self.dict_connection[curedge][action]
        return nextedge
    
    def get_edgelengths(self):
        dict_edgelengths = defaultdict(float)
        list_edgelengths = []
        dict_edgelengths.update((k,0.0 ) for k in self.edgelists)
        for edge in self.edgelists:
            lane = edge + '_0'
            length = self.sumo.lane.getLength(lane)
            dict_edgelengths[edge]=length
            list_edgelengths.append(length)
        return dict_edgelengths, list_edgelengths

    def get_edgelimits(self):
        dict_edgelimits = defaultdict(float)
        dict_edgelimits.update((k,15.0) for k in self.edgelists)
        dict_edgelimits['E7'] = 10.0
        dict_edgelimits['-E7'] = 10.0
        return dict_edgelimits

    def step(self, curedge, nextedge):
        
        beforeedge = curedge #비교해서 변하면 고를려고!

        done = self.get_done(curedge)
        reward = self.get_reward(curedge, nextedge)

        if done:
            return reward, done
        
        # self.sumo.vehicle.changeTarget(self.veh, nextedge)
        
        while self.sumo.simulation.getMinExpectedNumber() > 0:
            curedge = self.get_RoadID(self.veh)
            done = self.get_done(curedge)
            if done:
                break  
            self.sumo.simulationStep() 
            if curedge in self.edgelists and curedge !=beforeedge : #변했네!! 그럼 이제 다음 꺼 고르러 가야지
                break

        return reward, done    

    
    
    