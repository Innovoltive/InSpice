#r# ================
#r#  CEM Simulation
#r# ================

#r# This example show a CEM simulation.

# Fixme: retrieve PDF reference and complete

####################################################################################################

import matplotlib.pyplot as plt

####################################################################################################

import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from InSpice.Doc.ExampleTools import find_libraries
from InSpice import SpiceLibrary, Circuit, Simulator, plot
from InSpice.Unit import *

####################################################################################################

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

####################################################################################################

from HP54501A import HP54501A

#f# literal_include('HP54501A.py')

####################################################################################################

circuit = Circuit('HP54501A CEM')
circuit.include(spice_library['1N4148'])
diode_model = '1N4148'
ac_line = circuit.AcLine('input', 'input', circuit.gnd, rms_voltage=230@u_V, frequency=50@u_Hz)
# circuit.subcircuit(HP54501A(diode_model='1N4148'))
# circuit.X('hp54501a', 'HP54501A', 'input', circuit.gnd)
circuit.C(1, 'input', circuit.gnd, 1@u_uF)
circuit.X('D1', diode_model, 'line_plus', 'top')
circuit.X('D2', diode_model, 'scope_ground', 'input')
circuit.X('D3', diode_model, circuit.gnd, 'top')
circuit.X('D4', diode_model, 'scope_ground', circuit.gnd)
circuit.R(1, 'top', 'output', 10@u_Ω)
circuit.C(2, 'output', 'scope_ground', 50@u_uF)
circuit.R(2, 'output', 'scope_ground', 900@u_Ω)

simulator = Simulator.factory()
simulation = simulator.simulation(circuit, temperature=25, nominal_temperature=25)
analysis = simulation.transient(step_time=ac_line.period/100, end_time=ac_line.period*3)

figure, ax = plt.subplots(figsize=(20, 6))

ax.plot(analysis.input)
ax.plot(analysis.Vinput)
ax.plot(analysis.output - analysis.scope_ground)
ax.legend(('Vin [V]', 'I [A]'), loc=(.8,.8))
ax.grid()
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')

plt.show()

#f# save_figure('figure', 'hp54501a-cem.png')
