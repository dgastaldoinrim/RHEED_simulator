import traceback
import sys

class Errors(Exception):
    """
    This class, that inherits Exception in order to become an error handling class, is only a container for the errors that can be raised in MRLab classes.
    """
    pass

    def warning_handler(self):
        """
        This function is used to properly handle an ERROR exception, printing all the informations necessary to the users (including the eventual PyVISA
        internal error number and message). After having done this, it prints also the error traceback and stops script execution calling sys.exit() method.
        """
        print(self.code)
        print(self.name)
        print(self.message)
        traceback.print_tb(sys.exc_info()[2])

    def error_handler(self):
        """
        This function is used to properly handle an ERROR exception, printing all the informations necessary to the users (including the eventual PyVISA
        internal error number and message). After having done this, it prints also the error traceback and stops script execution calling sys.exit() method.
        """
        self.warning_handler()
        sys.exit()

class LatticeErrors(Errors):
    """
    This class, that inherits Errors in order to become an error handling class, is only a container for the errors that can be raised in Crystalline and Bravais class.
    """
    pass

class WrongLatticeSimmetry(LatticeErrors):
    """
    """
    def __init__(self, crystal_system):
        self.code = 'LATTICEERROR1'
        self.name = 'WRONG_SPACE_GROUP_SPECIFIED'
        self.message = 'ERROR: The given space group ("{0}") is not a Bravais space group.\nPlease check that you have inserted the right crystalline simmetry system for your lattice.\nExecution aborted.'.format(crystal_system)

class WrongParametersNumber(LatticeErrors):
    """
    """
    def __init__(self, given, required):
        self.code = 'LATTICEERROR2'
        self.name = 'WRONG_NUMBER_OF_PARAMETERS_INSERTED'
        self.message = 'ERROR: Please check that you have inserted the right parameters number for the selected lattice.\nYou give {0} parameters, while {1} parameters were required.\nExecution aborted.'.format(given, required)