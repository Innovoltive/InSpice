* this uses the pmsm.lib. test how to use the .lib file
.title PMSM model with sinusoidal back EMF
.include "../spice-library/electrical-machines/clark_park.lib"
.include "../spice-library/electrical-machines/pmsm.lib"

**input parameters
.param rs=3.4 
.param ls=12.1e-3 
.param poles=4
.param lambda_m=0.0827
.param Tl=0.4
.param J=5e-4
.param Bm=1e-9


** Build the input voltage sources based on vqs_ref and vds_ref
* this will be the outside of the motor
vqs_ref qs_ref 0 DC 0V PWL(0s 0V 1ms {11.25*sqrt(2)})
vds_ref ds_ref 0 0
Xpark   qs_ref ds_ref theta alpha_ref beta_ref park
* use reverse park transformation to get the reference voltages
Xiclark alpha_ref beta_ref asd bsd csd iclark
Eas as as_n value={v(asd)}
Ebs bs bs_n value={v(bsd)}
Ecs cs cs_n value={v(csd)}
Vas n as_n DC 0V
Vbs n bs_n DC 0V
Vcs n cs_n DC 0V
ran n 0 1e12
Xm as bs cs theta rpm pmsm rs={rs} ls={ls} 
+poles={poles} lambda_m={lambda_m} Tl={Tl} J={J} Bm={Bm}

.control
*options rshunt=1e12
*options noinit
*options klu
tran 0.1ms 2s
plot qs_ref ds_ref
plot v(as) v(bs) v(cs)
plot i(vas) i(vbs) i(vcs)
plot v(rpm)
.endc

