#!/usr/bin/env python3.6
import random as rand
import math as math


class Environment:
    def __init__(self, agent_lst=None, res_lst=None, envsize=8):
        """a"""
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
        """a"""
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.allocatedResLst = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def bid(self, res):
        min_dist = abs(self.posx - res.posx) + abs(self.posy - res.posy)

        for ares in self.allocatedResLst:
            dist = abs(ares.posx - ares.posx) + abs(ares.posy - res.posy)

            if dist < min_dist:
                min_dist = dist

        return min_dist

    def allocate(self, res):
        self.allocatedResLst.append(res)
        res.allocate()


class Ressource:
    def __init__(self, name, pos):
        """a"""
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
        """a"""
        self.env = environment
        self.nballocated = 0

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


if __name__ == "__main__":
    # Sample custom env
    lst_agent = [Agent("r1", (2, 5)), Agent("r2", (4, 4))]

    lst_res = [Ressource("o1", (5, 5)), Ressource("o2", (2, 2)), Ressource("o3", (4, 7)), Ressource("o4", (4, 2))]

    env = Environment(lst_agent, lst_res, 8)

    ssi = SSI(env)
    ssi.allocate()

    for agent in ssi.env.agent_lst:
        print(agent.name + " -> " + str(agent.allocatedResLst))

    # Sample rand env
    envrand = Environment()
    envrand.init_randomenv(2, 4)
