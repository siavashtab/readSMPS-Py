# -*- coding: utf-8 -*-
"""
Created on May 4 - 2019

---Based on the 2-stage stochastic program structure
---Assumption: RHS is random
---decompose the 2slp problem into a master and subproblems
---save the distributoin of the random variables and return the 
---random variables

@author: Siavash Tabrizian - stabrizian@smu.edu
"""

from readCOR  import readcor
from readSTOC import readstoc
from readTIM  import readtim

try:
    import gurobipy as gb
except ImportError as e:
    print('Gurobi is needed for building the problem optimization structure!')
    raise

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
        self.master_model = gb.Model('master_')
        self.master_vars  = self.mean_vars
        self.master_const = self.mean_const
        self.master_var_size  = 0
        self.master_const_size= 0
        self.sub_model = gb.Model('sub_')
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
        self.model_name = name
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
    
    def Reg_Objective(self,LinObj, var_dic):
        for vdic in var_dic.keys():
            LinObj += (vdic - var_dic[vdic]) * (vdic - var_dic[vdic])
        return LinObj
    
    # replace the observations in the proper location of the problem
    def replaceObs(self,obs,constr):
        obscount = 0
        for c in constr:
            if c.getAttr('ConstrName') in self.RV.rv:
                if len(obs) < obscount-1:
                    print("ERROR: Length of obs is less than rvs")
                    break;
                else:
                    c.setAttr('RHS',obs[obscount])
                    self.prob.mean_model.update()
                    obscount += 1

        return constr
    
    #Create master constraints
    def create_master_constr(self):
        constr = self.prob.mean_const[:self.tim.stage_idx_row[1]]
        for c in constr:
            empt = gb.LinExpr()
            for v in self.prob.master_vars:
                empt += self.prob.mean_model.getCoeff(c,v) * v
            self.prob.master_model.addConstr(empt,c.getAttr('Sense'),c.getAttr('RHS'),c.getAttr('ConstrName'))
            self.prob.master_model.update()
        self.prob.master_const = self.prob.master_model.getConstrs()
    
    #Create LSsub constraints
    def create_LSsub_constr(self,obs,incmbt):
        constr = self.prob.mean_const[self.tim.stage_idx_row[1]:]
        constr = self.replaceObs(obs,constr)
        for c in constr:
            empt = gb.LinExpr()
            Cx = 0
            for v in self.prob.sub_vars:
                empt += self.prob.mean_model.getCoeff(c,v) * v
            for v in range(len(self.prob.master_vars)):
                if 'eta' not in self.prob.master_vars[v].getAttr('VarName'):
                    Cx   += self.prob.mean_model.getCoeff(c,self.prob.master_vars[v]) * incmbt[v]
            self.prob.sub_model.addConstr(empt,c.getAttr('Sense'),c.getAttr('RHS') - Cx,c.getAttr('ConstrName'))
            self.prob.sub_model.update()
        self.prob.sub_const = self.prob.sub_model.getConstrs()
    
    #Creating linear master with one surrogates (\eta)
    def create_master(self):
        self.prob.master_vars = self.prob.master_vars[:self.tim.stage_idx_col[1]]
        self.prob.master_const = self.prob.master_const[:self.tim.stage_idx_row[1]]
        
        # Create surrogate variables 
        #eta = self.master_model.addVars ( *indices, lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS, name="" ) 
        for v in self.prob.master_vars:
            self.prob.master_model.addVar(lb=v.getAttr("LB"), ub=v.getAttr("UB"), obj=v.getAttr("Obj"), vtype=v.getAttr("VType"), name=v.getAttr("VarName"))
        self.prob.master_model.update()
        self.prob.master_vars = self.prob.master_model.getVars()
        eta = self.prob.master_model.addVar ( lb=0.0, ub=gb.GRB.INFINITY, obj=1.0, vtype=gb.GRB.CONTINUOUS, name="\eta") 
        self.prob.master_model.update()
        self.prob.master_vars.append(eta)
        
        #Building the master objective function
        obj_ = self.prob.mean_model.getObjective()
        varName = [j.getAttr("VarName") for j in self.prob.master_vars ]
        newobj_ = gb.LinExpr()
        newobj_ = eta
        for t in range(obj_.size()):
            if obj_.getVar(t).getAttr("VarName") in varName:
                newobj_ += obj_.getCoeff(t) * self.prob.master_vars[varName.index(obj_.getVar(t).getAttr("VarName"))]
        self.prob.master_model.setObjective(newobj_)
        self.create_master_constr()
    
    #Creating linear master with multiple surrogates(\eta0,\eta1,...) 
    def create_master_multi(self, scen_num):
        self.prob.master_vars = self.prob.master_vars[:self.tim.stage_idx_col[1]]
        self.prob.master_const = self.prob.master_const[:self.tim.stage_idx_row[1]]
        
        # Create surrogate variables 
        #eta = self.master_model.addVars ( *indices, lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS, name="" ) 
        for v in self.prob.master_vars:
            self.prob.master_model.addVar(lb=v.getAttr("LB"), ub=v.getAttr("UB"), obj=v.getAttr("Obj"), vtype=v.getAttr("VType"), name=v.getAttr("VarName"))
        self.prob.master_model.update()
        self.prob.master_vars = self.prob.master_model.getVars()
        varName = [j.getAttr("VarName") for j in self.prob.master_vars ]
        eta = self.prob.master_model.addVars(range(scen_num),lb=0.0, ub=gb.GRB.INFINITY, obj=1.0, vtype=gb.GRB.CONTINUOUS, name="\eta") 
        self.prob.master_model.update()
        for v in eta:
            self.prob.master_vars.append(eta[v])
        
        #Building the master objective function
        obj_ = self.prob.mean_model.getObjective()
        newobj_ = gb.LinExpr()
        for v in eta:
            newobj_ += eta[v]
        for t in range(obj_.size()):
            if obj_.getVar(t).getAttr("VarName") in varName:
                newobj_ += obj_.getCoeff(t) * self.prob.master_vars[varName.index(obj_.getVar(t).getAttr("VarName"))]
        self.prob.master_model.setObjective(newobj_)
        self.create_master_constr()

    #creating the Lshaped subproblem
    def create_LSsub(self,obs,incmb):
        self.prob.sub_vars  = self.prob.sub_vars[self.tim.stage_idx_col[1]:]
        self.prob.sub_const = self.prob.sub_const[self.tim.stage_idx_col[1]:]

        for v in self.prob.sub_vars:
            self.prob.sub_model.addVar(lb=v.getAttr("LB"), ub=v.getAttr("UB"), obj=v.getAttr("Obj"), vtype=v.getAttr("VType"), name=v.getAttr("VarName"))
        self.prob.sub_model.update()
        self.prob.sub_vars = self.prob.sub_model.getVars()
        self.create_LSsub_constr(obs,incmb)
    
        
        
        
        
        
        
        
        
        