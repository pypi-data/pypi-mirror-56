# nds2utils

nds2utils is a user interface for the python nds2 client.  
nds2 error messages and data structures can be hard to parse.
nds2utils provides helper functions, defaults, warnings, and error messages for users trying to get ligo data with python.
Git repository is at [https://git.ligo.org/craig-cahillane/nds2utils](https://git.ligo.org/craig-cahillane/nds2utils)

# Features

- Quick and easy data acquisition using nds2. `acquire_data()`
- Acquisition of data in real-time `stitch_real_time_data()`
- Automatic computation of power spectral densities, cross spectral densities, transfer functions, and coherence `'get_PSDs(), get_CSDs()'`
- Quick plotting of your data `plot_ASDs, plot_TFs_A, plot_TFs_A`
- Interactive legend - click on line in legend to toggle it
- Logbinning
- Calibration using zpk
- Examples
- Docstrings.  If in doubt about a function, look in the docstrings, using, e.g. `nu.acquire_data?`

# Installation

This library requires numpy , scipy, nds2-client, python-nds2-client, and matplotlib,
You can either conda install or pip install
```
conda install numpy scipy nds2-client python-nds2-client matplotlib
```
```
pip install numpy scipy nds2-client python-nds2-client matplotlib
```
Tested versions at the time of this publishing:
- python              3.7.3
- numpy               1.17.0
- scipy               1.3.1
- nds2-client         0.16.3
- python-nds2-client  0.16.4
- matplotlib          3.1.1

You can install nds2utils using `pip` at https://pypi.org/project/nds2utils/
```
pip install nds2utils
```

# Quick Start

You will have to `kinit albert.einstein@LIGO.ORG` to start a kerberos authenticated session to allow you to access data.

## Get raw time series data

```python
import nds2utils as nu

channels = ['H1:CAL-DELTAL_EXTERNAL_DQ', 'H1:LSC-REFL_SERVO_ERR_OUT_DQ']
gps_start = 1256771562
gps_stop  = 1256771712
dataDict = nu.acquire_data(channels, gps_start, gps_stop)

cal_deltal_external_data = dataDict['H1:CAL-DELTAL_EXTERNAL_DQ']['data'] # this is where the data is stored

# Plot raw time series data
nu.plot_raw_data(dataDict, seconds=150, downsample=2**10)
```

## Get data and take PSDs, CSDs, and TFs of time series data

```python
import nds2utils as nu

channels = ['H1:CAL-DELTAL_EXTERNAL_DQ', 'H1:PSL-ISS_SECONDLOOP_RIN_OUTER_OUT_DQ']
gps_start = 1256771562
gps_stop  = 1256771712
binwidth = 0.1 # Hz, frequency vector spacing
overlap = 0.5 # FFT overlap ratio

dataDict = nu.get_CSDs(channels, gps_start, gps_stop, binwidth, overlap)

nu.plot_ASDs(dataDict, title='Uncalibrated and Logbinned DARM and CARM spectra', logbin=True)
```

# Slow Start

Valid Host Sever:Port Number combos:
```
host_server:port_number
h1nds1:8088                   # only good on LHO CDS computers
h1nds0:8088                   # only good on LHO CDS computers
nds.ligo-wa.caltech.edu:31200 # LHO frame cache
nds.ligo-la.caltech.edu:31200 # LLO frame cache
nds.ligo.caltech.edu:31200    # Caltech frame cache
131.215.115.200:31200         # Caltech 40 meter
```

Important functions you will want to use:
```python
find_channels('H1:CAL*DQ') # Accepts a channel glob, returns matching channels
acquire_data() # Accepts array of channel names, gps_start, and gps_stop.  Returns dictionary containing the data.
```

Open an ipython terminal, and import the dataUtils library by running
```python
import nds2utils as nu
from nds2utils.dataUtils import *
```

You can't remember the exact name for the calibrated DARM channel you want, so you run
```python
find_channels('H1:CAL*DQ')
```

You see the channel you want in the output, `H1:CAL-DELTAL_EXTERNAL_DQ`.

You want to look at the DARM and intensity noise witness channel amplitude spectral density and transfer function at the time there was excess intensity noise at LIGO Hanford.  
You happen to know the gps times you want to look at.  
You rerun `find_channels('H1:PSL-ISS_SECONDLOOP*DQ')` and find the out of loop intensity noise witness channel, `H1:PSL-ISS_SECONDLOOP_RIN_OUTER_OUT_DQ`:
```python
channels = np.array(['H1:CAL-DELTAL_EXTERNAL_DQ', 'H1:PSL-ISS_SECONDLOOP_RIN_OUTER_OUT_DQ'])
gps_start = 1256805122
duration = 100 # seconds
gps_stop = gps_start + duration
binwidth = 1  # Hz, frequency bin spacing for the ASDs and TFs.
overlap = 0.5 # fraction between 0 and 1.  overlap ratio for the data window.

# Get time-series of data and sampling frequency,
# and calculate PSDs, ASDs, CSDs, and TFs between all channels
# stored in a dictionary with channel names as keys, and dictionaries for values.
dataDict = get_CSDs(channels, gps_start, gps_stop, binwidth, overlap)  
```

`dataDict` is a dictionary of dictionaries.
The top level dictionary uses channel names as keys, and returns values which are dictionaries containing the data relevant to the channel key.
You define a second-level dictionary, `darmDict`, to look only at the darm dictionary:
```python
print(darmDict.keys())

darmDict = dataDict['H1:CAL-DELTAL_EXTERNAL_DQ']

print(darmDict.keys())
```

`darmDict` contains the following keys:

Raw data keys:
- `'data'`     = the raw data from the channel
- `'fs'`       = sampling frequency of the data
- `'gpsStart'` = gps time representing the first data point acquired
- `'duration'` = time length of data acquired

PSD data keys:
- `'averages'` = int.   number of averages for the power spectral density calculation
- `'binwidth'` = float. Hz, frequency bin spacing for the ASDs and TFs
- `'overlap'`  = float. fraction between 0 and 1.  overlap ratio for the data window.
- `'fftLen'`   = float. length in seconds for the FFTs. Used in scipy.welch() PSD calculation.
- `'nperseg'`  = int.   number of samples per FFT segment.
- `'ff'`       = array. frequency vector for this channels ASDs and PSDs
- `'PSD'`      = array. power spectral density in units^2/Hz
- `'ASD'`      = array. amplitude spectral density in units/rtHz
- `'df'`       = float. Hz. delta frequency vector, should be the same as binwidth.

CSD and TF data keys: (names of all other channels, in this case, `'ISS_SECONDLOOP_RIN_OUTER_OUT_DQ'`:
- `'H1:PSL-ISS_SECONDLOOP_RIN_OUTER_OUT_DQ'` = dictionary containing CSD, TF, and coherence info.

We make another definition of the third level dictionary to get CSD and TF info:
```python
iss2darmDict = dataDict['H1:CAL-DELTAL_EXTERNAL_DQ']['H1:PSL-ISS_SECONDLOOP_RIN_OUTER_OUT_DQ']
print(iss2darmDict.keys())
```
`iss2darmDict` contains the following keys:
- `'ff'`       = array. frequency vector for these two channels CSDs, TFs, and coherences
- `'CSD'`      = array. cross spectral density in units $`\mathrm{unit_a} * \mathrm{unit_b}/\mathrm{Hz}`$
- `'TF'`       = array. transfer function in $`\mathrm{unit_b} / \mathrm{unit_b}`$
- `'coh'`      = array. power coherence, unitless $` \gamma^2 = |\mathrm{CSD}_{AB}|^2 / (\mathrm{PSD}_A * \mathrm{PSD}_B) `$

The convention for the cross spectral density: The first channel is the complex conjugated one.

- `dataDict[chanB][chanA]['CSD']` = $`\mathrm{CSD}_{AB}`$ = $`\langle{b^*}\rvert{a}\rangle`$

The convention for the transfer function: chanB is the first channel in the dataDict, chanA is the second:

- `dataDict[chanB][chanA]['TF']` = H(f) = $`\frac{\mathrm{CSD}_{AB}}{\mathrm{PSD}_{A}}`$ = $`\frac{\langle{a^*}\rvert{b}\rangle}{\langle{a^2}\rangle}`$

The convention for the coherence: coherence is the power coherence:

- `dataDict[chanB][chanA]['coh']` = $`\gamma^2 = \frac{|\langle{a^*}\rvert{b}\rangle|^2}{\langle{a^2}\rangle \langle{b^2}\rangle}`$

If you add a calibration using calibrate_chan(), you will have new keys in your dictionary:
- `'calASD'`
- `'calPSD'`
- `'calCSD'`
- `'calTF'`
