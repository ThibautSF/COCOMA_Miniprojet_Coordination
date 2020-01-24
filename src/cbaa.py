#!/usr/bin/env python3.6
import random
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
            agentpos = (random.randint(0, self.envsize - 1), random.randint(0, self.envsize - 1))
            while agentpos in pos_lst:
                agentpos = (random.randint(0, self.envsize - 1), random.randint(0, self.envsize - 1))

            a = Agent("r" + str(i + 1), agentpos)
            self.agent_lst.append(a)

        self.nbres = nbres
        for i in range(nbres):
            '''init res @ rand pos'''
            respos = (random.randint(0, self.envsize - 1), random.randint(0, self.envsize - 1))
            while respos in pos_lst:
                respos = (random.randint(0, self.envsize - 1), random.randint(0, self.envsize - 1))

            res = Ressource("o" + str(i + 1), respos)
            self.res_lst.append(res)

    def in_com_range(self, a1, a2):
        dist = abs(a1.posx - a2.posx) + abs(a1.posy - a2.posy)

        return dist <= self.comrange

    def init_test_env(self):
        self.envsize = 4
        self.comrange = 2
        self.agent_lst = [
            Agent("a1", (0, 1)),
            Agent("a2", (2, 1)),
            Agent("a3", (3, 0)),
            Agent("a4", (3, 2))
        ]
        self.nbagent = len(self.agent_lst)
        self.res_lst = [
            Ressource("t1", (0, 3)),
            Ressource("t2", (1, 3)),
            Ressource("t3", (2, 3)),
            Ressource("t4", (3, 3)),
        ]
        self.nbres = len(self.res_lst)

        self.agent_lst[0].utilities = [5, 1, 2, 3]
        self.agent_lst[1].utilities = [1, 3, 6, 1]
        self.agent_lst[2].utilities = [1, 2, 5, 3]
        self.agent_lst[3].utilities = [8, 1, 1, 1]


class Agent:
    def __init__(self, name, pos):
        self.name = name
        self.posx = pos[0]
        self.posy = pos[1]
        self.utilities = []
        self.allocate_bids = []

        self.allocatedResSet = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def allocate(self, res):
        self.allocatedResSet.add(res)
        res.allocate(self)

    def unallocate(self, res):
        self.allocatedResSet.remove(res)
        res.unallocate(self)


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
        self.allocated_agent.add(agent)

    def unallocate(self, agent):
        self.allocated_agent.remove(agent)


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

            for res in self.env.res_lst:
                u = abs(agent.posx - res.posx) + abs(agent.posy - res.posy)

                agent.utilities.append(mod - u)

        pass

    def agent_bid(self, agent):
        lst = copy.deepcopy(agent.utilities)

        for i, bid in enumerate(agent.allocate_bids):
            if bid[1] is not None:
                lst[i] = 0

        utilities = copy.deepcopy(lst)

        while True:
            best_u = max(lst)
            index_best = utilities.index(best_u)
            lst.remove(best_u)
            utilities[index_best] = min(agent.utilities)

            second_u = 0
            if len(lst) > 0:
                second_u = max(lst)

            if second_u == 0:
                second_u = 1

            if best_u - second_u > agent.allocate_bids[index_best][0]:
                break

        bid = best_u - second_u
        agent.allocate_bids[index_best] = (bid, agent)
        agent.current_bid = index_best
        agent.allocate(self.env.res_lst[index_best])

        print(str(agent) + " bid " + str(bid) + " on " + str(self.env.res_lst[index_best]))

    def agent_bid2(self, agent):

        pass

    def consensus(self):
        consensus_dict = dict()
        nb_agent_in_com = 0
        nb_agent_agreed = 0

        # Init the tables at this iteration for each agent
        for agent in self.env.agent_lst:
            consensus_dict[agent] = copy.deepcopy(agent.allocate_bids)

        for i_agent, agent in enumerate(self.env.agent_lst):
            for i_com_agent, com_agent in enumerate(self.env.agent_lst):
                if (agent != com_agent or i_agent != i_com_agent) and self.env.in_com_range(agent, com_agent):
                    # print(str(agent) + " -> " + str(com_agent))
                    nb_agent_in_com += 1

                    if all([a1[0] == a2[0] for a1, a2 in zip(consensus_dict[agent], consensus_dict[com_agent])]):
                        nb_agent_agreed += 1

                    for i, bid in enumerate(consensus_dict[com_agent]):
                        # Keep the highest bid
                        if bid[0] >= consensus_dict[agent][i][0]:
                            # consensus_dict[agent][i] = bid
                            if bid[0] > agent.allocate_bids[i][0]:
                                if agent.allocate_bids[i][1] == agent:
                                    print(str(agent) + " loose bid on " + str(self.env.res_lst[agent.current_bid]))

                                    agent.current_bid = None
                                    agent.unallocate(self.env.res_lst[i])
                                agent.allocate_bids[i] = bid
                            else:
                                if bid[1] is not None and agent.allocate_bids[i][1] is not None \
                                        and bid[0] >= agent.allocate_bids[i][0]:
                                    if bid[1].name > agent.allocate_bids[i][1].name:
                                        if agent.allocate_bids[i][1] == agent:
                                            print(str(agent) + " loose bid on " +
                                                  str(self.env.res_lst[agent.current_bid]))

                                            agent.current_bid = None
                                            agent.unallocate(self.env.res_lst[i])

                                        agent.allocate_bids[i] = bid
                    '''
                    print(str(agent) + "<-" + str(com_agent) + str(agent.allocate_bids) + " = " +
                          str(consensus_dict[agent]) + " <- " + str(consensus_dict[com_agent]))
                    '''

        return nb_agent_agreed == nb_agent_in_com

    def auctioning(self):
        for agent in self.env.agent_lst:
            if len(agent.allocatedResSet) == 0:
                # CBAA bid only if not assigned (nbagent = nbres)
                self.agent_bid(agent)

        pass

    def allocate(self):
        for agent in self.env.agent_lst:
            agent.allocate_bids = [(0, None) for _ in self.env.res_lst]

        i = 1

        while True:
            nb = 0
            for res in self.env.res_lst:
                if len(res.allocated_agent) == 1:
                    nb += 1

            self.nballocated = nb

            print("\nTurn " + str(i) + ", " + str(self.nballocated) + " allocated")
            for a in self.env.agent_lst:
                print(str(a) + " -> " + str(a.allocate_bids) + " -> " + str(a.allocatedResSet))

            '''
            if self.nballocated == self.env.nbres:
                print("END : All ressources allocated")
                break
            '''

            print("Auctioning #" + str(i))
            self.auctioning()

            print("Consensus #" + str(i))
            all_consent = self.consensus()

            if all_consent:
                print("END : All agent consent")
                break

            i += 1


if __name__ == "__main__":
    # Sample custom env
    """
    list_agent = [Agent("r1", (2, 5)), Agent("r2", (4, 4))]
    list_res = [Ressource("o1", (5, 5)), Ressource("o2", (2, 2)), Ressource("o3", (4, 7)), Ressource("o4", (4, 2))]
    env = Environment(list_agent, list_res, 8)

    cbaa = CBAA(env)
    cbaa.allocate()

    for one_agent in cbaa.env.agent_lst:
        print(one_agent.name + " -> " + str(one_agent.allocatedResLst))
    """

    # Sample rand env
    envrand = Environment()
    envrand.init_randomenv(4, 4)

    cbaa = CBAA(envrand)
    cbaa.compute_utilities()
    # cbaa.env.init_test_env()

    print("Map:")
    for x in range(cbaa.env.envsize):
        line = ""
        for y in range(cbaa.env.envsize):
            s = "_"
            for one_agent in cbaa.env.agent_lst:
                if one_agent.posx == x and one_agent.posy == y:
                    s = one_agent.name

            for one_res in cbaa.env.res_lst:
                if one_res.posx == x and one_res.posy == y:
                    s = one_res.name

            line += s + "\t"
        print(line)

    print("\nUtilities:")
    for one_agent in cbaa.env.agent_lst:
        print(str(one_agent) + " -> " + str(one_agent.utilities))

    print("\nSTART CBAA")
    cbaa.allocate()

    print("\nFinal assignment :")
    for one_agent in cbaa.env.agent_lst:
        print(str(one_agent) + " -> " + str(one_agent.allocatedResSet))
