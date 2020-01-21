#!/usr/bin/env python3.6
import random as rand
import math
import copy


class Environment:
    def __init__(self, agent_lst=None, res_lst=None, envsize=8, comrange=8):
        if agent_lst is None:
            agent_lst = []
        if res_lst is None:
            res_lst = []

        self.envsize = envsize
        self.comrange = comrange
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

    def in_com_range(self, a1, a2):
        dist = abs(a1.posx - a2.posx) + abs(a1.posy - a2.posy)

        return dist <= self.comrange


class Agent:
    def __init__(self, name, pos):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        # self.utilities = []
        # self.allocate_bids = []

        self.allocatedResSet = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def allocate(self, res):
        self.allocatedResSet.add(res)
        res.allocate(self)


class Ressource:
    def __init__(self, name, pos):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.allocated_agent = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def allocate(self, agent):
        #if self.allocated_agent is not None:
        #    # remove ressource from previous agent owner
        #   self.allocated_agent.allocatedResSet.remove(self)

        self.allocated_agent.add(agent)


class CBAA:
    def __init__(self, environment):
        """a"""
        self.env = environment
        self.nballocated = 0

        self.compute_utilities()

    def compute_utilities(self):
        mod = self.env.envsize * 2

        for agent in self.env.agent_lst:
            agent.utilities = []
            agent.allocate_bids = []

            for res in self.env.res_lst:
                u = abs(agent.posx - res.posx) + abs(agent.posy - res.posy)

                agent.utilities.append(mod - u)
                agent.allocate_bids.append(0)

        pass

    def agent_bid(self, agent):
        best_u = -math.inf
        index_best = 0
        second_u = 0

        for i, res in enumerate(self.env.res_lst):
            u = agent.utilities[i]

            if u > best_u and u > agent.allocate_bids[i]:
                second_u = best_u
                best_u = u
                index_best = i

        bid = best_u - second_u
        agent.allocate_bids[index_best] = bid
        agent.current_bid = index_best

    def consensus(self):
        consensus_dict = dict()

        # Init the tables at this iteration for each agent
        for agent in self.env.agent_lst:
            consensus_dict[agent] = copy.deepcopy(agent.allocate_bids)

        for agent in self.env.agent_lst:
            for com_agent in self.env.agent_lst:
                if self.env.in_com_range(agent, com_agent):
                    for i, bid in enumerate(agent.allocate_bids):
                        # TODO
                        pass

        pass

    def allocate(self):
        for agent in self.env.agent_lst:
            if len(agent.allocatedResSet()) == 0:
                # CBAA bid only if not assigned (nbagent = nbres)
                self.agent_bid(agent)

        pass
