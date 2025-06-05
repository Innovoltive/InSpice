
import math
import matplotlib.pyplot as plt

####################################################################################################

import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from InSpice.Doc.ExampleTools import find_libraries
from InSpice import SpiceLibrary, Circuit, Simulator, plot
from InSpice.Unit import *
####################################################################################################

libraries_path = "examples/spice-library/TLC555.LIB"
spice_library = SpiceLibrary(libraries_path)


####################################################################################################
circuit = Circuit("PMSM Example")