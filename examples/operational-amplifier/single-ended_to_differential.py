####################################################################################################

import numpy as np

import matplotlib.pyplot as plt

####################################################################################################

import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################
from InSpice.Doc.ExampleTools import find_libraries
from InSpice.Plot.BodeDiagram import bode_diagram
from InSpice import SpiceLibrary, Circuit, Simulator, plot
from InSpice.Unit import *

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)

#f# literal_include('OperationalAmplifier.py')

####################################################################################################

circuit = Circuit('Operational Amplifier')
circuit.include(spice_library['LMH6551'])
gain = 1/2
rh_val = 10@u_kΩ
# AC 1 PWL(0US 0V  0.01US 1V)
circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, offset = 0@u_V, amplitude=1@u_V, frequency=100@u_kHz)
circuit.V('Vcm', 'Vcm', circuit.gnd, dc_value=0@u_V)
circuit.V('V+', 'V+', circuit.gnd, dc_value=5@u_V)
circuit.V('V-', 'V-', circuit.gnd, dc_value=-5@u_V)

circuit.X('op', 'LMH6551', 'in+', 'in-', 'V+', 'V-', 'Vcm', 'out+', 'out-')
circuit.R('inph', 'in',          'in+', rh_val)
circuit.R('innh', circuit.gnd,   'in-', rh_val)

circuit.R('innl', 'in+', 'out-', gain*rh_val)
circuit.R('inpl', 'in-', 'out+', gain*rh_val)

circuit.R('load', 'out+', 'out-', 470@u_Ω)


simulator = Simulator.factory()
simulation = simulator.simulation(circuit, temperature=25, nominal_temperature=25)
analysis = simulation.transient(step_time=1e-6, end_time=20e-6, start_time=0@u_ms, max_time=1@u_ns, use_initial_condition=True)

figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

plt.title("output Operational Amplifier")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
ax1.plot(analysis.time, analysis['in'], label='input voltage')
ax1.plot(analysis.time, analysis['out+']-analysis['out-'], label='differential output')

# add legend
ax1.legend()

ax2.plot(analysis.time, analysis['in+'], label='opamp in+')
ax2.plot(analysis.time, analysis['in-'], label='opamp in-')
ax2.plot(analysis.time, analysis['out+'], label='opamp out+')
ax2.plot(analysis.time, analysis['out-'], label='opamp out-')
# add legend
ax2.legend()

plt.tight_layout()
plt.show()

#f# save_figure('figure', 'operational-amplifier.png')
