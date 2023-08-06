The Isotel IDM Python API Release Notes
=======================================

- Project home: http://isotel.eu/idm
- Distribution: https://pypi.org/project/isotel-idm/

-------------

Beta-Release 1.0b21 on 26. November 2019
----------------------------------------

- Added signal test functions: rms() for dc/ac, sinad_dB(), enob()
- Added spectrum analysis: tospectrum() with blackmanharris windows of 3,4 and 7 terms
- Added fast pyqtgraph based: qscope() for real-time simultaneous presentation of
  signal and spectrum at the same time

Beta-Release 1.0b20 on 8. June 2019
-----------------------------------

- Fixed monodaq.print_setup() to work with remote systems requiring user/pass
- Added history dumping to monodaq main for bounded interval from, to, with optional
  scaling (down-sampling).

Release 1.0a19
--------------

- Added flex non-equiv-distant interval sampling to collect() method, based on
  time samples as they arrive from devices themself.
- Added until parameter to get() and get_value() methods. Requires idm-1.1a5/b5
  and example. It allows retrieval of data with natural arrival from the devices
  in a bounded time frame interval.


Release 1.0a18 on 1. Feb 2019
-----------------------------

- Added support to instantiate inactive device and retrieve its latest status
  with get(), get_value(), and get_records()


Release 1.0a17 on 30. Jan 2019
------------------------------

- Added Device.collect() method to continuously fetch samples from given parameter
  and output it as a generator, to be used by isotel.idm.signal methods in the
  same way as MonoDAQ_U.fetch()
- Added incremental option to the signal.stream2signal() to continuously update
  slow signals, i.e. with signal.scope() method.
- Increased number of decimals for MonoDAQ_U.fetch() to be able to observe every LSB


Release 1.0a16 on 23. Jan 2019
------------------------------

- Aligned with the latest API from IDM 1.1b3
- Gateway default time-out increased to 60 seconds (from 10 seconds) for slow networks


Release 1.0a15 on 5. Nov 2018
-----------------------------

- MonoDAQ time is left untouched after first synchronization to be compatible
  with the Dewesoft plugin.


Release 1.0a14 on 17. Oct 2018
-----------------------------

- Added Multi-Rate support to synchronous Multi-MonoDAQs fetch


Release 1.0a13 on 15. Oct 2018
------------------------------

- Added class MonoDAQs_U with synchronous fetch from multiple MonoDAQs
- Added EC class with helper function to configure common and channel options


Release 1.0a12 on 9. Oct 2018
-----------------------------

- Relaxed requirements, on MAC you would need to install as
  pip install isotel-idm requests==2.8.1


Release 1.0a11 on 7. Oct 2018
-----------------------------

- TSV format outputs no-value on None or NaN
- MonoDAQ fixed mdu.reset() to properly clean on remote devices
- pypy: Fixed not raised GeneratorExit exception


Release 1.0a9 on 5. Oct 2018
----------------------------

- Fixed div by zero in digital only operation
- MonoDAQ: added command line tool: python -m isotel.idm.monodaq -h
- Signal: Added to TSV generator


Release 1.0a7 on 4. Oct 2018
----------------------------

- Fixed digital only operation


Release 1.0a6 on 3. Oct 2018
----------------------------

- Added packet counter checks to detect lost packets and to detect
  potential mis-alignment of signals from various streams.
- In trigger single shot mode when signal is acquired, generator
  exists and consequently MonoDAQ_U stops streaming. So in the
  following example number of samples may be used as timeout until
  the first triggering:

   signal.trigger( mdu.fetch(2000000), precond='DI1 < 0.5', cond='DI1 > 0.5', P=200, N=200, single_shot=True)

- MonoDAQ_U: added support for 7 channels


Release 1.0a5 on 30. Sep 2018
------------------------------

- First published release supporting Isotel Precision & MonoDAQ-U-X products