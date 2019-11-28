#  readSMPS-Py

[—[Source]—](https://github.com/siavashtab/readSMPS-Py/tree/master/src)
[—[license]—](https://github.com/siavashtab/readSMPS-Py/blob/master/LICENSE)

reading SMPS format files for two-stage stochastic programs

------------------

##  Author: Siavash Tabrizian -- stabrizian@smu.edu

------------------

## Intoduction:

readSMPS: A package for reading and saving the information of two stage stochastic programs from SMPS files

There are implementations for reading SMPS files which are either written in other 
programming languages (C or Julia) or do not provide a suitable data structures for L-shaped 
based algorithms (based on GUROBI solver). Moreover, it would be crucial to facilitate the problem that can handle sampling 
techniques for stochastic programming which can be done in this code.

-  this package store the problem information in GUROBI format
-  the distribution of random variables are discrete (even if it is not discrete it can be turned to a discrete distribution)
-  randomness is on the right handside of the recourse problem
-  COR file contains the mean value problem which its optimal value yields a lower bound

------------------

## Dependencies:

- This package needs the GUROBI solver for optimization parts (https://www.gurobi.com/), 
  and the problem will be created based on the  GUROBI objects.

------------------

## Output

- this program will read the SMPS files, decompose the problem
  into a master and subproblem based on the GUROBI objects. 
  The data structure in which problems will be stored are all defined in prob_struct.h

------------------

## SMPS 

- SMPS is an efficient and effective way of describing stochastic programs. 

  It contains the follwoing files:
  
  1 - _.cor:
  
     This file is the core of the formulation which is basically derived from the 
	 mean value problem. It's format is very similar to _.mps files.
	 
  2 - _.tim
    
	This file contains the information of stages. The name of rows and columns 
	associated with each stage
	
  3 - _.sto
  
    This file contains the information about the random variables, and their distribution.
	Also, it shows the place in which the random variables appear in the second stage problem

-------------------

## Description

The program can be runned by specifying the instance name and directory and the suitable problems can be created
~~~~
>> d = decompose("pgp2",".\\Input\\")
>> d.find_stage_idx()
>> d.create_master()
~~~~

