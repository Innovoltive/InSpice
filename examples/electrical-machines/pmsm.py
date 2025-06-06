####################################################################################################

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

libraries_path = find_libraries()
spice_library = SpiceLibrary(libraries_path)


####################################################################################################
circuit = Circuit("PMSM Example")
circuit.include(spice_library['pmsm'])  # Include the PMSM library
circuit.include(spice_library['clark'])  # Include the PMSM library
circuit.include(spice_library['iclark'])  # Include the PMSM library
circuit.include(spice_library['park'])  # Include the PMSM load library

#TODO: show how to ramp the input voltage
# circuit.V('qs_ref', 'qs_ref', circuit.gnd, 11.2*math.sqrt(2)@u_V)  # Reference voltage for q-axis
circuit.V('qs_ref', 'qs_ref', circuit.gnd, raw_spice='PWL(0 0 100m {11.2*sqrt(2)})')
circuit.V('ds_ref', 'ds_ref', circuit.gnd, 0@u_V)  # Reference voltage for d-axis
# Xpark   qs_ref ds_ref theta alpha_ref beta_ref park
circuit.X('park', 'park', 'qs_ref', 'ds_ref', 'theta', 'alpha_ref', 'beta_ref')
# Xiclark alpha_ref beta_ref asd bsd csd iclark
circuit.X('iclark', 'iclark', 'alpha_ref', 'beta_ref', 'asd', 'bsd', 'csd')

neutral = 'n'
circuit.NonLinearVoltageSource('as', 'phase_a', neutral, raw_spice='value={v(asd)}')  
circuit.NonLinearVoltageSource('bs', 'phase_b', neutral, raw_spice='value={v(bsd)}')  
circuit.NonLinearVoltageSource('cs', 'phase_c', neutral, raw_spice='value={v(csd)}')  
circuit.R('n', neutral, circuit.gnd, 1@u_GOhm)  # Neutral resistor to ground
circuit.C('n', neutral, circuit.gnd, 1@u_nF)  # Neutral capacitor to ground
# Behavioral voltage source for mechanical angle and speed
# Three-phase voltage sources with proper phase relationships
# #TODO: implement phase in the voltage source. we make cosine to match my course. we add an offset to the delay to match the cosine wave
# vas=circuit.SinusoidalVoltageSource('vas', 'phase_a', circuit.gnd, amplitude=AMPLITUDE, frequency=FLINE, delay=-5*TLINE/4)
# vbs=circuit.SinusoidalVoltageSource('vbs', 'phase_b', circuit.gnd, amplitude=AMPLITUDE, frequency=FLINE, delay=   TLINE/3 - 5*TLINE/4)
# vcs=circuit.SinusoidalVoltageSource('vcs', 'phase_c', circuit.gnd, amplitude=AMPLITUDE, frequency=FLINE, delay= 2*TLINE/3 - 5*TLINE/4)

circuit.V('as', 'phase_a', 'pha', 0) # to measure current in phase and model cable resistance
circuit.V('bs', 'phase_b', 'phb', 0) # to measure current in phase and model cable resistance
circuit.V('cs', 'phase_c', 'phc', 0) # to measure current in phase and model cable resistance

# Add PMSM subcircuit                        
#+rs=3.4 ls=12.1e-3 poles=4 
# +lambda_m=0.0827 Tl=0 J=5e-4 Bm=1e-9
circuit.X('M', 'pmsm', 'pha', 'phb', 'phc', 'theta', 'rpm', 'tl',
        rs=0.1,
        ls=1e-3,
        poles=2,
        lambda_m=0.0827,
        J=5e-3,
        Bm=1e-9)
circuit.V('tl', 'tl', circuit.gnd, 0.4)  # Load torque voltage source
# Add load resistors to complete the circuit and prevent floating nodes


simulator = Simulator.factory()
simulation = simulator.simulation(circuit)
# simulation.options('RSHUNT = 1e12') # helps with convergence in some cases
simulation.options('SAVECURRENTS') # save all the currents in the simulation
# simulation.options('NOINIT')
# simulation.options('KLU')
# simulation.options('ABSTOL=1e-10')  # Absolute tolerance for convergence
# simulation.options('RELTOL=0.01')  # Relative tolerance for convergence
analysis = simulation.transient(step_time=0.1@u_ms, end_time=2@u_s)


##################################################### Plotting #####################################################
figure1, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

ax1.set_title('Three-Phase PMSM Voltage Sources')
ax1.set_ylabel('Voltage [V]')
ax1.grid()
ax1.plot(analysis['phase_a'], label='Phase A')
ax1.plot(analysis['phase_b'], label='Phase B')
ax1.plot(analysis['phase_c'], label='Phase C')
ax1.legend()

ax2.set_title('Three-Phase PMSM Currents')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Current [A]')
ax2.grid()
ax2.plot(analysis.branches['vas'], label='Current Phase A')
ax2.plot(analysis.branches['vbs'], label='Current Phase B')
ax2.plot(analysis.branches['vcs'], label='Current Phase C')
ax2.legend()

ax3.set_title('PMSM Mechanical Parameters')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Mechanical Parameters')
ax3.grid()
# ax3.plot(analysis['xm.alpha'], label='valpha', color='C0')
# ax3.plot(analysis['xm.beta'], label='vbeta', color='C1')
# ax3.plot(analysis['xm.qs'], label='vqs', color='C0')
# ax3.plot(analysis['xm.ds'], label='vds', color='C1')
# ax3.plot(analysis['xm.wm'], label='Mechanical Angular Velocity [rad/s]', color='C0')
# ax3.plot(analysis['xm.we'], label='Electrical Angular Velocity [rad/s]', color='C1')
ax3.plot(analysis['rpm'], label='Speed [RPM]', color='C0')
# ax3.plot(analysis['xm.theta'], label='Mechanical Angle [rad]', color='C0')
# ax3.plot(analysis['xm.theta2'], label='Electrical Angle [rad]', color='C1')
ax3.legend()

ax4.set_title('PMSM Electrical Parameters')
ax4.set_xlabel('Time [s]')
ax4.set_ylabel('Electrical Parameters')
ax4.grid()
# ax4.plot(analysis['xm.q3'], label='back EMF q-axis [V]', color='C0')
# ax4.plot(analysis['xm.iqs'], label='iqs current [A]', color='C1')
# ax4.plot(analysis['xm.ids'], label='ids current [A]', color='C2')
ax4.plot(analysis['xm.te'], label='Torque [Nm]', color='C0')
ax4.plot(analysis['tl'], label='Load Torque [Nm]', color='C1')
ax4.legend()
plt.tight_layout()
plt.show()

