"""Read a COMPAS TWB or TXT file."""

################################### Imports: ###################################

import os
import numpy as np
import datetime

############################### Main functions: ################################

def ReadTXTFile(fileName, max_beats=500000):
    """Read a COMPAS TXT file and return a 2D array containing the data for all
    beats, along with the column headers for that array.  Date and time are
    converted to date and time objects, and all other values are converted to
    float (or None).
    """
    measurements = []
    headers = []
    with open(fileName) as f:
        for i, line in enumerate(f):
            if headers==[]:
                candidate_headers = [val.strip() for val in line.strip().split('\t')]
                if candidate_headers[:2] == ['Day','Time']:
                    headers = candidate_headers
                    headers = ['Date' if v=='Day' else v for v in headers]
                continue
            beat = [val.strip() for val in line.strip().split('\t')]
            # we'll assume first 2 cols are Date and Time
            dt = datetime.datetime.strptime(beat[0]+' '+beat[1], '%m/%d/%Y %H:%M:%S')
            meas = [float(m) if float(m)!=-9 else None for m in beat[2:]]
            measurements.append([dt.date(), dt.time()] + meas)
    return measurements, headers

def ReadIcardiacFile(fileName, max_beats=500000):
    """Read a COMPAS-like text file from iCardiac and return a 2D array containing
    the data for all beats, along with the column headers for that array.  Date
    and time are converted to date and time objects, and all other values are
    converted to float (or None).
    """
    sr = None; start_datetime = None; headers = None; results = []
    with open(fileName) as f:
        for i, line in enumerate(f):
            if line.startswith('Frequency: '):
                # sr = float( line.strip().split(' ')[-1] )  # if times are in samples
                sr = 1000  # if times are in msec (so this isn't really SR)
                continue
            if line.startswith('DateRecorded: '):
                d = line.strip().split(' ')[-1]
                start_datetime = datetime.datetime.strptime( d , '%Y%m%d%H%M%S' )
                continue
            if line.startswith('BeatIndex'):
                headers = line.strip().split('\t')
                continue
            if headers == None: continue
            beat = [val.strip() for val in line.strip().split('\t')]
            meas = [float(m) if float(m)!=-9 else None for m in beat]
            sample = meas[ headers.index('R') ]
            dt = start_datetime + datetime.timedelta(seconds=sample/sr)  # TODO?: float
            # TODO: flag to skip beats where beatstability != 0 (and possibly
            # prev+next beats too).  i.e. don't append to results when
            # meas['beatstability'] != 0.  may want something similar if QT or
            # RR are None.
            results.append( [dt.date(), dt.time()] + meas )
    # Hack to handle a specific typo I've seen:
    if headers == ['BeatIndex', 'R', 'RR', 'QTApex_I', 'QTApex_II', 'QTApex_II', 'QTApex_V1', 'QTApex_V2', 'QTApex_V3', 'QTApex_V5', 'QTApex_V5', 'QTApex_V6', 'QTend_I', 'QTend_II', 'QTend_II', 'QTend_V1', 'QTend_V2', 'QTend_V3', 'QTend_V5', 'QTend_V5', 'QTend_V6', 'QTcF_I', 'QTcF_II', 'QTcF_II', 'QTcF_V1', 'QTcF_V2', 'QTcF_V3', 'QTcF_V5', 'QTcF_V5', 'QTcF_V6', 'Tend_I', 'Tend_II', 'Tend_II', 'Tend_V1', 'Tend_V2', 'Tend_V3', 'Tend_V5', 'Tend_V5', 'Tend_V6', 'Tapex_I', 'Tapex_II', 'Tapex_II', 'Tapex_V1', 'Tapex_V2', 'Tapex_V3', 'Tapex_V5', 'Tapex_V5', 'Tapex_V6', 'TpTe_I', 'TpTe_II', 'TpTe_II', 'TpTe_V1', 'TpTe_V2', 'TpTe_V3', 'TpTe_V5', 'TpTe_V5', 'TpTe_V6', 'beatstability']:
        for i in [5,14,23,32,41,50]:
            headers[i] = headers[i].replace('II','III')
        for i in [9,18,27,36,45,54]:
            headers[i] = headers[i].replace('V5','V4')
    # end hack.
    headers = ['date','time'] + headers
    return results, headers

def ReadTWBFile(fileName, max_beats=500000, clean=True):
    """Read a COMPAS TWB file and return a 2D array containing the data for all
    beats.  The output will have the following columns, with one row for every
    beat:
      day / time (2 columns)
      sample number (1 column)
      pTWBData (numColumn columns)
      beatStability (1 column)
      Beat_Anno (1 column)
      LTangent (numLead columns)
      RTangent (numLead columns)
      TLength  (numLead columns)
      TQ       (numLead columns)
      SNR      (numLead columns)
    The pTWBData columns are:
      RR, Ampl_[all leads], QTApex_[all leads], RTApex_[all leads],
      QTOffset_[all leads], RTOffset_[all leads],
      QTA25_[all leads], RTA25_[all leads],
      QTA50_[all leads], RTA50_[all leads],
      QTA95_[all leads], RTA95_[all leads],
      QTA97_[all leads], RTA97_[all leads]
    QTc could be computed from RR and QTOffset.  Note that -9 in any field
    indicates a "non-measurable" value, and will be replaced by None.  Also,
    sinus beats will all have Beat_Anno=0.

    Keyword arguments:
    fileName -- the file to read
    max_beats -- if the file claims to have annotations for more than this number of beats, we won't process it
    clean -- remove beats with invalid sample numbers (i.e. duplicate or out of sequence)
    """
    # TODO: this function probably fails on VM files
    lFileLength = os.path.getsize(fileName)
    br = open(fileName, 'rb')

    # get number of beats (line of data):
    br.seek(lFileLength-4, os.SEEK_SET)
    numBeat = np.fromfile(br, dtype=np.int32, count=1)[0]

    if ( (numBeat<0) or (numBeat>max_beats) ):
        br.close()
        print("Got bad value (" + str(numBeat) + ") for number of beats in " + fileName + "; not loading.")
        return [], []

    br.seek(0, os.SEEK_SET)

    # read beat to beat header.  Beat-to-beat .twb files should always start with 1.
    value = np.fromfile(br, dtype=np.int32, count=1)[0]
    assert (value == 1), "Can't handle this type of input file!"
    fileNameLen = np.fromfile(br, dtype=np.int32, count=1)[0]
    charFN = np.fromfile(br, dtype=np.uint8, count=fileNameLen)
    charFN = ''.join(chr(i) for i in charFN)
    value = np.fromfile(br, dtype=np.int32, count=5)  # TODO?: don't know what this value is.
    numLead = np.fromfile(br, dtype=np.int32, count=1)[0]

    # prepare empty arrays:
    numColumn = 1 + 13*numLead
    pTime           = [None for i in range(numBeat)]
    pBeatAnnotation = [None for i in range(numBeat)]
    beatStability   = [None for i in range(numBeat)]
    sampleNum       = [None for i in range(numBeat)]
    pTWBData = [[None for col in range(numColumn)] for row in range(numBeat)]
    LTangent = [[None for col in range(numLead)] for row in range(numBeat)]
    RTangent = [[None for col in range(numLead)] for row in range(numBeat)]
    TLength  = [[None for col in range(numLead)] for row in range(numBeat)]
    TQ       = [[None for col in range(numLead)] for row in range(numBeat)]
    SNR      = [[None for col in range(numLead)] for row in range(numBeat)]

    # read data:
    for i in range(numBeat):
        pTime[i]           = np.fromfile(br, dtype=np.int32,   count=1        )[0]
        sampleNum[i]       = np.fromfile(br, dtype=np.int32,   count=1        )[0]
        pTWBData[i]  = list( np.fromfile(br, dtype=np.float32, count=numColumn) )
        beatStability[i]   = np.fromfile(br, dtype=np.uint8,   count=1        )[0]
        pBeatAnnotation[i] = np.fromfile(br, dtype=np.uint8,   count=1        )[0]
        TwaveAnnotation    = np.fromfile(br, dtype=np.uint8,   count=numLead  )     # not used.  TODO?
        LTangent[i]  = list( np.fromfile(br, dtype=np.float32, count=numLead  ) )
        RTangent[i]  = list( np.fromfile(br, dtype=np.float32, count=numLead  ) )
        TLength[i]   = list( np.fromfile(br, dtype=np.float32, count=numLead  ) )
        TQ[i]        = list( np.fromfile(br, dtype=np.float32, count=numLead  ) )
        SNR[i]       = list( np.fromfile(br, dtype=np.float32, count=numLead  ) )

    br.close()

    # make single 2D array with all results.  posix times will be converted to
    # 'day' and 'time' strings.
    output_array = [ [0 for col in range(2 + 1 + numColumn + 1 + 1 + 5*numLead)]
                        for row in range(numBeat) ]  # no row for header line
    for row in range(numBeat):
        # TWB time format is ridiculous.  The times appear to be adjusted to GMT
        # based on the time zone of the annotator, rather than the patient.  For
        # example, if the TWB is created by a computer in EST (-0500), you must
        # use EST in fromtimestamp() when you read the file, not your local time
        # zone or GMT.

        # Use this and specify the annotator's timezone as 2nd arg:
        dt = datetime.datetime.fromtimestamp(pTime[row])
        # Or use this if local time was stored:
        #dt = datetime.datetime.utcfromtimestamp(pTime[row])

        # TODO: make parameters for this function to select between no
        # correction, current tz correction, or custom tz correction.

        # TODO?: reconcile time using .txt file if available

        output_array[row] = [dt.date()] + [dt.time()] + [sampleNum[row]] + pTWBData[row] +\
                            [beatStability[row]] + [pBeatAnnotation[row]] + LTangent[row] +\
                            RTangent[row] + TLength[row] + TQ[row] + SNR[row]
    # Switch all the '-9' and NaN values to None:
    output_array = [[val if (
        (val!=-9) and
        not (isinstance(val, np.float32) and np.isnan(val))
    ) else None for val in row] for row in output_array]

    # Build the column headers:
    leadNames = get_leadnames(fileName, numLead)

    headers = ['Date', 'Time', 'Sample', 'RR']
    for measurement in [ 'Ampl', 'QTApex', 'RTApex', 'QTOffset', 'RTOffset',
                         'QTA25', 'RTA25', 'QTA50', 'RTA50', 'QTA95', 'RTA95',
                         'QTA97', 'RTA97' ]:
        for i in range(numLead):
            headers += [measurement + '_' + leadNames[i]]
    headers += ['Stability','Annotation']
    for measurement in [ 'LTangent', 'RTangent', 'TLength', 'TQ', 'SNR' ]:
        for i in range(numLead):
            headers += [measurement + '_' + leadNames[i]]

    # Remove beats with bad sample numbers:
    if clean:
        dirty_array = output_array
        output_array = []
        sidx = headers.index('Sample')
        prev_samp = -1  # for first loop iteration
        for beat in dirty_array:
            if beat[sidx] > prev_samp:
                output_array.append(beat)
                prev_samp = beat[sidx]
            # TODO?: handle first beat being a bad one (i.e. high or duplicate sample number)

    return output_array, headers

############################## Helper functions: ###############################

def get_numleads(fileName):
    br = open(fileName, 'rb')
    br.seek(4, os.SEEK_SET)  # bytes 0-3: some value we don't need
    fileNameLen = np.fromfile(br, dtype=np.int32, count=1)[0]  # bytes 4-7: string length
    br.seek(4+4+fileNameLen+20, os.SEEK_SET)  # bytes 8-M: string, bytes M-(M+20): some other value we don't need
    numLead = np.fromfile(br, dtype=np.int32, count=1)[0]
    if numLead<0: return None
    return numLead

def txt_to_leadnames(txtfile):
    leadnames = []
    with open(txtfile) as f:
        for line in f:
            fields = [cell.strip() for cell in line.split('\t')]
            if fields[0:3] == ['Day', 'Time', 'RR']:
                found = False
                for m in fields[3:]:
                    if m.startswith('QTApex_'):  # because QTApex should always be a COMPAS output (TODO: make sure that's a good assumption)
                        found = True
                        leadnames.append(m.split('_')[-1])
                    elif found:
                        break  # got them all in this row
                break  # don't have to keep searching more rows
    return leadnames

def get_leadnames(twb_filename, numLead=None):
    try:
        txtfile = os.path.splitext(twb_filename)[0] + '.txt'
        leadNames = txt_to_leadnames(txtfile)
    except IOError:
        leadNames = []
    if leadNames == []:  # txt_to_leadnames() crashed or found nothing
        if numLead==None:
            numLead = get_numleads(twb_filename)
        if numLead==3:
            leadNames = ['X', 'Y', 'Z']
        elif numLead==8:
            leadNames = ['I', 'II', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        elif numLead==12:
            leadNames = ['I', 'II', 'III', 'AVR', 'AVL', 'AVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        else:
            leadNames = [str(i+1) for i in range(12)]
        # TODO: make sure that's always the order for 3, 8, and 12 lead COMPAS files.
    return leadNames

################################################################################
