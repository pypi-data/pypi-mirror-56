# COMPAS File Reader for Python #

A library to read/convert COMPAS ECG measurement files

### Prerequisites ###

* numpy 

### Installation ###

    $ pip install compaslib

### Example ###

    from compaslib import ReadTWBFile
    
    # Read a COMPAS binary file from disk:
    beats, headers = ReadTWBFile('filename.twb')

    # Print RR values of the first 10 beats:
    idx = headers.index('RR')
    print( [beat[idx] for beat in beats[:10]] )

TODO: more examples / function descriptions

### WARNING ###

Always double-check the times produced by this library when reading a binary (TWB) file.  They may not match the local time of the ECG due to the insane format in which COMPAS stores times.  Further, COMPAS may start at 00:00:00 rather than even trying to save the actual start time.

### Who do I talk to? ###

* Alex Page, alex.page@rochester.edu