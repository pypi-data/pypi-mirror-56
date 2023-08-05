import matplotlib.pyplot as plt
import ecalic.ic
import urllib2

### input file
www = 'https://ecaldpg.web.cern.ch/ecaldpg/users/fcouderc/examples/ecalic/'
inputtxt = urllib2.urlopen(www + '/ic_example.txt')
with open( 'ic.test.txt','w') as ftest: ftest.write( inputtxt.read())
ftest.close()

### create an instance of ecalic.ic
i =  ecalic.ic.icCMS( 'ic.test.txt' , 'example IC' )

### help for each method
#?i.etaRingNorm(

### normalize to 1 per eta ring
i.etaRingNorm()

### plot 2D
i.plot( zRange_eb = [0.98,1.02], zRange_ee = [0.95,1.05], title = 'IC test'  )

### average per harness and plot,
### remove 10% of the most tailish cristals (left and right from mean)

# add a variable with the average
# trim = remove 10% of the most tailish cristals (left and right from mean)
i['ic_av'] = i.average( groupby='harness', trim = 0.10 )
# plot the average
i.plot( var = 'ic_av', zRange_eb = [0.98,1.02], zRange_ee = [0.95,1.05], title = 'IC test average'  )
plt.show()
