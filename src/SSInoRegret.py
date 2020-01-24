#!/usr/bin/env python3.6
import random as rand
import math as math

class Environment:
    def __init__(self, agent_lst=None, res_lst=None, envsize=8):
        if agent_lst is None:
            agent_lst = []
        if res_lst is None:
            res_lst = []

        self.envsize = envsize
        self.agent_lst = agent_lst
        self.nbagent = len(agent_lst)
        self.res_lst = res_lst
        self.nbres = len(res_lst)

    def init_randomenv(self, nbagent=2, nbres=4):
        pos_lst = []

        self.nbagent = nbagent
        for i in range(nbagent):
            '''init agent @ rand pos'''
            agentpos = (rand.randint(0, self.envsize - 1), rand.randint(0, self.envsize - 1))
            while agentpos in pos_lst:
                agentpos = (rand.randint(0, self.envsize - 1), rand.randint(0, self.envsize - 1))

            a = Agent("r" + str(i + 1), agentpos)
            pos_lst.append(agentpos)
            self.agent_lst.append(a)

        self.nbres = nbres
        for i in range(nbres):
            '''init res @ rand pos'''
            respos = (rand.randint(0, self.envsize - 1), rand.randint(0, self.envsize - 1))
            while respos in pos_lst:
                respos = (rand.randint(0, self.envsize - 1), rand.randint(0, self.envsize - 1))

            res = Ressource("o" + str(i + 1), respos)
            pos_lst.append(agentpos)
            self.res_lst.append(res)

class Agent:
    def __init__(self, name, pos):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.allocatedResLst = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def bid(self, listRessource):
        min_dist = math.inf
        indexBestRessource = None

        for index, ressource in enumerate(listRessource): # Ressource la plus proche du robot..
          if ressource.allocated == False: # .. qui ne soit pas allouée
            dist = abs(self.posx - ressource.posx) + abs(self.posy - ressource.posy)
            if dist < min_dist:
              min_dist = dist
              indexBestRessource = index

        for index, ressource in enumerate(listRessource): # Ressource la plus proche d'une ressource possédée par le robot
          for ownedRessource in self.allocatedResLst:
            if ressource.allocated == False:
              dist = abs(ownedRessource.posx - ressource.posx) + abs(ownedRessource.posy - ressource.posy)
              if dist < min_dist:
                min_dist = dist
                indexBestRessource = index

        return (indexBestRessource, min_dist)

    def allocate(self, res):
        self.allocatedResLst.append(res)
        res.allocate()

class Ressource:
    def __init__(self, name, pos):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.allocated = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def allocate(self):
        self.allocated = True

class SSI:
    def __init__(self, environment):
        self.env = environment
        self.nballocated = 0

    def allocate(self):
        while self.nballocated < self.env.nbres:
            print("############# New allocation round #############")
            min_bid = math.inf
            indexRessource = None
            for index, agent in enumerate(self.env.agent_lst):
                (indexBestRessource, bid) = agent.bid(self.env.res_lst)
                print("Agent n°", index + 1, "bids", bid, "on ressource n°", indexBestRessource + 1)
                if bid < min_bid:
                    min_bid = bid
                    bidder = index
                    indexRessource = indexBestRessource
            print("-----> Agent n°", bidder + 1, "gets ressource n°", indexRessource + 1)
            self.env.agent_lst[bidder].allocate(self.env.res_lst[indexRessource])
            self.nballocated += 1

    def printMap(self):
        print("Map: ")
        for y in range(self.env.envsize):
            line = ""
            for x in range(self.env.envsize):
                s = "_"
                for one_agent in self.env.agent_lst:
                    if one_agent.posx == x and one_agent.posy == y:
                        s = one_agent.name

                for one_res in self.env.res_lst:
                    if one_res.posx == x and one_res.posy == y:
                        s = one_res.name

                line += s + "\t"
            print(line)
if __name__ == "__main__":
    # Sample custom env
    list_agent = [Agent("r0", (2, 5)), Agent("r1", (4, 4))]
    list_res = [Ressource("o1", (5, 5)), Ressource("o2", (2, 2)), Ressource("o3", (4, 7)), Ressource("o4", (4, 2))]
    env = Environment(list_agent, list_res, 8)

    ssi = SSI(env)
    ssi.allocate()

    for agent in ssi.env.agent_lst:
        print(agent.name + " -> " + str(agent.allocatedResLst))
    ssi.printMap()
    # # Sample rand env
    # envrand = Environment()
    # envrand.init_randomenv(2, 4)
