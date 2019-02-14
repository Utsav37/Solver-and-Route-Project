#!/usr/bin/env python3
# put your routing program here!

import sys
import math

def map_latlong(Filename):
    f=open(Filename,'r')
    data=f.read()
    la=data.split('\n')
    la =la[0:len(la)-1]

    map={}
    for row in la:
        templist=row.split(' ')
        map[templist[0].replace('"','')]=[float(templist[1]),float(templist[2])]
    return map

def map_locations(Filename):
    f=open(Filename,'r')
    data=f.read()
    la=data.split('\n')
    la =la[0:len(la)-1]
    map={}
    for row in la:
        templist=row.split(' ')
        if templist[0] in (list(map.keys())):
            tempvalues=map[templist[0]]
            tempvalues.append(templist[1:5])
            map[templist[0]]=tempvalues
        else:
            map[templist[0]] = [templist[1:5]]
        if templist[1] in (list(map.keys())):
            tempvalues=map[templist[1]]
            tempvalues.append(templist[0:1]+templist[2:5])
            map[templist[1]]=tempvalues
        else:
            map[templist[1]] = [templist[0:1]+templist[2:5]]
    return map

def map_highway():
    high={}
    for each in MAP:
        for t in MAP[each]:
            if t[4] not in list(high.keys()):
                high[t[4]]=[eacht[4] for eacht in MAP[t[0]]]
            else:
                temp=high[t[4]]
                temp.append([eacht[4] for eacht in MAP[t[0]]])
                high[t[4]]=temp
    return high



def is_goal(city):
    if (city==destination):
        return True
    return False

def result(lst_res):
    return str(int(lst_res[1]))+' '+str(lst_res[2])+lst_res[0]

def successors(parent):
    succ=[]
    src=parent[0][parent[0].rindex(' ')+1:]
    ldst=MAP[src]

    for each in ldst:
        if each[2]=='' or each[2]=='0' or each[0] in parent[0]:
            continue
        else:
            temp = [parent[0] +' '+each[0],round((float(each[1])+float(parent[1])),3),
                            round((parent[2]+float(each[1])/float(each[2])),3)]
        succ.append(temp)

    return(succ)

def solve_breadth(initial_board):
    fringe = [[' '+initial_board,0,0]]
    visited_nodes=[]
    for p in fringe:
        visited_nodes.append(p[0][p[0].rindex(' ')+1:])
        for s in successors(p):
            child=s[0][s[0].rindex(' ')+1:]
            if is_goal(child):
                return(s)
            if child not in visited_nodes:
                fringe.append(s)
    return False

def solve_depth(initial_board,k=0):
    fringe = [[' '+initial_board,0,0]]
    while len(fringe) > 0:
        pop_parent=fringe.pop()
        if (algo=='ids' and (pop_parent[0].count(' ')+1>=k)):
            continue
        for s in successors(pop_parent):
            child = s[0][s[0].rindex(' ') + 1:]
            if is_goal(child):
                return(s)
            fringe.append(s)
    return False

def solve_ids(initial_board):
    for i in range(3,len(MAP),3):
        res=solve_depth(initial_board,i)
        if res != False:
            return res
    return False

def solve_uniform(initial_board):
    visited_nodes = [initial_board]
    fringe = [[' '+initial_board,0,0]]
    while len(fringe)>0:
      #  print('fringe=', fringe)
        p=0
        if cost_func=='distance':
            j=1
        else:
            j=2
        if cost_func in ('distance','time'):
            for i in range(1,len(fringe)):
                if fringe[i][j]<fringe[p][j]:
                    p=i
        visited_nodes.append(fringe[p][0][fringe[p][0].rindex(' ')+1:])
        if is_goal( fringe[p][0][fringe[p][0].rindex(' ')+1:]):
            return (fringe[p])
        for s in successors(fringe[p]):
            child = s[0][s[0].rindex(' ') + 1:]
            if child not in visited_nodes:
                fringe.append(s)
        fringe=fringe[0:p]+fringe[p+1:]
    return False

def solve_astar(initial_board):
    visited_nodes = [initial_board]
    fringe = [[' '+initial_board,0,0]]
    while len(fringe)>0:
      #  print('fringe=', fringe)
        p=0
        if cost_func=='distance':
            j=1
        else:
            j=2
        if cost_func in ('distance','time'):
            for i in range(1,len(fringe)):
                childi = fringe[i][0][fringe[i][0].rindex(' ') + 1:]
                childp = fringe[p][0][fringe[p][0].rindex(' ') + 1:]
                if childi not in list(LATLONG.keys()) or childp not in list(LATLONG.keys()) or cost_func == 'time':
                    if (fringe[i][j]) < (fringe[p][j]):
                        p = i
                else:
                    Eucdistp=math.sqrt((abs(LATLONG[childp][0])-abs(LATLONG[destination][0]))**2+(
                        abs(LATLONG[childp][1])-abs(LATLONG[destination][1]))**2)
                    Eucdisti = math.sqrt((abs(LATLONG[childi][0]) - abs(LATLONG[destination][0])) ** 2 + (
                            abs(LATLONG[childi][1]) - abs(LATLONG[destination][1])) ** 2)
                    if (fringe[i][j]+Eucdisti)<(fringe[p][j]+Eucdistp):
                        p=i
        visited_nodes.append(fringe[p][0][fringe[p][0].rindex(' ')+1:])
        if is_goal( fringe[p][0][fringe[p][0].rindex(' ')+1:]):
            return (fringe[p])
        for s in successors(fringe[p]):
            child = s[0][s[0].rindex(' ') + 1:]
            if child not in visited_nodes:
                fringe.append(s)
        fringe=fringe[0:p]+fringe[p+1:]
    return False

def opt_y_n(opt_r,in_r):

    if (cost_func=='distance'):
        if in_r[1]<=opt_r[1]:
            return 'yes'
        else:
            return 'no'
    elif (cost_func=='time'):
        if in_r[2]<=opt_r[2]:
            return 'yes'
        else:
            return 'no'
    else:
        if in_r[0].count(' ')<=opt_r[0].count(' '):
            return 'yes'
        else:
            return 'no'






source=str(sys.argv[1])
destination=str(sys.argv[2])
algo=str(sys.argv[3])
cost_func=str(sys.argv[4])
MAP=map_locations('road-segments.txt')
LATLONG=map_latlong('city-gps.txt')

if algo == 'bfs':
    in_res=solve_breadth(source)
elif algo == 'dfs':
    in_res=solve_depth(source)
elif algo == 'ids':
    in_res =solve_ids(source)
elif algo == 'uniform':
    in_res =solve_uniform(source)
elif algo == 'astar':
    in_res =solve_astar(source)
else:
    print("Error input. Please try again")
    exit(0)

opt_res=solve_astar(source)
print(opt_y_n(opt_res,in_res)+' '+result(in_res))
