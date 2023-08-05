class GND:
    """
    Example:
    FILES = ['direct.fits','grism1.fits','grism2.fits'] # Further on, only the index 0,1,2 will be used for referring the files
    X = GND(FILES) 
    X.files >>> FILES
    X.make_meta() # X.meta, or X.show_meta() >>> show information from headers
    X.meta >>> show meta info, unformatted
    X.show_meta() >>> show meta info, formatted and sorted
    
    pair = {0: [1,2]} # pair info {direct: [grism1,grism2]}, use X.show_meta() for helping you identify good pairs with its sort capability
    X.make_pair(pair) # wrapping pair info
    X.make_xyd(plot=True) # find direct reference from the direct image, and plot
    
    conf = ['WFC3.UVIS.G280.CHIP1.V2.0.conf'] # make a list of conf file for each pair
    X.make_conf(conf) # wrapping conf info
    X.make_xyref() # make xyref (this requires xyd from the direct image, and xyoff from the conf file)
    
    X.make_trace() # make trace solution
    LINES = [1643.9,1911.0,2299.2,2402.6]
    X.show_trace(lines=LINES) # plot trace solution, and lines
    
    X.make_wavelength() # make wavelength solution 
    X.make_aperture(apsize=5) # wrapping aperture size info, apsize = total aperture size centerred at the exact (x,y) from the trace solution.
    X.count() # sum the count for each x given in the trace solution with aperture size given by make_aperture(apsize)
    
    sens = ['wfc3_abscal_UVg280_1st_sensTV3.fits','wfc3_abscal_UVg280_1st_sensTV3.fits'] # each file parallels to grism image. Use X.grism.keys() for the list of grism image
    X.make_sens(sens) # read sens file for its (wavelength, sensitivity, e_sensitivity), and make a linear interpolate model
    X.make_apcorr() # calculate aperture correction. This is not implemented in this version yet. Set to 1. by default.
    X.make_wavebin() # calculate wavebin (i.e., wavelength width in the unit of A/pix) by using (tracex, wavelength) solution
    X.c2flam() # converting from counts to flam unit. If the count unit is ELECTRONS (i.e., WFC3/UVIS), EXPTIME is applied to change to e/s
    X.show_grism(x,y,log,lines) # plot info from each grism by specifying (x,y) using the keys (i.e., from X.grism[grism_index][keys]). x='wavelength', y='count' by defaults. lines can be supplied.
    ----------
    
    GND (standing for grism and direct images) is a class containing information, and functions to perform grism reduction. The info includes:
    """
    def __init__(self,files):
        self.files = files
        self.meta = {}
        for i,ii in enumerate(files):
            self.meta[i] = {}
            self.meta[i]['FILE'] = ii
    ##############################
    def show_meta(self,id=None,sort=None):
        import pandas as pd
        if not sort:
            sort = ['EXPSTART','POSTARG1','POSTARG2','FILTER']
        if not id:
            display(pd.DataFrame(self.meta).T.sort_values(sort))
        else:
            x = {}
            for i,ii in enumerate(id):
                x[ii] = self.meta[ii]
            display(pd.DataFrame(x).T)
    ##############################
    def make_meta(self
                  ,keys={'PRIMARY': ['FILTER'
                                     ,'EXPSTART','EXPTIME'
                                     ,'POSTARG1','POSTARG2'
                                     ,'SUBARRAY']}):
        from astropy.io import fits
        for i in self.meta:
            x = fits.open(self.meta[i]['FILE'])
            for j in keys:
                for k in keys[j]:
                    self.meta[i][k] = x[j].header[k]
    ##############################
    def make_pair(self,pair=None):
        self.direct = list(pair.keys())
        self.pair,self.grism = {},{}
        for i in self.direct:
            self.pair[i] = {}
            self.pair[i]['grism'] = pair[i]
            for j in pair[i]:
                self.grism[j] = {}
                self.grism[j]['direct'] = i                
    ##############################
    def make_xyd(self,plot=True):
        from astropy.io import fits
        from astropy.wcs import WCS
        from astropy.coordinates import SkyCoord
        for i in self.pair.keys():
            x = fits.open(self.meta[i]['FILE'])
            xdata = x['SCI'].data
            w = WCS(x['SCI'])
            ra,dec = x[0].header['RA_TARG'],x[0].header['DEC_TARG']
            coord = SkyCoord(ra,dec,unit='deg')
            xx,yy = w.all_world2pix(coord.ra,coord.dec,1)
            self.pair[i]['xyd'] = (xx.tolist(),yy.tolist())
            if plot:
                vmin,vmax = np.percentile(xdata,5.),np.percentile(xdata,95.)
                plt.figure(figsize=(10,10)),plt.imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
                plt.scatter(*self.pair[i]['xyd'],s=30,edgecolor='red',facecolor='None')
                plt.title('{0} {1}'.format(i,self.meta[i]['FILE']))
    ##############################
    def make_conf(self,conffiles=None):
        from kbastroutils.grismconf import GrismCONF
        for i,ii in enumerate(self.pair.keys()):
            self.pair[ii]['conf'] = GrismCONF(conffiles[i])
            self.pair[ii]['conf'].fetch()
    ##############################
    def make_xyref(self):
        from astropy.io import fits
        for i in self.grism.keys():
            direct = self.grism[i]['direct']
            xyd = self.pair[direct]['xyd']
            xoff,yoff = None,None
            for j in self.pair[direct]['conf'].value.keys():
                if 'XOFF' in j:
                    xoff = self.pair[direct]['conf'].value[j]
                if 'YOFF' in j:
                    yoff = self.pair[direct]['conf'].value[j]
            post1,post2 = self.meta[i]['POSTARG1'],self.meta[i]['POSTARG2']
            post1d,post2d = self.meta[direct]['POSTARG1'],self.meta[direct]['POSTARG2']
            scale = fits.open(self.meta[i]['FILE'])[1].header['IDCSCALE']
            scaled = fits.open(self.meta[direct]['FILE'])[1].header['IDCSCALE']
            dx = post1/scale - post1d/scaled
            dy = post2/scale - post2d/scaled
            xref = xyd[0] + xoff + dx
            yref = xyd[1] + yoff + dy
            self.grism[i]['xyref'] = (xref[0],yref[0])
    ##############################
    def make_trace(self):
        import numpy as np
        for i in self.grism.keys():
            direct = self.grism[i]['direct']
            xref,yref = self.grism[i]['xyref'][0],self.grism[i]['xyref'][1]
            value = self.pair[direct]['conf'].value
            order = value['DYDX_ORDER_A'].astype(int)
            d = []
            for j in np.arange(order + 1):
                string = 'DYDX_A_{0}'.format(j)
                y = value[string]
                px,py = 0,0
                a = [(px,py)]
                b = [(xref,yref)]
                p = 0
                q = True
                while(q):
                    if px==0:
                        p+=1
                        px=p
                        py=0
                    else:
                        px-=1
                        py+=1
                    a.append((px,py))
                    b.append((xref,yref))
                    if len(a)>=len(y):
                        q = False
                a,b = np.array(a),np.array(b)
                c = b**a
                c = np.sum(c[:,0]*c[:,1]*y)
                d.append(c)
            d = np.array(d)
            self.grism[i]['dydx'] = np.copy(d)
            xmin,xmax = value['BEAMA']
            xhat = np.arange(xmin,xmax+1,step=1.)
            yhat = np.full_like(xhat,0.,dtype=float)
            for j,jj in enumerate(d):
                yhat += jj * xhat**j
            xx,yy = xref+xhat,yref+yhat
            self.grism[i]['tracex'] = xx
            self.grism[i]['tracey'] = yy
    ##############################
    def make_wavelength(self):
        import numpy as np
        varclength = np.vectorize(self.arclength)
        for i in self.grism.keys():
            direct = self.grism[i]['direct']
            xref,yref = self.grism[i]['xyref'][0],self.grism[i]['xyref'][1]
            value = self.pair[direct]['conf'].value
            order = value['DISP_ORDER_A'].astype(int)
            d = []
            for j in np.arange(order + 1):
                string = 'DLDP_A_{0}'.format(j)
                y = value[string]
                px,py = 0,0
                a = [(px,py)]
                b = [(xref,yref)]
                p = 0
                q = True
                while(q):
                    if px==0:
                        p+=1
                        px=p
                        py=0
                    else:
                        px-=1
                        py+=1
                    a.append((px,py))
                    b.append((xref,yref))
                    if len(a)>=len(y):
                        q = False
                a,b = np.array(a),np.array(b)
                c = b**a
                c = np.sum(c[:,0]*c[:,1]*y)
                d.append(c)
            d = np.array(d)
            self.grism[i]['dldp'] = np.copy(d)
            xmin,xmax = value['BEAMA']
            xhat = np.arange(xmin,xmax+1,step=1.)
            arc,earc = np.array(varclength(xhat,*self.grism[i]['dydx']))
            yhat = np.full_like(xhat,0.,dtype=float)
            for j,jj in enumerate(d):
                yhat += jj * arc**j
            xx,yy = xref+xhat,yhat
            self.grism[i]['wavelength'] = yy
    ##############################
    def arclength_integrand(self,Fa,*coef):
        import numpy as np
        s = 0
        for i,ii in enumerate(coef):
            if i==0:
                continue
            s += i * ii * (Fa**(i-1))
        return np.sqrt(1. + np.power(s,2))
    ##############################
    def arclength(self,Fa,*coef):
        from scipy.integrate import quad
        integral,err = quad(self.arclength_integrand, 0., Fa, args=coef)
        return integral,err
    ##############################
    def show_trace(self,lines=None):
        from astropy.io import fits
        import matplotlib.pyplot as plt
        import numpy as np
        for i,ii in enumerate(self.grism.keys()):
            x = fits.open(self.meta[ii]['FILE'])
            xdata = x['SCI'].data
            fig,ax = plt.subplots(1,3,figsize=(40,10))
            vmin,vmax = np.percentile(xdata,5.),np.percentile(xdata,95.)
            ax[0].imshow(xdata,origin='lower',cmap='viridis',vmin=vmin,vmax=vmax)
            xx,yy,ww,cc = self.grism[ii]['tracex'],self.grism[ii]['tracey'],self.grism[ii]['wavelength'],self.grism[ii]['count']
            xyd = self.pair[self.grism[ii]['direct']]['xyd']
            ax[0].scatter(*xyd,s=100,edgecolor='red',facecolor='red')
            xyref = self.grism[ii]['xyref']
            ax[0].scatter(*xyref,s=100,edgecolor='orange',facecolor='orange')
            ax[0].plot(xx,yy,'r-')
            dx,dy = 500,300
            ax[0].set_xlim(np.min(xx)-dx,np.max(xx)+dx)
            ax[0].set_ylim(xyref[1]-50,xyref[1]+dy)
            ax[1].plot(ww,xx)
            ax[2].plot(ww,cc)
            if lines:
                ymin,ymax = np.min(cc),np.max(cc)
                for j,jj in enumerate(lines):
                    ax[2].plot([jj,jj],[ymin,ymax],'--')
    ##############################
    def make_aperture(self,apsize=5):
        for i,ii in enumerate(self.grism.keys()):
            self.grism[ii]['apsize'] = apsize
    ##############################
    def count(self):
        from astropy.io import fits
        import numpy as np
        for i,ii in enumerate(self.grism.keys()):
            x = fits.open(self.meta[ii]['FILE'])
            xdata,xerr,xdq = x['SCI'].data,x['ERR'].data,x['DQ'].data
            tracex,tracey = self.grism[ii]['tracex'].astype(int),self.grism[ii]['tracey'].astype(int)
            dy = int(0.5*(self.grism[ii]['apsize']-1))
            c = np.full_like(tracex,np.nan,dtype=float)
            for j,jj in enumerate(tracex):
                ymin,ymax = tracey[j]-dy,tracey[j]+dy+1
                c[j] = np.sum(xdata[ymin:ymax,jj])
            self.grism[ii]['count'] = np.copy(c)
            self.grism[ii]['count_unit'] = x['SCI'].header['BUNIT']  
    ##############################
    def make_sens(self,files):
        from kbastroutils.grismsens import GrismSens
        for i,ii in enumerate(self.grism.keys()):
            self.grism[ii]['sens'] = GrismSens(files[i])
    ##############################
    def make_wavebin(self):
        import numpy as np
        for i,ii in enumerate(self.grism.keys()):
            w = self.grism[ii]['wavelength']
            dw = np.diff(w)
            med = [np.median(dw)]
            self.grism[ii]['wavebin'] = np.abs(np.concatenate((med,dw)))
    ##############################
    def make_apcorr(self):
        for i,ii in enumerate(self.grism.keys()):
            apsize = self.grism[ii]['apsize']
            print('Error: make_apcorr is not implemented in this version. Set to 1.')
            self.grism[ii]['apcorr'] = 1.
    ##############################
    def c2flam(self):
        for i,ii in enumerate(self.grism.keys()):
            smod = self.grism[ii]['sens'].model
            ww,cc = self.grism[ii]['wavelength'],self.grism[ii]['count']
            if self.grism[ii]['count_unit'] == 'ELECTRONS':
                cc = cc / self.meta[ii]['EXPTIME']
            apcorr,wavebin,sens = self.grism[ii]['apcorr'],self.grism[ii]['wavebin'],smod(ww)
            self.grism[ii]['flam'] = cc * wavebin / apcorr / sens
    ##############################
    def show_grism(self,x='wavelength',y='count',log=False,lines=None):
        import matplotlib.pyplot as plt
        import numpy as np
        for i,ii in enumerate(self.grism.keys()):
            xx = self.grism[ii][x]
            yy = self.grism[ii][y]
            plt.figure(figsize=(10,10))
            plt.plot(xx,yy,label=y)
            if lines:
                iii = ~np.isnan(yy) & np.isfinite(yy)
                ymin,ymax = np.min(yy[iii]),np.max(yy[iii])
                for j,jj in enumerate(lines):
                    plt.plot([jj,jj],[ymin,ymax],'--')
            plt.legend()
            plt.show()
            
            