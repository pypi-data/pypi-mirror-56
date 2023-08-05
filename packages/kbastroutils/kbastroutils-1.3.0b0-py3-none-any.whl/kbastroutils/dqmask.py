class DQMask:
    """
    Example:
    data = [13, 5, 4, 2, 1, 0]
    value = [0,1,4]
    x = DQMask(value)
    x.make_mask(data)
    x.value >>> [0,1,4]
    x.combine >>> [0,1,4,5]
    x.data >>> [13, 5, 4, 2, 1, 0]
    x.mask >>> [False, True, True, False, True, True]
    -----------
    value = list of DQ classes to be set to True (default: value=[0])
    -----------
    DQ Classes:
    From the WFC3 Instrument Handbook (accessed Oct 2019), DQ classes are --
        0 # OK
        1 # Reed Solomon decoding error
        2 # Data missing and replaced by fill value
        4 # Bad detector pixel
        8 # Deviant zero read (bias) value
        16 # Hot pixel
        32 # Unstable response
        64 # Warm pixel
        128 # Bad reference pixel
        256 # Full well saturation
        512 # Bad or uncertain flat value, including 'blobs'
        1024 # (Reserved)
        2048 # Signal in zero read
        4096 # cosmic ray detected by Astrodrizzle
        8192 # Cosmic ray detected during calwf3 up the ramp fitting
        16384 # Pixel affected by ghost/crosstalk
    """
    def __init__(self,value=[0]):
        self.value = value
        self.combine = self.make_class()
        self.data = None
        self.mask = None
    def make_class(self):
        """
        Example:
        x.value = [0,1,4]
        x.combine = x.make_class()
        x.combine >>> [0,1,4,5]
        ----------
        make_class sums all possible combinations from x.value.
        """
        from itertools import combinations
        import numpy as np
        out = []
        n = len(self.value)
        for i in np.arange(n):
            x = i+1
            a = combinations(self.value,x)
            for j in list(a):
                y = np.sum(j)
                if y not in out:
                    out.append(y)
        if 0 not in out:
            out.append(0)
        return out
    def make_mask(self,data):
        """
        Example:
        data = [13, 5, 4, 2, 1, 0]
        x.combine = [0,1,4,5]
        x.mask = x.make_mask(data)
        x.mask >>> [False, True, True, False, True, True]
        ----------
        make_mask takes self.combine and data, and returns self.mask as a bool array parallel to data with 
        x.mask[i] = True if data[i] in x.combine, and x.mask[i] = False otherwise.
        """
        import numpy as np
        self.data = data
        self.mask = np.full_like(self.data,fill_value=False,dtype=bool)
        for i in self.combine:
            self.mask[self.data == i] = True