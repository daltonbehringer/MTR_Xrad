import mtrxrad
import matplotlib.pyplot as plt
import glob


fdir = '/Users/daltonbehringer/MTR_data/xband/XSCZ/sv_tor_dec2024/2deg/'
fname = 'AQPI_outbound.scrz-20241214-214043_226773_21_2_PPI_qc.netcdf'
radvar = 'BV'

f = fdir + fname

for name in glob.glob(fdir + 'AQPI_outbound.scrz*'):
		mtrxrad.plot_ppi(name, radvar)
		plt.savefig(name + '_' + radvar + '.png', dpi=300, bbox_inches='tight')
		plt.close()