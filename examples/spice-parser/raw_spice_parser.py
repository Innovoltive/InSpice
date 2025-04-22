
import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from InSpice import Circuit, SubCircuit, SubCircuitFactory
from InSpice.Spice.Parser.HighLevelParser import SpiceSource
from InSpice.Spice.Parser import Translator
from InSpice.Unit import *

raw_spice = '''


EGND 99 0 4 5 1
ENONLIN 100 101 POLY(2) 3 0 4 0 0.0 13.6 0.2 0.005
EAND out1 out0 and(2) in1 0 in2 0 (0.5, 0) (2.8, 3.3)
EGND1 99 0 POLY(2) (3,0) (4,0) 0 .5 .5
ECMP 11 0 TABLE {V(10,9)} = (-5mV, 0V) (5mV, 5V)
E41 4 0 value = {V(3)*V(3)-Offs}
E411 4 0 vol = ’V(3)*V(3)-Offs’

'''

'''
issue with the following lines
ELOPASS 4 0 LAPLACE {V(1)} {5 * (s/100 + 1) / (s^2/42000 + s/60 + 1)} {V(20,21)}= DB (1.000000e+07Hz, 1.633257e-07, -1.859873e+01)

'''


''' Below lines are okay
EGND 99 0 4 5 1
ENONLIN 100 101 POLY(2) 3 0 4 0 0.0 13.6 0.2 0.005
EAND out1 out0 and(2) in1 0 in2 0 (0.5, 0) (2.8, 3.3)
EGND1 99 0 POLY(2) (3,0) (4,0) 0 .5 .5
ECMP 11 0 TABLE {V(10,9)} = (-5mV, 0V) (5mV, 5V)
E41 4 0 value = {V(3)*V(3)-Offs}
E4111 4 0 vol = ’V(3)*V(3)-Offs’


'''


source = raw_spice

spice_source = SpiceSource(source=source, title_line=False)
for obj in spice_source.obj_lines:
    print(obj)
bootstrap_circuit = Translator.Builder().translate(spice_source)
bootstrap_source = str(bootstrap_circuit)
print(bootstrap_source)
# assert bootstrap_source == source

# circuit = Circuit('Test')
# circuit.NonLinearVoltageSource(1, 'output', circuit.gnd,
#                                expression='V(reference, comparator)',
#                                table=((-micro(1), 0),
#                                       (micro(1), 10))
#                                )
# circuit.NonLinearVoltageSource(2, '99', '0', raw_spice='POLY(2) (3,0) (4,0) 0 .5 .5')

# # assert bootstrap_source == source
# print(circuit)