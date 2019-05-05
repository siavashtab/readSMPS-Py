# -*- coding: utf-8 -*-
"""
Created on Sun May 05 11:41:17 2019

@author: stabr
"""

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
from gurobipy import *

class readcor:
    def __init__(self, name):
        self.name = ".\\Input\\" + name + "\\" + name + ".cor"
        self.rownum = 0
        self.colnum = 0
    
    ## Read the cor file
    def readfile(self):
        self.mean_model = read(self.name)
                    
                        
                    
                
        



