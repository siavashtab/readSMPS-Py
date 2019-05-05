# -*- coding: utf-8 -*-
"""
Created on May 4

---Based on the 2-stage stochastic program structure
---Assumption: RHS is random
---read cor file (.mps)
---save the distributoin of the random variables and return the 
---random variables

@author: Siavash Tabrizian - stabrizian@gmail.com - stabrizian@smu.edu
"""
from gurobipy import *

class readcor:
    def __init__(self, name):
        self.name = ".\\Input\\" + name + "\\" + name + ".mps"
        self.rownum = 0
        self.colnum = 0
    
    ## Read the cor file
    def readfile(self):
        self.mean_model = read(self.name)
    
    ## Get the mean model information
    def get_mean(self):
        self.mean_vars   = self.mean_model.getVars()
        self.mean_const  = self.mean_model.getConstrs()
        self.mean_model.optimize()
        print"Mean value optimal: "
        self.mean_model.printAttr('x')
        self.mean_sol = [o.getAttr('x') for o in self.mean_vars]
        self.mean_status = self.mean_model.Status
        self.mean_objVal = self.mean_model.objVal
        self.mean_var_num   = len(self.mean_vars)
        self.mean_const_num = len(self.mean_const)
                                
        
                    
                        
                    
                
        



