'''This example shows how to use a single ended to differential amplifier to sense a high voltage
and convert it to a low voltage. The circuit is based on the ADA4940 operational amplifier.
You can see how using AD8137 causes instability in the circuit. The circuit is a simple
'''
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
circuit.include(spice_library['ADA4940'])
circuit.include(spice_library['genopadiff'])
circuit.include(spice_library['LMH6551'])
circuit.include(spice_library['ad8137'])

gain = 80e3/10e6
rh_val = 10e3@u_kΩ
vdd_voltage = 5 
input_offset = 270@u_V
input_amplitude = 1@u_V

circuit.V('V+', 'V+', circuit.gnd, dc_value=vdd_voltage@u_V)
circuit.V('V-', 'V-', circuit.gnd, dc_value=0@u_V)
# place a 0.1uF capacitor from V+ to ground
circuit.C('V+', 'V+', circuit.gnd, 0.1@u_uF)


circuit.SinusoidalVoltageSource('inputh', 'inh', circuit.gnd, offset = input_offset, amplitude=input_amplitude, frequency=1@u_kHz)
circuit.V('inputl', 'inl', circuit.gnd, dc_value=0@u_V)

# ic = 'ad8137'
ic = 'genopadiff'
# ic = 'ada4940'
# ic = 'LMH6551'
if ic == 'ad8137':
    circuit.X('op', 'ad8137', 'in+', 'in-', 'V+', 'V-', 'out+', 'out-', 'Vcm')
elif ic == 'genopadiff':
    circuit.X('op', 'genopadiff', 'in+', 'in-', 'V+', 'V-', 'out+', 'out-', 'Vcm')

elif ic == 'ada4940':
    circuit.X('op', 'ADA4940', 'FB-', 'FB+', 'in+', 'in-', 'V+', 'V-','out+', 'out-', 'Vcm')
elif ic == 'LMH6551':
    # Note that the LMH6551 needs a Vcm voltage to work properly. This is the common mode voltage.
    circuit.X('op', 'LMH6551', 'in+', 'in-', 'V+', 'V-', 'Vcm', 'out+', 'out-')
    circuit.V('Vcm', 'Vcm', circuit.gnd, dc_value=vdd_voltage@u_V)
else:
    raise ValueError('Unknown IC: {}'.format(ic))

circuit.R('inph', 'inh',   'in+', rh_val)
circuit.R('innh', 'inl',   'in-', rh_val)

circuit.R('innl', 'in+', 'out-', gain*rh_val)
circuit.R('inpl', 'in-', 'out+', gain*rh_val)

# put a 56 omhm in series with each output of th opamp
circuit.R('out+', 'out+', 'outp', 56@u_Ω)
circuit.R('out-', 'out-', 'outn', 56@u_Ω)
# place 39pf from outp and outn to ground
# circuit.C('outp', 'outp', circuit.gnd, 390@u_pF)
# circuit.C('outn', 'outn', circuit.gnd, 390@u_pF)

circuit.R('load', 'outp', 'outn', 470@u_Ω)
# place a 0.22uF capacitor from Vcm to ground
circuit.C('Vcm', 'Vcm', circuit.gnd, 0.22@u_uF)



simulator = Simulator.factory()
simulation = simulator.simulation(circuit, temperature=25, nominal_temperature=25)
simulation.options(rshunt=1e12)
simulation.options(max_step=1e-6)
analysis = simulation.transient(step_time=1e-6, end_time=10e-3, start_time=0@u_ms, max_time=1@u_us, use_initial_condition=False)

figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

plt.title("output Operational Amplifier")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
ax1.plot(analysis.time, analysis['inh'], label='input voltage')

# add legend
ax1.legend()
ax2.plot(analysis.time, analysis['outp']-analysis['outn'], label='differential output')

ax2.legend()

plt.tight_layout()
plt.show()

#f# save_figure('figure', 'operational-amplifier.png')
