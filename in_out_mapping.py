import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def read_ints(s):
    return [int(i) for i in s.split(' ')]


def read_input(input_filepath):
    with open(input_filepath, 'r') as f:
        input_file = f.read().split('\n')
    nl, mt, ns, nt = read_ints(input_file[0])
    orgs, dests, wght, time, pps = [], [], [], [], []
    for i in range(ns):
        l = read_ints(input_file[1 + i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc, endTripLoc, startTime, endTime, ppkg, mw = [], [], [], [], [], []
    for i in range(nt):
        l = read_ints(input_file[1+ns+i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route = np.zeros((nt, nl, nl), int)
    route = route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]] = 1

    tim = np.zeros((nt, mt, mt), int)
    tim = tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]] = 1
    return nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw, tim, route


def graph_fun(edges, weight, name):
    G = nx.MultiGraph(edges)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='green', node_size=500, alpha=1)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight, font_color='r')
    ax = plt.gca()
    for e in G.edges:
        ax.annotate("",
                    xy=pos[e[1]], xycoords='data',
                    xytext=pos[e[0]], textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="0.5",
                                    shrinkA=15, shrinkB=15,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3*e[2])
                                                                           ),
                                    ),
                    )

    plt.axis('off')
    plt.show()


def create_edges(start, end, weight, t1, t2, p):
    #print(start, end)
    output = [(start[a], end[a]) for a in range(len(start))]
    weight = {output[a]: str(weight[a]) + "," + str(t1[a]) + "," +
              str(t2[a]) + "," + str(p[a]) for a in range(len(output))}
    return output, weight


def collect_output(start, end, testcase, i):
    file = open(f"testset_1_output/Algo{i}/test_{testcase}.out")
    output_temp = []
    for f in file:
        res = []
        for i in f.split(" "):
            z = f.split(" ")
            if not "\n" in i:
                res.append(i)
        output_temp.append(res)
    output = []
    # print(weight_temp)
    for o in range(len(output_temp)):
        # print(output_temp[o])
        if len(output_temp[o]) != 0:
            for i in output_temp[o]:
                output.append((start[int(i)], end[int(i)]))
    arr = [oo for out in output_temp for oo in out]
    print(arr)
    weight = {output[a]: arr[a] for a in range(len(output))}
    print(weight, output)
    return output, weight


def draw_figure(testcase, algo):
    # inputs
    nl, mt, ns, nt, orgs, dests, wght, time, pps, startTripLoc, endTripLoc, startTime, endTime, ppkg, mw, tim, route = read_input(
        f"testset_1/test_{testcase}.in")
    input_trip_edges, weight_i_t = create_edges(
        startTripLoc, endTripLoc, mw, startTime, endTime, ppkg)
    input_ship_edges, weight_i_s = create_edges(
        orgs, dests, wght, [0]*ns, time, pps)
    output_path, weight_o = collect_output(
        startTripLoc, endTripLoc, testcase, algo)

    # graph
    graph_fun(input_trip_edges, weight_i_t, "Input Trips")
    graph_fun(input_ship_edges, weight_i_s, "Input Shipment Org and Dest")
    graph_fun(output_path, weight_o, "Output Shipment Trips")


draw_figure(0, 4)
