# -*- coding: utf-8 -*-
"""
Created on May 4

---Based on the 2-stage stochastic program structure
---Assumption: RHS is random
---read stoc file (.sto)
---save the distributoin of the random variables and return the 
---random variables

@author: Siavash Tabrizian - stabrizian@gmail.com - stabrizian@smu.edu
"""

class readstoc:
    def __init__(self, name):
        self.name = name + ".sto"
        self.rv = list()
        self.dist = list()
        self.cumul_dist = list()
        self.rvnum = 0
    
    ## Read the stoc file
    def readfile(self):
        with open(self.name, "r") as f:
            data = f.readlines()
        count = 0
        cumul = 0
        for line in data:
            words = line.split()
            #print words
            if len(words) > 2:
                if words[0] != "RHS":
                    print"ERROR: Randomness is not on the RHS"
                else:
                    #store the name of the random variables
                    if words[1] not in self.rv:
                        cumul = 0
                        self.rv.append(words[1])
                        tmp = list()
                        tmp.append({float(words[2]):float(words[3])})
                        self.dist.append(tmp)
                        tmp = list()
                        tmp.append({float(words[2]):float(words[3])})
                        self.cumul_dist.append(tmp)
                        count += 1
                    else:
                        cumul += float(words[3])
                        tmp = list()
                        tmp.append({float(words[2]):float(words[3])})
                        rvidx = self.rv.index(words[1])
                        self.dist[rvidx].append(tmp)
                        tmp = list()
                        tmp.append({float(words[2]):cumul})
                        self.cumul_dist[rvidx].append(tmp)
        
        #count contains the number of rvs
        self.rvnum = count
                    
                        
                    
                
        



