# @file SimplexSolverADT.py
# @author Hanane Zlitni
# @brief This module contains all functions needed for solving linear programs using the simplex method.
# @date Dec 17, 2018

import numpy as np
import Exceptions
import ast, getopt, sys, copy, os
from enum import Enum

# *************** Clear console (cross-platform) ***************
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Goal(Enum):
    MAX = 'max'
    MIN = 'min'

class SimplexSolverADT():
    def __init__(self):
        self.LCs = []
        self.Constants = []
        self.objcFunc = []
        self.sTableau = []
        self.entering = []
        self.departing = []
        self.LCsType = []
        self.goal = Goal.MAX.value
        self.wasMin = False
    #end constructor

# ****************************** Getters ******************************
    def getEnteringVariable(self): 
        #The entering variable is obtained by finding the most negative value in the last row
        lastRow = self.sTableau[len(self.sTableau) - 1]
        iMostNegative = 0
        mostNegative = lastRow[iMostNegative]
        for index, value in enumerate(lastRow):
            if value < mostNegative:
                mostNegative = value
                iMostNegative = index
        return iMostNegative
    #end getEnteringVariable()
             
    def getDepartingVariable(self, iEntering):
        #The departing variable is obtained by fiding min(ratio), where ratio = (value in pivot column / constant in same row)
        temp = 0
        iMinRatio = -1
        minRatio = 0
        for index, x in enumerate(self.sTableau):
            if x[iEntering] != 0 and x[len(x)-1]/x[iEntering] > 0:
                temp = index
                iMinRatio = index
                minRatio = x[len(x)-1]/x[iEntering]
                break
        
        if minRatio > 0:
            for index, x in enumerate(self.sTableau):
                if index > temp and x[iEntering] > 0:
                    ratio = x[len(x)-1]/x[iEntering]
                    if minRatio > ratio:
                        minRatio = ratio
                        iMinRatio = index
        
        return iMinRatio
    #end getDepartingVariable()
    
    def getOptimum(self):
        #Get the optimum from sTableau
        optimum = {}
        for x in self.entering:
            if x is not 'Constants':
                if x in self.departing:
                    optimum[x] = self.sTableau[self.departing.index(x)]\
                                  [len(self.sTableau[self.departing.index(x)])-1]
                else:
                    optimum[x] = 0
        optimum['z'] = self.sTableau[len(self.sTableau) - 1]\
                          [len(self.sTableau[0]) - 1]
        
        if (self.wasMin):
            optimum['z'] = optimum['z'] * -1

        return optimum
    #end getOptimum()

# ****************************** Main Functions ******************************
    def solveLP(self, LCs, Constants, objcFunc, LCsType=[], goal=Goal.MAX.value):
        #Main simplex method function
        try:
            if (LCs == [] or Constants == [] or objcFunc == []):
                raise Exceptions.MISSING_INPUT
            else: 
                self.LCs = LCs
                self.Constants = Constants
                self.LCsType = LCsType

            self.goal = goal
            
            #If the goal is 'min', multiple the objective function by -1
            if (self.goal == Goal.MIN.value):
                self.wasMin = True
                self.objcFunc = [-1 * x for x in objcFunc]
                self.goal = Goal.MAX.value
            else:
                self.objcFunc = objcFunc

            #Construct the simplex tableau
            self.formSimplexTableau()

            #Update the values in the entering and departing lists
            self.updateEnteringDepartingVars(self.sTableau)
                
            #Determine whether to proceed to the next iteration in the simplex method steps 
            #or stop by looking for negative values in the last row (excluding the constants column)
        
            while (not self.isOptimumFound()):
                #Find non-negative pivot. If it is negative, there is no optimal solution for the LP
                pivot = self.findPivot()

                if pivot[1] < 0:
                    raise Exceptions.NO_OPTIMAL_SOLUTION

                #Otherwise, perform row operations
                self.pivot(pivot)

            #Get the optimum
            optimum = self.getOptimum()

            
            #If there is no optimum, raise an exception
            if (optimum == "" or optimum['z'] == 0):
                raise Exceptions.NO_OPTIMAL_SOLUTION
                
            #Otherwise, print the values of Z and the points where it occurs
            #The values are rounded and limited to 2 decimal points
            else:
                output = {'Z': round(optimum['z'],4)}
                output.update({k : round(v,4) for k, v in optimum.items() if 'x' in k})
                print(output)
                return output
                    
        except Exceptions.NO_OPTIMAL_SOLUTION:
            print("NO_OPTIMAL_SOLUTION: This linear program does not have an optimal solution.")
        
        except Exceptions.MISSING_INPUT:
            print("MISSING_INPUT: At least one input is missing.")
    #end solveLP()

    def formSimplexTableau(self):
        #Construct simplex tableau by adding the slack and artificial variables then appending the inputs to the matrix
        self.sTableau = copy.deepcopy(self.LCs)

        #Convert the tableau to the canonical form by adding the slack (for '<=' LCs) and artificial (for '=' LCs) variables
        self.toCanonical()
        
        objcFunc = copy.deepcopy(self.objcFunc)
        for index, elem in enumerate(objcFunc):
            objcFunc[index] = -elem
        self.sTableau.append(objcFunc + [0] * (len(self.Constants)+1))
    #end formSimplexTableau()

    def toCanonical(self):
        #Add slack and artificial variables
        slackVariables = []
        for i in range(0, len(self.sTableau)):
            row = []
            for j in range(0, len(self.sTableau)):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            slackVariables.append(row)

        for i in range(0, len(slackVariables)):
            self.sTableau[i] += slackVariables[i]
            self.sTableau[i] += [self.Constants[i]]
        
        self.LCsType = ['='] * len(self.Constants)
    #end toCanonical()

    def updateEnteringDepartingVars(self, matrix):
        #Create lists for entering and departing variables
        self.entering = []
        self.departing = []

        for i in range(0, len(matrix[0])):
            if i < len(self.LCs[0]):
                prefix = 'x'
                self.entering.append("%s_%s" % (prefix, str(i + 1)))
            elif i < len(matrix[0]) - 1:
                self.entering.append("s_%s" % str(i + 1 - len(self.LCs[0])))
                self.departing.append("s_%s" % str(i + 1 - len(self.LCs[0])))
            else:
                self.entering.append("Constants")
    #end updateEnteringDepartingVars()

    def findPivot(self):
        #Find the index of the pivot
        iEntering = self.getEnteringVariable()
        iDeparting = self.getDepartingVariable(iEntering)
        return [iEntering, iDeparting]
    #end findPivot()

    def pivot(self, iPivot):
        #Perform row operations
        j,i = iPivot

        pivot = self.sTableau[i][j]
        self.sTableau[i] = [element / pivot for
                           element in self.sTableau[i]]
        for index, row in enumerate(self.sTableau):
           if index != i:
              row_scale = [y * self.sTableau[index][j]
                          for y in self.sTableau[i]]
              self.sTableau[index] = [x - y for x,y in
                                     zip(self.sTableau[index],
                                         row_scale)]

        self.departing[i] = self.entering[j]
    #end pivot()

    def isOptimumFound(self):
        #Determine whether the optimum is found or not to proceed to the next iteration of the simplex method steps
        optimumFound = True
        index = len(self.sTableau) - 1
        for i, x in enumerate(self.sTableau[index]):
            if x < 0 and i != len(self.sTableau[index]) - 1:
                optimumFound = False
        return optimumFound
    #end isOptimumFound()
