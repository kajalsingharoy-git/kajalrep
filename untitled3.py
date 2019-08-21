import networkx as nx
import random as rd
import pandas as pd
import csv


rnum=[] #list of random degrees
nodedict={} #Dict of nodes:degree
ndlist=[] #list of nodes having degree>0
toremove=[] #list of nodes having degree 0
edlist=[] #list of edges
cluster=[] #Dict of Cluster number:Nodes
connode=[] #list of bridging nodes
c1=1 #starting node of cluster
c2=1 #ending  node of cluster

noc=input("Enter Total no. of clusters: ")
noc=int(noc)


for d in range(noc):
    nodedict.clear()
    
###Arrange criterias for clusters    
    nn=input("\n\nEnter no. of nodes for Cluster %d: " %(d+1))
    nn=int(nn)
    c1=c2
    c2=c1+nn
    print("C1 &C2: ", c1,c2)
    
    mpe=int((nn*(nn-1))/2)  #Max possible edge of cluster
    cr1=int(mpe*0.6) #Max possible edge x60%
    mindeg=int((nn-1)*0.40) #40% of total no of nodes in cluster
    maxdeg=nn-1

    
###Create Clusters
    for i in range(1, nn+1): #generating list of random degrees
        rnum.append(rd.randint(mindeg, maxdeg))
        #print("random degrees:", i)


    for i in range(c1, c2): #assigning degree to nodes
        #print("Nodes", i)
        nodedict[i]= rnum[i-1]
    cluster.append(list(nodedict.keys()))

    #print("\n\nNode:Degree ", nodedict)

    for i in nodedict.keys(): #creating list of node having degree>0
        ndlist.append(int(i))

    while len(ndlist)>1:
        #print("\n\nNodes Available for selection: ", ndlist)
        n1=rd.choice(ndlist) #generate rd node from ndlist
        n2=rd.choice(ndlist)
        #print("\nnode selection: %d & %d" %(n1,n2))

        if(n1!=n2): 
            edlist.append([n1,n2]) #add to edglist
            nodedict[n1] -=1 #decrease degree of node n1 by 1
            nodedict[n2] -=1

        for i in nodedict.keys():
            if(nodedict.get(i)==0):
                #print("\nNode %d value: " %(i), nodedict.get(i), ", Gets Popped")
                toremove.append(i) #create list of nodes having degree 0
        
        for i in toremove:
            nodedict.pop(i) #remove nodes from nodedict having degree 0
        toremove=[] #empty list

        ndlist=[] #empty list      
        for i in nodedict.keys():
            ndlist.append(int(i)) ##creating list of node having degree>0

    print("Cluster %d Done --------------------------------------------------------" %(d+1))

print("\n\n")

c2=c2-1

print("\nNo. of Nodes in Network Before Bridging: ", c2,"\n")

rnc=[]
for i in range(noc):
    rnc.append(i)


cmb=[]
while noc>0:
    rr=rd.choice(rnc)
    rr2=rd.choice(rnc)
    if rr != rr2:
        temp1=[[rr,rr2]]
        temp2=[[rr2,rr]]
        if temp1 not in cmb and temp2 not in cmb:
            print("rr2 & rr: ", rr2, rr)
            nob=int((len(cluster[rr2])+len(cluster[rr]))*0.1)
            print("NOB of Cluster%d & Cluster%d:" %(rr2, rr), nob)
            for j in range(nob):
                r1=rd.choice(cluster[rr2])
                r2=c2+1
                r3=rd.choice(cluster[rr])
                edlist.append([r1,r2])
                edlist.append([r2,r3])
                connode.append(r2)
                c2=r2
        cmb.append(temp1)
        cmb.append(temp2)
        noc -= 1
    
#print("Clusters: ", cluster)        
#print("\n\nTotal no of bridging node:", len(brnodes))
#print("\nList of bridging nodes", brnodes)
print("\nLength of Connecting nodes: ", len(connode))
print("\nConnecting nodes: ", connode)
print("\nNo. of Nodes in Network After Bridging: ", c2)
#print("\n\nFinal Edgelist List: ", edlist)


G = nx.Graph()
G.add_edges_from(edlist)
G.add_edges_from(edlist)

print(nx.draw(G, with_labels=True))   

edlist=[['n','m']] + edlist
#print(edlist)

#Writing to CSV file with each element of list being a separate row

with open('Network.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(edlist)

csvFile.close()