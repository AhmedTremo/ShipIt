import numpy as np
import os

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
k = 0
Algo = [1,2,3,4]
detailed_data = [5,6,7,11]
detailed_output = ["detailed_output_1", "detailed_output_2", "detailed_output_3", "detailed_output_3"]
for i in detailed_data:
    filename=os.path.join("testset_1_output/",f"detailed_output_{k}.csv")
    fll = open(filename,"w")
    algo = ["features","Genetics", "Greedy", "DP", "IP"]
    for a in algo:
        fll.write(a + ",")
    fll.write("\n")
    k+=1
    nl,mt,ns,nt,orgs,dests,wght,time,pps,startTripLoc,endTripLoc,startTime,endTime,ppkg,mw,tim,route=read_input(f"testset_1/test_{i}.in")
    totalShipAll = []
    totalPriceAll = []
    totalWeightAll = []
    averageDelTimeAll = []
    averagePricePerShipAll = []
    for j in Algo:  
        print("TESTCASE ", i, " ALGO ",j)
        file = open(f"testset_1_output/Algo{j}/test_{i}.out")
        fileInp = open(f"testset_1/test_{i}.in")
        fileInp.readline()
        totalShip = 0
        totalPrice = 0
        totalWeight = 0
        averageDelTime = 0
        averagePricePerShip = 0
        for f in range(ns):
            if os.stat(f"testset_1_output/Algo{j}/test_{i}.out").st_size == 0:
                totalShip = -1
                totalPrice = -1
                totalWeight = -1
                break
            inp = fileInp.readline()
            #print("Input File",inp)
            inpDet = inp.split(" ")
            line = file.readline()
            details = line.split(" ")
            #print("Output File",details)
            if details[0] != "0\n":
                totalShip += 1
                totalWeight += int(inpDet[2])
                for t in details:                    
                    if "\n" in t:
                        totalPrice += int(details[len(details) - 1][:len(details[len(details) - 1])-1])
                        break;
                    #print("ENDTIME", endTime[int(t)], "STARTTIME", startTime[int(t)])
                    averageDelTime += endTime[int(t)] - startTime[int(t)] + 1
                    #print(endTime[int(t)] - startTime[int(t)] + 1)
                #print(averageDelTime)
        averageDelTime = averageDelTime/totalShip
        averagePricePerShip = totalPrice/totalShip
        totalShipAll.append(totalShip)
        totalPriceAll.append(totalPrice)
        totalWeightAll.append(totalWeight)
        averageDelTimeAll.append(averageDelTime)
        averagePricePerShipAll.append(averagePricePerShip)
    res = []
    res.append(totalShipAll)
    res.append(totalPriceAll)
    res.append(totalWeightAll)
    res.append(averageDelTimeAll)
    res.append(averagePricePerShipAll)
    features = ["Total no. of Shipments", "Total Price Paid", "Total Weight", "Average Delievery Time", "Average Price Per Shipment"]
    for z in range(len(features)):
        fll.write(features[z]+",")
        for n in res[z]:
            if n == 0 or n == -1 or n == 1:
                fll.write("-1,")
            else:
                fll.write(str(n)+",")
        fll.write("\n")
        
fll.close()
        

    
                
  
        
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    