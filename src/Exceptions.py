# @file Exceptions.py
# @author Hanane Zlitni
# @brief This module contains all the exceptions that the library throws.
# @date Dec 17, 2018

#Base class for exceptions in this module
class Error(Exception):
    pass

#MISSING_INPUT is raised when at least one input is missing
class MISSING_INPUT(Error):
   pass

#NO_OPTIMAL_SOLUTION is raised when the linear program does not have an optimum
class NO_OPTIMAL_SOLUTION(Error):
   pass