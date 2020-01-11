import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

file = "./co/S5P_OFFL_L2__CO_____20191202T070058_20191202T084228_11065_01_010302_20191208T062144.nc"
nc = Dataset(file, "r")

lons = nc.groups["PRODUCT"].variables['longitude'][:][0,:,:]
lats = nc.groups["PRODUCT"].variables['latitude'][:][0,:,:]
meth_conc = nc.groups["PRODUCT"].variables['carbonmonoxide_total_column_precision'][:]
meth_unit = nc.groups["PRODUCT"].variables['carbonmonoxide_total_column_precision'].units

lons_0 = lons.mean()
lats_0 = lats.mean()

fig = plt.figure(figsize=(10, 10))
m = Basemap(projection='lcc', resolution='h', llcrnrlat=8.4, urcrnrlat=37.6, llcrnrlon=68.7, urcrnrlon=97.25, lon_0=lons_0, lat_0=lats_0)
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')

# all_conc = []
# for i in range(len(lats)):
# 	print(i)
# 	for j in range(len(lats[0])):
# 		if (meth_conc[0][i][j] is np.ma.core.MaskedConstant()) == False:
# 			all_conc.append((lats[i][j], lons[i][j], meth_conc[0][i][j]))

# all_conc = sorted(all_conc, reverse=True, key=lambda x: x[2] if (x[0]>=8.4 and x[0]<=37.6 and x[1]>=68.7 and x[1]<=97.25 == True) else 0)[:100000]
# for coord in all_conc:
# 	 if m.is_land(coord[0], coord[1]) == True:
# 	 	print(coord)

xi, yi = m(lons, lats)
cs = m.pcolor(xi,yi,np.squeeze(meth_conc),norm=LogNorm(), cmap='viridis')
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(meth_unit)

plt.title(r'$C0$ in atmosphere taken at '+nc.groups['METADATA'].groups['GRANULE_DESCRIPTION'].GranuleStart)
plt.savefig('foo.png')
