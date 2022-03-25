import random

# test values for gamma and alpha
alpha=0.6
gamma=0.4
r=[0,0,0,0,0,0,1]

states_list=[1,2,3,4,5]
dict={0:"left terminating state",1:"A",2:"B",3:"C",4:"D",5:"E",6:"right terminating state"}
dict_keys=list(dict.keys())
dict_vals=list(dict.values())
#LETS START WITH STATE A
graph=[[0,0,0,0,0,0,0],
        [1,0,1,0,0,0,0],
        [0,1,0,1,0,0,0],
        [0,0,1,0,1,0,0],
        [0,0,0,1,0,1,0],
        [0,0,0,0,1,0,1],
        [0,0,0,0,0,0,0]]


st_array=[]

#Find different random episodes 


def findEpisode(matrix,presentState,dict,states_array):
    visitable=[]
    states_array.append(dict[presentState])
    if presentState==0 or presentState==6:
        return states_array
    else:    
        for i in range(7):
            if matrix[presentState][i]==1:
                visitable.append(i)    
        return findEpisode(matrix,random.choice(visitable),dict,states_array)
        

#find multiple episodes given the number of episodes

def findMultipleEpisodes(matrix,dict,n,startState):
    
    epi_graph=[]
    for i in range(n):
        states_array_two=[]
        epi_graph.append(findEpisode(matrix,startState,dict,states_array_two))
    return epi_graph



svf=[0,0,0,0,0,0,0]

#####  evaluate state value functions of each state after obtaining multiple episodes, using MC learning  #######

######## V(s)  <--  V(s)+alpha*(Rt+gamma*V(s+1)-V(s))
def mc(episodes,dict_keys,dict_vals,svf,alpha,gamma,r):
    epi_graph=findMultipleEpisodes(graph,dict,episodes,3)
    # print(epi_graph)
    for episode in range(len(epi_graph)):
        
        for state in range(len(epi_graph[episode])-1): 
            if epi_graph[episode][state+1]=="left terminating state":
                svf[dict_keys[dict_vals.index(epi_graph[episode][state])]]=svf[dict_keys[dict_vals.index(epi_graph[episode][state])]]+ alpha*(-1*svf[dict_keys[dict_vals.index(epi_graph[episode][state])]])
            elif epi_graph[episode][state+1]=="right terminating state":  
                svf[dict_keys[dict_vals.index(epi_graph[episode][state])]]=svf[dict_keys[dict_vals.index(epi_graph[episode][state])]]+alpha*(1-svf[dict_keys[dict_vals.index(epi_graph[episode][state])]])
            else:
                    
                svf[dict_keys[dict_vals.index(epi_graph[episode][state])]]=svf[dict_keys[dict_vals.index(epi_graph[episode][state])]]+alpha*(r[dict_keys[dict_vals.index(epi_graph[episode][state+1])]]+gamma*svf[dict_keys[dict_vals.index(epi_graph[episode][state+1])]]-svf[dict_keys[dict_vals.index(epi_graph[episode][state])]])
    return svf 



print("10 episodes\n",mc(10,dict_keys,dict_vals,svf,alpha,gamma,r))
print("25 episodes\n",mc(25,dict_keys,dict_vals,svf,alpha,gamma,r))           
print("100 episodes\n",mc(100,dict_keys,dict_vals,svf,alpha,gamma,r))
                     