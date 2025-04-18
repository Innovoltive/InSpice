
import InSpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from InSpice import Circuit, SubCircuit, SubCircuitFactory
from InSpice.Spice.Parser.HighLevelParser import SpiceSource
from InSpice.Spice.Parser import Translator
from InSpice.Unit import *
'''
EGND1 99 0 POLY(2) (3,0) (4,0) 0 .5 .5
EGND 99 0 4 5 1
ENONLIN 100 101 POLY(2) 3 0 4 0 0.0 13.6 0.2 0.005
'''
raw_spice = '''
ECMP 11 0 TABLE {V(10,9)} = (-5mV, 0V) (5mV, 5V)

'''
'''
E41 4 0 value = {V(3)*V(3)-Offs}
E41 4 0 vol = ’V(3)*V(3)-Offs’
ELOPASS 4 0 LAPLACE {V(1)} {5 * (s/100 + 1) / (s^2/42000 + s/60 + 1)} {V(20,21)}= DB (1.000000e+07Hz, 1.633257e-07, -1.859873e+01)
EAND out1 out0 and(2) in1 0 in2 0 (0.5, 0) (2.8, 3.3)
'''

raw_spice = '''
*.tile Qucs 25.1.1  ...
.INCLUDE "/usr/share/qucs-s/xspice_cmlib/include/ngspice_mathfunc.inc"

.SUBCKT SpiceOpamp_LM358 	gnd 1 2 3 4 5
*
C1   11 12 5.544E-12
C2    6  7 20.00E-12
DC    5 53 DX
DE   54  5 DX
DLP  90 91 DX
DLN  92 90 DX
DP    4  3 DX
EGND 99  0 POLY(2) (3,0) (4,0) 0 .5 .5
FB    7 99 POLY(5) VB VC VE VLP VLN 0 15.91E6 -20E6 20E6 20E6 -20E6
GA    6  0 11 12 125.7E-6
GCM   0  6 10 99 7.067E-9
IEE   3 10 DC 10.04E-6
HLIM 90  0 VLIM 1K
Q1   11  2 13 QX
Q2   12  1 14 QX
R2    6  9 100.0E3
RC1   4 11 7.957E3
RC2   4 12 7.957E3
RE1  13 10 2.773E3
RE2  14 10 2.773E3
REE  10 99 19.92E6
RO1   8  5 50
RO2   7 99 50
RP    3  4 30.31E3
VB    9  0 DC 0
VC 3 53 DC 2.100
VE   54  4 DC .6
VLIM  7  8 DC 0
VLP  91  0 DC 40
VLN   0 92 DC 40
.MODEL DX D(IS=800.0E-18)
.MODEL QX PNP(IS=800.0E-18 BF=250)
.ENDS
  
.SUBCKT Power_amp_arduino_subscheme Vout gnd Vin VCC 
QX2N2222A_1 VCC Vopamp Vout QMOD_X2N2222A_1 AREA=1
.MODEL QMOD_X2N2222A_1 npn (Is=14.34F Nf=1 Nr=1 Ikf=0.2847 Ikr=0 Vaf=74.03 Var=0 Ise=14.34F Ne=1.307 Isc=0 Nc=2 Bf=255.9 Br=6.092 Rbm=0 Irb=0 Rc=1 Re=0 Rb=10 Cje=22.01P Vje=0.75 Mje=0.377 Cjc=7.306P Vjc=0.75 Mjc=0.3416 Xcjc=1 Cjs=0 Vjs=0.75 Mjs=0 Fc=0.5 Tf=411.1P Xtf=3 Vtf=0 Itf=0.6 Tr=46.91N Kf=0 Af=1 Ptf=0 Xtb=1.5 Xti=3 Eg=1.11 Tnom=26.85 )
RG 0 _net2  100K
XOP1 0  Vin _net2 VCC 0 Vopamp SpiceOpamp_LM358
Rf _net2 Vout  1K 
RG1 Vin 0  100K
.ENDS
Rsh Vin _net0  1K
V2 VCC 0 DC 8
V4 Vin 0 DC 2
XSUB1 _net4 0 _net0 VCC Power_amp_arduino_subscheme
QX2N2222A_1 _net5 Vbase 0 QMOD_X2N2222A_1 AREA=1
.MODEL QMOD_X2N2222A_1 npn (Is=14.34F Nf=1 Nr=1 Ikf=0.2847 Ikr=0 Vaf=74.03 Var=0 Ise=14.34F Ne=1.307 Isc=0 Nc=2 Bf=255.9 Br=6.092 Rbm=0 Irb=0 Rc=1 Re=0 Rb=10 Cje=22.01P Vje=0.75 Mje=0.377 Cjc=7.306P Vjc=0.75 Mjc=0.3416 Xcjc=1 Cjs=0 Vjs=0.75 Mjs=0 Fc=0.5 Tf=411.1P Xtf=3 Vtf=0 Itf=0.6 Tr=46.91N Kf=0 Af=1 Ptf=0 Xtb=1.5 Xti=3 Eg=1.11 Tnom=26.85 )
VIb _net4 OutV DC 0
Rsh2 Vbase OutV  1K

'''
source = raw_spice

spice_source = SpiceSource(source=source, title_line=False)
for obj in spice_source.obj_lines:
    print(obj)
bootstrap_circuit = Translator.Builder().translate(spice_source)
bootstrap_source = str(bootstrap_circuit)
print(bootstrap_source)
# assert bootstrap_source == source

circuit = Circuit('Test')
circuit.NonLinearVoltageSource(1, 'output', circuit.gnd,
                               expression='V(reference, comparator)',
                               table=((-micro(1), 0),
                                      (micro(1), 10))
                               )
circuit.NonLinearVoltageSource(2, '99', '0', raw_spice='POLY(2) (3,0) (4,0) 0 .5 .5')

# assert bootstrap_source == source
print(circuit)