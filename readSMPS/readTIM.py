
"""
Created on May 4 - 2019

---Based on the 2-stage stochastic program structure
---Assumption: RHS is random
---read stoc file (.tim)
---save the distributoin of the random variables and return the 
---random variables

@author: Siavash Tabrizian - stabrizian@gmail.com - stabrizian@smu.edu
"""

class readtim:
    def __init__(self, name):
        self.name = name + ".tim"
        self.stage = list()
        self.stagenum = 0
    
    ## Read the stoc file
    def readfile(self):
        with open(self.name, "r") as f:
            data = f.readlines()
        #go through the time file
        count = 0
        for line in data:
            words = line.split()
            #print words
            if len(words) > 2:
                tmp = list()
                tmp.append(words[0])
                tmp.append(words[1])
                self.stage.append(tmp)
                count += 1
        
        self.stagenum = count
        if count > 2:
           print "ERROR: more than two stages"               
                    
                        
                    
                
        



