import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import ecalic.ic as ic, ecalic.iov as iov
import ecalic.cmsStyle as cms
import urllib2

### input files
www = 'https://ecaldpg.web.cern.ch/ecaldpg/users/fcouderc/examples/ecalic/'
pedestal1 =  urllib2.urlopen(www + '/pedestals_hlt_run324773.xml' )
pedestal2 =  urllib2.urlopen(www + '/pedestals_hlt_run315840.xml' )
status    =  urllib2.urlopen(www + '/status_run324773.xml'        )

### Make the ICs from the input files
print('Downloading input files from web... keep cool')
noise1 = ic.icCMS( iov.xml( pedestal1, type = 'noise12' ), 'noise (x12) run 324773' )
noise2 = ic.icCMS( iov.xml( pedestal2, type = 'noise12' ), 'noise (x12) run 315840' )
status = ic.icCMS( iov.xml( status   , type = 'status'  ), 'status run 324773' )

### mask bad channels (i.e. status != 0)
noise1['ic'].mask( status['ic'] != 0 , inplace=True )
noise2['ic'].mask( status['ic'] != 0 , inplace=True )

### plot the 2D noise map
noise1.plot( zRange_eb = [1,3], zRange_ee = [1,3], title = 'noise run 324773' )
noise2.plot( zRange_eb = [1,3], zRange_ee = [1,3], title = 'noise run 315840' )

### profile along eta
plt.figure( 'Noise profile', figsize = [8,4] )
axis = plt.gca()
noise1.profile1D( axis = axis, legend = 'noise 1' )
noise2.profile1D( axis = axis, legend = 'noise 2' )

### poslihing plot (not mandatory)
cms.polishPlot(axis, xTitle = 'Crystal $i\eta$', yTitle = 'Pedestal RMS (ADC)', \
                xRange = [-130,130], yRange = [0,3], \
                year = 2018, legTitle = 'ECAL Noise', legLoc = 8)
cms.ecalModuleBoundaries(axis)

### noises ratio, correlation ...
plt.figure( 'Noise ratio', figsize = [8,4] )
ratio = noise1 / noise2

### get the correlation in a group of crystal defined by grby
### (example: grby ieta band of 5 crystals)
grby = np.sign(ic.geom['ieta']) * ((np.abs(ic.geom['ieta'])-1)//5)
ratio['cov'],ratio['cor'] = ic.icCovCor(noise1,noise2,groupby=grby)

### plot the projection of the correlation along ieta
ratio.profile1D(yvar = 'cor',axis = plt.gca(), title = 'correlation')

### plot polishing
cms.polishPlot(plt.gca(), xTitle = 'Crystal $i\eta$', yTitle = 'Noise correlation',
                xRange = [-130,130], yRange = [0,1], year = 2018 )
cms.ecalModuleBoundaries(plt.gca())
plt.gca().grid( axis = 'y', linestyle='--', linewidth=0.9, which = 'both')

### visualize with pyplot
plt.show()
