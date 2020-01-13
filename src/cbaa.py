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
            self.agent_lst.append(a)

        self.nbres = nbres
        for i in range(nbres):
            '''init res @ rand pos'''
            respos = (rand.randint(0, self.envsize - 1), rand.randint(0, self.envsize - 1))
            while respos in pos_lst:
                respos = (rand.randint(0, self.envsize - 1), rand.randint(0, self.envsize - 1))

            res = Ressource("o" + str(i + 1), respos)
            self.agent_lst.append(res)


class Agent:
    def __init__(self, name, pos):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.utilities = []

        self.allocatedResLst = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def bid(self, listRessource):
        min_dist = math.inf
        indexBestRessource = None

        for index, ressource in enumerate(listRessource):
            # Ressource la plus proche du robot..
            if not ressource.allocated:
                # .. qui ne soit pas allouée
                dist = abs(self.posx - ressource.posx) + abs(self.posy - ressource.posy)
                if dist < min_dist:
                    min_dist = dist
                    indexBestRessource = index

        for index, ressource in enumerate(listRessource):
            # Ressource la plus proche d'une ressource possédée par le robot
            for ownedRessource in self.allocatedResLst:
                if not ressource.allocated:
                    dist = abs(ownedRessource.posx - ressource.posx) + abs(ownedRessource.posy - ressource.posy)
                    if dist < min_dist:
                        min_dist = dist
                        indexBestRessource = index

        return indexBestRessource, min_dist

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


class CBAA:
    def __init__(self, environment):
        """a"""
        self.env = environment
        self.nballocated = 0

        self.compute_utilities()

    def compute_utilities(self):
        for agent in self.env.agent_lst:
            for res in self.env.res_lst:
                u = abs(agent.posx - res.posx) + abs(agent.posy - res.posy)
                agent.utilities.append(u)

    def select_task(self, ci, ):
        pass

    def allocate(self):
        while self.nballocated < self.env.nbres:
            res = self.env.res_lst[self.nballocated]

            bidder = -1
            min_bid = math.inf

            for i, a in enumerate(self.env.agent_lst):
                bid = a.bid(res)

                if bid < min_bid:
                    min_bid = bid
                    bidder = i

            if bidder != -1:
                self.env.agent_lst[bidder].allocate(res)
                self.nballocated += 1
