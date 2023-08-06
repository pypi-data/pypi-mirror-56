# KBAstroUtils

This is a collection of modules for analyses related to astrophysics by Dr. Kornpob Bhirombhakdi. Contact: kbhirombhakdi@stsci.edu

Tasks include:

    - dqmask.py = handle data quality (DQ) arrays
    
    - container.py = handle declaring attibutes given keys and values
    
    - segmentation.py = wrapper for making a segmentation map (used to be source.py in version < 1.2.0)
    
    - sub2full.py = mapping a subarray image back to its full frame
    
    - gnd.py = wrapper, and main class for grism reduction
    
    - grismconf.py = read conf file for grism reduction
    
    - grismsens.py = read sens file for grism reduction
    
    - grismapcorr.py = read aperture correction table, and calculate aperture correction factor
    
    - make_sip.py = calculate Simple Imaging Polynomial (SIP)
    
    - photapcorr.py = read photometric calibration table, and prepare calibration factors (i.e., encircled energy correction, and photometric AB zeropoint)
    
    - mag2flux.py = converting ABmag to flam
        
Known issues:

    - No description/documentation
    
    - Handling other telescopes
        
    - flux2mag.py
    
    - AB2Vega.py
    
    - Vega2AB.py

v.2.1.0a

    - Add functionalities in GND.show(method='clean', traceon=True, zoom=True)
    
    - Implement: photapcorr.py, mag2flux.py

v.2.0.0

    - New APIs: gnd.py
    
    - Demo provided
    
    - Implement: grismapcorr.py, make_sip.py
    
---

v.1.3.1

    - Fix import

v.1.3.0

    - Implement: grismconf.py, gnd.py, grismsens.py
    
v.1.2.0

    - Implement: sub2full.py

    - Change: source.py to segmentation.py
    
    - Fix description: segmentation.py

v.1.1.0

    - Implement: container.py, source.py
    
    - Fix description: dqmask.py
    
v.1.0.2

    - Fix description of dqmask.py
    
v.1.0.1

    - Fix import modules in dqmask.py
    
v.1.0.0

    - Implement dqmask.py
    