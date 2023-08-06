#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
import os
try:
    from MESA2HYDRO.lib import MESAhandling as MJ
    from MESA2HYDRO.lib import converge_funcs as cf
except ImportError:
    MESA_PKG_DIR = os.path.abspath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
    sys.path.insert(0, os.path.join(MESA_PKG_DIR, 'lib'))
    import MESAhandling as MJ
    import converge_funcs as cf
###################################################
M_to_solar=1.988*10.0**33.0 ## g/Msolar
R_to_solar=6.957*10.0**10.0 ## cm/Rsolar
###################################################


subprocess.call('ls ../data/sample_MESA_output/profile*', shell=True)
ftag=str(raw_input('enter MESA identifier "profile_..." (ex: "redgiant"): '))
MESA_file='../data/sample_MESA_output/profile_'+ftag+'.data'
logdata=str(raw_input('log? (y for yes): '))
try:
	mc=float(raw_input('depth of penetration from surface? (default 5%): '))
	masscut=(100.0-mc)/100.0
except ValueError:
	masscut=0.95
sf=str(raw_input('save? (y for yes): '))

if sf=='y':
	savefig=True
else:
	savefig=False

print("masscut: ", masscut)

if logdata=='y':
	unlogg_data=False
else:
	unlogg_data=True

tag=ftag


try:
	fit_region_R = cf.get_MESA_profile_edge(MESA_file, quantity='logR', masscut=masscut,strip=False)
	fit_region_rho = cf.get_MESA_profile_edge(MESA_file, quantity='logRho', masscut=masscut ,strip=False)

	if unlogg_data:
		fit_region_R=cf.unlog(fit_region_R)*R_to_solar
		fit_region_rho=cf.unlog(fit_region_rho)

	plt.plot(fit_region_R, fit_region_rho,'m-', label=tag)
	if unlogg_data:
		plt.xlabel('R (cm)')
		plt.ylabel('Rho (g/cm$^3$)')
	else:
		plt.xlabel('logR (R/Rsolar)')
		plt.ylabel('logRho (g/cm$^3$)')
	plt.title('data from profile_'+ftag+' at '+str((1.0-masscut)*100.0)+r'% surface depth')
	plt.legend(loc=1)
	if savefig:
		plt.savefig(tag+'_density_profile_'+str(masscut)+'.png')
	plt.show()
	plt.close()
except IOError:
	print('file ../out/sample_MESA_output/profile_'+ftag+'.data not found\n')
	print('available files: ')
	subprocess.call('ls ../out/sample_MESA_output/profile*', shell=True)
