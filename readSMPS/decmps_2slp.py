# -*- coding: utf-8 -*-
"""
Created on May 4

---Based on the 2-stage stochastic program structure
---Assumption: RHS is random
---decompose the 2slp problem into a master and subproblems
---save the distributoin of the random variables and return the 
---random variables

@author: Siavash Tabrizian - stabrizian@gmail.com - stabrizian@smu.edu
"""

from readCOR  import readcor
from readSTOC import readstoc
from readTIM  import readtim


class prob:
    def __init__(self, name):
        #Import the Mean problem
        cor = readcor(name)
        cor.readfile()
        cor.get_mean()
        self.mean_model = cor.mean_model
        self.mean_vars   = cor.mean_vars
        self.mean_const  = cor.mean_const
        self.mean_sol = cor.mean_sol
        self.mean_status = cor.mean_status
        self.mean_objVal = cor.mean_objVal
        self.mean_var_size   = cor.mean_var_num
        self.mean_const_size = cor.mean_const_num
        self.master_model = self.mean_model
        self.master_vars  = self.mean_vars
        self.master_const = self.mean_const
        self.master_var_size  = 0
        self.master_const_size= 0
        self.sub_model = self.mean_model
        self.sub_vars  = self.mean_vars
        self.sub_const = self.mean_const
        self.sub_var_size  = 0
        self.sub_const_size= 0
        

class RandVars:
    def __init__(self,name):
        #Import stochastic information
        stoc = readstoc(name)
        stoc.readfile()
        self.rv = stoc.rv
        self.dist = stoc.dist
        self.cumul_dist = stoc.cumul_dist
        self.rvnum = stoc.rvnum
 
class TIME:
    def __init__(self,name):
        #Import time information
        tim = readtim(name)
        tim.readfile()
        self.stage_names = tim.stage
        self.stage_idx_col   = list()
        self.stage_idx_row   = list()
        self.stage_size  = tim.stagenum
        
class decompose:
    def __init__(self,name,dirr): # dirr = ".\\Input\\"
        self.name = dirr + name + "\\" + name
        self.prob = prob(self.name)     #Prob information
        self.RV   = RandVars(self.name) #Random variabels
        self.tim  = TIME(self.name)     #Time information(stages)

        
    #find the index of stages (rows and columns)
    def find_stage_idx(self):
        #initialize the index structs
        self.tim.stage_idx_col = list()
        self.tim.stage_idx_row = list()
        #find the column indexes (associated with variables)
        for i in range(0,self.tim.stage_size):
            count = 0
            for j in self.prob.mean_vars:
                if self.tim.stage_names[i][0] == j.varname:
                    self.tim.stage_idx_col.append(count)
                    break
                count += 1

            
        #find the row indexes (associated with constraints)
        for i in range(0,self.tim.stage_size):
            emp = [x for x in self.prob.mean_const if 
                               x.constrname == self.tim.stage_names[i][1]]
            if emp == []:
                tmp = 0
            else:
                tmp = self.prob.mean_const.index(emp[0])
            #add the init and end index of the column of stage i
            self.tim.stage_idx_row.append(tmp)
    
    def create_master(self):
        self.prob.master_vars = self.prob.master_vars[:self.tim.stage_idx_col[0]+1]
        self.prob.master_const = self.prob.master_const[:self.tim.stage_idx_row[0]+1]
        
        
        
        
        
        
        
        
        
        