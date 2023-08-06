import numpy as np
from scipy.interpolate import interp2d
import copy
class PhotApCorr:
    def __init__(self):
        TABLE = {'WFC3-IR': 
                 {'ref': 'WFC3 Instrument Handbook, Ch 7.6 + 9.3'
                  ,'scale': 0.13
                  ,'scaleunit': 'arcsec/pix'
                  ,'type': 'radius'
                  ,'row': 'apsize'
                  ,'col': 'wave'
                  ,'apunit': 'arcsec'
                  ,'apsize': np.array((0.10,0.15,0.20,0.25,0.30
                                       ,0.40,0.50,0.60,0.80,1.00
                                       ,1.50,2.00
                                      ))
                  ,'waveunit': 'A'
                  ,'wave': np.array((7000.,8000.,9000.,10000.,11000.,12000.,13000.,14000.,15000.,16000.,17000.))
                  ,'value' : np.array(((0.575,0.549,0.524,0.502,0.484,0.468,0.453,0.438,0.426,0.410,0.394)
                                       ,(0.736,0.714,0.685,0.653,0.623,0.596,0.575,0.558,0.550,0.539,0.531)
                                       ,(0.802,0.794,0.780,0.762,0.739,0.712,0.683,0.653,0.631,0.608,0.590)
                                       ,(0.831,0.827,0.821,0.813,0.804,0.792,0.776,0.756,0.735,0.708,0.679)
                                       ,(0.850,0.845,0.838,0.833,0.828,0.822,0.816,0.808,0.803,0.789,0.770)
                                       ,(0.878,0.876,0.869,0.859,0.850,0.845,0.841,0.838,0.840,0.836,0.832)
                                       ,(0.899,0.894,0.889,0.884,0.878,0.868,0.858,0.852,0.852,0.850,0.848)
                                       ,(0.916,0.913,0.904,0.897,0.893,0.889,0.883,0.875,0.870,0.863,0.859)
                                       ,(0.937,0.936,0.929,0.924,0.918,0.909,0.903,0.900,0.903,0.900,0.895)
                                       ,(0.951,0.951,0.946,0.941,0.935,0.930,0.925,0.920,0.917,0.912,0.909)
                                       ,(0.967,0.969,0.967,0.965,0.963,0.959,0.954,0.951,0.952,0.948,0.943)
                                       ,(0.974,0.977,0.976,0.975,0.973,0.972,0.969,0.967,0.970,0.967,0.963)
                                     ))
                  ,'ZP': np.array((('F098M',9864.7,25.68)
                                   ,('F105W',10551.0,26.27)
                                   ,('F110W',11534.4,26.82)
                                   ,('F125W',12486.1,26.24)
                                   ,('F140W',13922.8,26.46)
                                   ,('F160W',15369.1,25.95)
                                  ))
                  ,'ZPunit': ('filter','pivot wavelength Angstrom','ABMAG ZP')
                  ,'model': None
                 }
                }
        self.table = TABLE
        self.instrument = list(TABLE.keys())
        self.make_model()
    def make_model(self):
        for i in self.instrument:
            apsize = np.copy(self.table[i]['apsize'])
            wave = np.copy(self.table[i]['wave'])
            value = np.copy(self.table[i]['value'])
            model = interp2d(wave,apsize,value,kind='linear',copy=True
                             ,bounds_error=False,fill_value=np.nan
                            )
            self.table[i]['model'] = copy.deepcopy(model)
    def make_apcorr(self,instrument,wave,apsize,apunit='pix'
                    ,replace='median'
                   ):
        apunittab = self.table[instrument]['apunit']
        model = self.table[instrument]['model']
        apsize2 = None
        value = None
        if (apunittab=='arcsec') & (apunit=='pix'):
            apsize2 = self.pix2arcsec(instrument,apsize)
        elif (apunittab=='pix') & (apunit=='arcsec'):
            apsize2 = self.arcsec2pix(instrument,apsize)
        value = model(wave,apsize2)
        if replace=='median':
            median = np.median(value[np.where(np.isfinite(value))])
            value[np.where(~np.isfinite(value))] = median
        value[np.where(value <= 0.)] = 0.
        value[np.where(value >= 1.)] = 1.        
        return value
    def pix2arcsec(self,instrument=None,pixsize=None):
        out = None
        if not instrument:
            print('Error: instrument is required. Set to None')
            return
        if not pixsize:
            print('Error: pixsize is required. Set to None')
            return
        scale = self.table[instrument]['scale']
        scaleunit = self.table[instrument]['scaleunit']
        if scaleunit=='arcsec/pix':
            out = pixsize * scale
        elif scaleunit=='pix/arcsec':
            out = pixsize.astype(float) / scaleunit
        else:
            print('Error: invalid scaleunit. Set to None')
        return out
    def arcsec2pix(self,instrument=None,arcsec=None):
        out = None
        if not instrument:
            print('Error: instrument is required. Set to None')
            return
        if not arcsec:
            print('Error: arcsec is required. Set to None')
        scale = self.table[instrument]['scale']
        scaleunit = self.table[instrument]['scaleunit']
        if scaleunit=='arcsec/pix':
            out = arcsec.astype(float) / scale
        elif scaleunit=='pix/arcsec':
            out = arcsec.astype(float) * scale
        else:
            print('Error: invalid scaleunit. Set to None')
        return out
