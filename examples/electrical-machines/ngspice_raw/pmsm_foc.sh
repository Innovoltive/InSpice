* this uses the pmsm.lib. test how to use the .lib file
.title PMSM model with sinusoidal back EMF
.include "../../spice-library/electrical-machines/clark_park.lib"
.include "../../spice-library/electrical-machines/pmsm.lib"
.include "../../spice-library/electrical-machines/foc.lib"
.include "../../spice-library/electrical-machines//average.lib"
.include "../../spice-library/semiconductors/operational-amplifier/generic_opamp.lib"

**input parameters
.param rs=3.4 
.param ls=12.1e-3 
.param poles=4
.param lambda_m=0.0827
.param J=5e-4
.param Bm=1e-9
.param vbus={30}

***************************Build the voltage sources***************************
vbus vbus 0 DC {vbus}
Xspvm qs_ref ds_ref theta as_ref bs_ref cs_ref vbus spvm_avg
*Xspvm qs_ref ds_ref theta as_ref bs_ref cs_ref vbus spvm
** Build the input voltage sources based on vqs_ref and vds_ref
* this will be the outside of the motor
Eas as as_n value={v(as_ref)}
Ebs bs bs_n value={v(bs_ref)}
Ecs cs cs_n value={v(cs_ref)}
Vas n as_n DC 0V
Vbs n bs_n DC 0V
Vcs n cs_n DC 0V
ran n 0 1e12
can n 0 1e-9

*********************** Adding PMSM model ************************************
* add the motor model
Xm as bs cs theta rpm tl pmsm
+rs={rs} ls={ls} 
+poles={poles} 
+lambda_m={lambda_m} 
+J={J} Bm={Bm}

**************** Apply the load ***************************
* A fan model
Etl tl 0 value={1e-6*v(rpm)*v(rpm)}

********************** Building the FOC controller ***************************
Eias iasm 0 value={i(vas)}
Eibs ibsm 0 value={i(vbs)}
Eics icsm 0 value={i(vcs)}

Xfoc iasm ibsm icsm rpm theta vbus qs_ref ds_ref controller rpm_ref=500

.control
tran 0.1ms 1s 0s uic
*plot qs_ref ds_ref
plot v(as) v(bs) v(cs)
*plot i(vas) i(vbs) i(vcs)
*plot v(as) i(vas)
plot v(rpm)
.endc


