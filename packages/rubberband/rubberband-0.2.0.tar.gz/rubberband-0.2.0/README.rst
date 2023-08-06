README for rubberband Python3 Module
====================================

Introduction
------------

**rubberband** is a simple Python3 wrapper around the well-known librubberband_ sound stretching / pitch-shifting library.  Unlike existing Python wrappers (e.g. pyrubberband_) this is a true native extension.

The initial release provides a single function that will stretch a mono audio stream my multiplying its duration by a provided factor.  Future versions may include pitch shifting, and more complex processing based on data maps.

Installation
------------

The module is available only for MacOS and Linux.  The code may compile on Windows, but it has not been tested. Dependencies are:

    - Python 3 (preferably 3.6 or greater)
    - librubberband_ (> 1.8)
    - libsndfile_ (> 1.0)

Assuming these dependencies are met, then installation is simplicity itself::

    pip3 install rubberband


The install script does check for the required libraries, and will complain vociferously if they cannot be located.  Information on obtaining them is available from the links above.

API
---

    **rubberband.stretch** (*inarray*, *rate* , *ratio* , *crispness* = **5** , *formants* = **False** )

    Arguments   

        *inarray*
            input audio is assumed to be encoded as single-dimensional NUMPY_ arrays of type **float32**.  librubberband assumes that input data is normalised to the range [-1,1]; **rubberband.stretch** automatically applies normalisation if it is required

        *rate*
            the frame rate of the input audio stream (so bit rate divided by sample size)

        *ratio*
            the ration of output length to input length (in seconds / number of samples)

        *crispness*
            integer 0 - 6, default 5: measure of performance - see the `rubberband-cli documentation`_ for more details

        *formants*
            Boolean, default **False** : whether or not to preserve formants - see the `rubberband-cli documentation`_ for more details

    Return value
        a one-dimensional NUMPY array of type **float32** containing the stretched audio data

Example
-------

  .. code:: python

    import rubberband 
    from sound import wavfile

    nFrames = None
    rate = None
    bitrate = None
    stream = None

    with wavfile("infile.wav",rw='r') as wav:
        rate=wav.rate
        bitrate=rate*16
        stream = wav.read()

    nFrames=len(stream)
    oldDuration=nFrames/rate

    newDuration=4
    ratio=newDuration/oldDuration
    print(f'Ratio is {ratio}')

    out=rubberband.stretch(stream,rate=bitrate,ratio=ratio,
                           crispness=5,formants=True)

    with wavfile("outfilet.wav",rw='w',rate=rate) as f:
        f.write(out)



.. _librubberband: https://breakfastquay.com/rubberband/
.. _pyrubberband: https://pypi.org/project/pyrubberband/
.. _libsndfile: http://www.mega-nerd.com/libsndfile/
.. _`rubberband-cli documentation`: https://breakfastquay.com/rubberband/usage.txt
.. _NUMPY: https://numpy.org




