# @file Output.py
# @author Hanane Zlitni
# @brief This module handles entering the inputs using the command line to test the library 
# @date Dec 17, 2018

import ast, getopt, sys, copy, os
import Exceptions
# @file Driver.py
# @author Hanane Zlitni
# @brief This file contains the implementation of a command line client that uses LoSMS
# @date Dec 17, 2018

import SimplexSolverADT
import time

# *************** Clear console (cross-platform) ***************
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Driver():
    if __name__ == '__main__':
        clear()
        start = time.time()

        #Command line handling
        lc = []
        const = []
        ob = []
        t = []
        g = ''
        argv = sys.argv[1:]  

        print("Enter a b c")  

        try:
            opts, args = getopt.getopt(argv,"hlc:const:ob:g:",["lc=","const=","ob=","g="])
            
            for opt, arg in opts:
                #Print 'help' information
                if opt == '-h':
                    print('Output.py -lc <matrix> -const <vector> -ob <vector> -g <LP_goal>')
                    print('lc: Matrix representing the coefficients of the linear constraints.')
                    print('const: The constants (Ax <= const)')
                    print('ob: The coefficients of the objective function.')
                    print('g: The goal of the linear program (max or min)')
                    sys.exit()
                else:
                    #If one of the inputs is completely missing from the arguments list, raise exception
                    if ('-lc') not in argv or ('-const') not in argv or ('-ob') not in argv or ('-g') not in argv:
                        raise Exceptions.MISSING_INPUT
                    '''
                    else:
                        #If the arguments are present but their contents are empty, raise exception
                        if (argv[1] == "[]" or argv[3] == "[]" or argv[5] == "[]" or argv[7] == ""):
                            raise Exceptions.MISSING_INPUT
                    '''
                    #Otherwise, assign inputs to variables and pass them to SimplexSolverADT
                    if sys.argv[1] == ("-lc"):
                        lc = ast.literal_eval(sys.argv[2])
                    if sys.argv[3] == ("-const"):
                        const = ast.literal_eval(sys.argv[4])
                    if sys.argv[5] == ("-ob"):
                        ob = ast.literal_eval(sys.argv[6])
                    if sys.argv[7] in ("-g"):
                        g = sys.argv[8].strip()
                
        except Exceptions.MISSING_INPUT:
            print('MISSING_INPUT: At least one input is missing. Type the following for more info --> Output.py -h')
            sys.exit()

        except getopt.GetoptError:
            print('The input should be in the following form --> Output.py -lc <matrix> -const <vector> -ob <vector> -g <type>')
            sys.exit(2)

        #Assuming 'max' is the default linear program goal
        if g not in ('max', 'min'):
            g = 'max'

        #Pass inputs to SimplexSolverADT
        SimplexSolverADT.SimplexSolverADT().solveLP(lc,const,ob,goal=g)
        
        end = time.time()
        print(end - start)