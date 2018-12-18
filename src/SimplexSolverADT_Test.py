# @file SimplexSolverADT_Test.py
# @author Hanane Zlitni
# @brief This file contains the system and unit test cases
# @date Dec 17, 2018

from SimplexSolverADT import SimplexSolverADT
import Exceptions
import unittest

class SimplexSolverADT_Test(unittest.TestCase):

    #****************** SYSTEM V&V TEST CASES ******************
    #Maximization with optimum 
    def testMaxOpt1(self):
        self.assertDictEqual({'Z': 3.0,'x_1': 0,'x_2': 0,'x_3': 3.0}, 
                              SimplexSolverADT().solveLP([[1,1,1],[4,-3,1],[2,1,-1]],[10,3,10],[2,-3,1],[],'max')
                            )

    #Maximization with no optimum  
    def testMaxNoOpt(self):
        self.assertRaises(Exceptions.NO_OPTIMAL_SOLUTION, 
                              SimplexSolverADT().solveLP([[1,-1],[2,-1]],[10,40],[2,1],[],'max')
                            )

    #Minimization with optimum 
    def testMinOpt(self):
        self.assertDictEqual({'Z': -4.5714,'x_1': 2.2857,'x_2': 0}, 
                              SimplexSolverADT().solveLP([[3,4],[7,4]],[24,16],[-2,3],[],'min')
                            )
    
    #Minimization with no optimum 
    def testMinNoOpt1(self):
        self.assertRaises(Exceptions.NO_OPTIMAL_SOLUTION, 
                              SimplexSolverADT().solveLP([[-1,-5],[-1,-4],[-1,-3],[-1,-2],[-1,-1]],[-6,-5,-4,-5,-6],[3,14],[],'min')
                            )
    
    #No objective function
    def testMissingObjcFunc(self):
        self.assertRaises(Exceptions.NO_OPTIMAL_SOLUTION, 
                              SimplexSolverADT().solveLP([[3,4],[7,4]],[24,16],[],[],'min')
                            )

    #No Linear Constraints
    def testMissingLC(self):
        self.assertRaises(Exceptions.NO_OPTIMAL_SOLUTION, 
                              SimplexSolverADT().solveLP([],[],[-2,3],[],'min')
                            )

    #****************** UNIT V&V TEST CASES ******************
    #Maximization with optimum 
    def testMaxOpt2(self):
        self.assertDictEqual({'Z': 1052000.0,'x_1': 4.0,'x_2': 10.0,'x_3': 14.0}, 
                              SimplexSolverADT().solveLP([[20,6,3],[0,1,0],[-1,-1,1],[-9,1,1]],[182,10,0,0],[100000,40000,18000],[],'max')
                            ) 
    
    #Maximization with optimum 
    def testMaxOpt3(self):
        self.assertDictEqual({'Z': 180,'x_1': 40.0,'x_2': 30.0}, 
                              SimplexSolverADT().solveLP([[3,2],[1,0],[0,1]],[180,40,60],[3,2],[],'max')
                            )

    #Minimization with no optimum 
    def testMinNoOpt2(self):
        self.assertRaises(Exceptions.NO_OPTIMAL_SOLUTION, 
                              SimplexSolverADT().solveLP([[400,300],[300,400],[200,500]],[25000,27000,30000],[11,16,15],[],'min')
                         )
    
if __name__ == "__main__":
    unittest.main()
