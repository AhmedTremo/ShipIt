import os
from Genetic_Algorithm import runFile
import Greedy
import DP
import IP
import numpy as np
import csv
import time as tm

def read_ints(s):
    return [int(i) for i in s.split(' ')]
def read_input(input_filepath):
    with open(input_filepath, 'r') as f:
        input_file = f.read().split('\n')
    nl,mt,ns,nt = read_ints(input_file[0])
    orgs, dests, wght, time,pps = [], [], [], [], []
    for i in range(ns):
        l = read_ints(input_file[1 + i])
        orgs.append(l[0])
        dests.append(l[1])
        wght.append(l[2])
        time.append(l[3])
        pps.append(l[4])
    startTripLoc,endTripLoc,startTime,endTime,ppkg,mw=[],[],[],[],[],[]
    for i in range(nt):
        l = read_ints(input_file[1+ns+i])
        startTripLoc.append(l[0])
        endTripLoc.append(l[1])
        startTime.append(l[2])
        endTime.append(l[3])
        ppkg.append(l[4])
        mw.append(l[5])
    route=np.zeros((nt,nl,nl),int)
    route=route.tolist()
    for t in range(nt):
        route[t][startTripLoc[t]][endTripLoc[t]]=1

    tim=np.zeros((nt,mt,mt),int)
    tim=tim.tolist()
    for t in range(nt):
        tim[t][startTime[t]][endTime[t]]=1
    return nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw,tim,route

fields = ["test_case", "ns", "nt", "Genetics_z", "Genetics_t", "Greedy_z", "Greedy_t", "DP_z", "DP_t", "IP_z", "IP_t"]
rows=[]

folderPathAlgo1=os.path.join("testset_1_output","Algo1")
folderPathAlgo2=os.path.join("testset_1_output","Algo2")
folderPathAlgo3=os.path.join("testset_1_output","Algo3")
folderPathAlgo4=os.path.join("testset_1_output","Algo4")
os.makedirs(folderPathAlgo1, exist_ok = True)
os.makedirs(folderPathAlgo2, exist_ok = True)
os.makedirs(folderPathAlgo3, exist_ok = True)
os.makedirs(folderPathAlgo4, exist_ok = True)

def getCosts(array,ppkg,wght):
    res=[]
    for s in range(len(array)):
        shipWght=0
        for t in array[s]:
            shipWght+=ppkg[t]*wght[s]
        res.append(shipWght)
    return res


def writeFile(folderPath,i,array,costs):
    filename=os.path.join(folderPath,"test_"+str(i)+".out")
    f = open(filename, "w")
    for s in range(len(array)):
        genString=""
        for t in array[s]:
            genString+=str(t)+" "
        genString+=str(costs[s])
        f.writelines(str(genString)+"\n")

def writeFiles(i,arrayGen,arrayGre,arrayDP,arrayIP,ns,nt,ppkg,startTripLoc,endTripLoc,startTime,endTime,wght):
    costsGen=getCosts(arrayGen,ppkg,wght)
    writeFile(folderPathAlgo1,i,arrayGen,costsGen)
    costsGre=getCosts(arrayGre,ppkg,wght)
    writeFile(folderPathAlgo2,i,arrayGre,costsGre)
    costsDP=getCosts(arrayDP,ppkg,wght)
    writeFile(folderPathAlgo3,i,arrayDP,costsDP)
    costsIP=getCosts(arrayIP,ppkg,wght)
    writeFile(folderPathAlgo4,i,arrayIP,costsIP)

for i in range(23):
    print(i)
    nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw,tim,route=read_input(f"testset_1/test_{i}.in")
    shipmentTimes = [0]*ns
    start = tm.time()
    delGen,arrayGen=runFile(i)
    end =tm.time()
    timeGen=end-start
    print(delGen,arrayGen)

    nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw,tim,route=read_input(f"testset_1/test_{i}.in")
    start = tm.time()
    delGre,arrayGre=Greedy.run(ns,nt,nl,mt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs,dests,wght,time,pps)
    end=tm.time()
    timeGre=end-start
    print(delGre,arrayGre)

    nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw,tim,route=read_input(f"testset_1/test_{i}.in")
    if i<6:
        start = tm.time()
        delDP,arrayDP=DP.run(ns,nt,ppkg,mw,startTripLoc,endTripLoc,startTime,endTime,orgs,dests,wght,time,pps,shipmentTimes)
        arrayDP=DP.fixArray(arrayDP,ns)
        end =tm.time()
        timeDP=end-start
        print(delDP,arrayDP)
        DP.memo={}
    else:
        delDP=0
        arrayDP=[]
        timeDP=0
    nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw,tim,route=read_input(f"testset_1/test_{i}.in")
    if i<8:
        start = tm.time()
        delIP,arrayIP=IP.run(ns,nt,nl,mt,ppkg,mw,route,tim,orgs,dests,wght,time,pps)
        end =tm.time()
        timeIP=end-start
        print(delIP,arrayIP)
    else:
        delIP=0
        arrayIP=[]
        timeIP=0
    rows.append([i,str(ns),str(nt),str(delGen),str(int(timeGen)),str(delGre),str(int(timeGre)),str(delDP),str(int(timeDP)),str(delIP),str(int(timeIP))])
    writeFiles(i,arrayGen,arrayGre,arrayDP,arrayIP,ns,nt,ppkg,startTripLoc,endTripLoc,startTime,endTime,wght)
    timeDP = 0
    timeIP = 0
    delDP = 0
    delIP = 0
    

# filename = os.path.join("summary.csv")
# # writing to csv file 
# with open(filename, 'w') as csvfile: 
#     csvwriter = csv.writer(csvfile) 
#     csvwriter.writerow(fields)  
#     csvwriter.writerows(rows)
