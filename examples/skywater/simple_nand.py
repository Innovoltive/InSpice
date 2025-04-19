from InSpice.Doc.ExampleTools import find_libraries
from InSpice.Probe.Plot import plot
from InSpice.Spice.Library import SpiceLibrary
from InSpice.Spice.Netlist import Circuit
from InSpice.Unit import *

# libraries_path = "/home/asepahvand/repos/skywater-pdk/libraries/sky130_fd_pr/latest/models/sky130.lib.spice"
libraries_path = "/home/asepahvand/repos/spice_libraries/generic_format.lib"

# spice_library = SpiceLibrary(libraries_path)

####################################################################################################

#?# circuit_macros('buck-converter.m4')
# libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path,recurse=True, section="tt")

####################################################################################################

#?# circuit_macros('buck-converter.m4')

circuit = Circuit('Buck Converter')
circuit.include(spice_library['generic_comp'])

print(circuit)