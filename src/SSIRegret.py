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
          if ressource.allocated == False: # .. qui ne soit pas allouee
            dist = abs(self.posx - ressource.posx) + abs(self.posy - ressource.posy)
            if dist < min_dist:
              min_dist = dist
              indexBestRessource = index

        for index, ressource in enumerate(listRessource): # Ressource la plus proche d'une ressource possedee par le robot
          for ownedRessource in self.allocatedResLst:
            if ressource.allocated == False:
              dist = abs(ownedRessource.posx - ressource.posx) + abs(ownedRessource.posy - ressource.posy)
              if dist < min_dist:
                min_dist = dist
                indexBestRessource = index

        return (indexBestRessource, min_dist)

    def costInsertion(self, ressource):
      if len(self.allocatedResLst) == 0:
        return abs(self.posx - ressource.posx) + abs(self.posy - ressource.posy)
      elif len(self.allocatedResLst) == 1:
          return abs(self.allocatedResLst[0].posx - ressource.posx) + abs(self.allocatedResLst[0].posy - ressource.posy)
      else:
        actualCost = 0
        for idRes in range(len(self.allocatedResLst) - 1):
            actualCost += abs(self.allocatedResLst[idRes].posx - self.allocatedResLst[idRes + 1].posx) + abs(self.allocatedResLst[idRes].posy - self.allocatedResLst[idRes + 1].posy)
        newCost = math.inf
        for positionInsertion in range(len(self.allocatedResLst) + 1):
            newTmpList = []
            costTmp = 0
            offset = 0
            for i in range(len(self.allocatedResLst) + 1):
                if i == positionInsertion:
                    newTmpList.append(ressource)
                    offset = 1
                else:
                    newTmpList.append(self.allocatedResLst[i - offset])
            for idRes in range(len(newTmpList) - 1):
                costTmp += abs(newTmpList[idRes].posx - newTmpList[idRes + 1].posx) + abs(newTmpList[idRes].posy - newTmpList[idRes + 1].posy)
            if costTmp < newCost:
                newCost = costTmp
        return newCost - actualCost

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

class SSIregret:
    def __init__(self, environment):
        self.env = environment
        self.nballocated = 0


    def solve(self):
      for i in range(self.env.nbres):
        print("############# New allocation round #############")
        regretArray = []
        regretArray.append([]) # ressources names
        for ressource in self.env.res_lst: # Add ressources available
          if (ressource.allocated == False):
            regretArray[0].append(ressource)
        for indexAgent, agent in enumerate(self.env.agent_lst): # For each agent..
          regretArray.append([])
          for ressource in regretArray[0]: # ..Add insertion cost of the agent for each ressource available
            regretArray[indexAgent + 1].append(agent.costInsertion(ressource))
        regretArray.append([]) # Regrets line
        for idRes in range(len(regretArray[0])): # Compute regret for each available ressource
            minBid = math.inf
            minSecondBid = math.inf
            agentMinBid = None
            agentSecondMinBid = None
            for indexAgent in range(len(self.env.agent_lst)):
                if (regretArray[indexAgent + 1][idRes] < minBid):
                    minBid = regretArray[indexAgent + 1][idRes]
                    agentMinBid = indexAgent
            for indexAgent in range(len(self.env.agent_lst)):
                if (regretArray[indexAgent + 1][idRes] < minSecondBid):
                    if (indexAgent != agentMinBid):
                        minSecondBid = regretArray[indexAgent + 1][idRes]
                        agentSecondMinBid = indexAgent
            regretArray[len(self.env.agent_lst) + 1].append(minSecondBid - minBid)

        maxRegret = - math.inf
        for idRes in range(len(regretArray[0])):
            if (regretArray[len(self.env.agent_lst) + 1][idRes] > maxRegret):
                maxRegret = regretArray[len(self.env.agent_lst) + 1][idRes]

        nbSameRegretFound = 0
        minBidOfAll = math.inf
        for idRes in range(len(regretArray[0])):
            if (regretArray[len(self.env.agent_lst) + 1][idRes] == maxRegret):
                nbSameRegretFound += 1
                for allocatedAgent in range(len(self.env.agent_lst)):
                    if regretArray[allocatedAgent + 1][idRes] < minBidOfAll:
                        minBidOfAll = regretArray[allocatedAgent + 1][idRes]
                        indexMaxRegret = idRes

        minBid = math.inf
        agentMinBid = None
        for allocatedAgent in range(len(self.env.agent_lst)):
            if regretArray[allocatedAgent + 1][indexMaxRegret] < minBid:
                minBid = regretArray[allocatedAgent + 1][indexMaxRegret]
                agentMinBid = allocatedAgent

        self.env.agent_lst[agentMinBid].allocate(regretArray[0][indexMaxRegret])
        print("########## Current Regret Table : ##########")
        print("Objects available")
        print(regretArray[0])
        print("Bids of each agents")
        for i in range(len(self.env.agent_lst)):
            print(regretArray[i + 1])
        print("Regrets for each objects")
        print(regretArray[len(self.env.agent_lst) + 1])
        if (nbSameRegretFound > 1):
            print("Found a TIE with the highest regret, finding the best bid..")
        # print(regretArray)
        print("Object with highest regret is object", regretArray[0][indexMaxRegret])
        print("Agent n°", agentMinBid + 1, "get it")
        # print("The min bid on this object is ", regretArray[][] "from agent")
        print("")

if __name__ == "__main__":
    # Sample custom env
    list_agent = [Agent("r1", (2, 5)), Agent("r2", (4, 4))]
    list_res = [Ressource("o1", (5, 5)), Ressource("o2", (2, 2)), Ressource("o3", (4, 7)), Ressource("o4", (4, 2))]
    env = Environment(list_agent, list_res, 8)

    ssi_regret = SSIregret(env)
    ssi_regret.solve()
    for agent in ssi_regret.env.agent_lst:
        print(agent.name + " -> " + str(agent.allocatedResLst))
