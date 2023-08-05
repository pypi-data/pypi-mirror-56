================
Multi Processing
================

Start by importing UBCS LCP auxiliary package library.

first you can install the auxiliary library

.. code-block:: shell

  pip3 install ubcs_auxiliary

you may need to upgrade the library if it was installed before

.. code-block:: shell

  pip3 install --upgrade ubcs_auxiliary

>>> from ubcs_auxiliary.multi_processing import MultiProcessing
>>> def function(N):
        from time import time, sleep
        import os
        print('Starting Process: pid: {}'.format(os.getpid()))
        t1 = time()
        print('[{} s] Start sleeping for {} seconds'.format(round(time()-t1,4),N))
        print('[{} s] Sleeping... '.format(round(time()-t1,4)))
        sleep(N)
        print('[{} s] Done sleeping for {} seconds'.format(round(time()-t1,4),N))
>>> mp = MultiProcessing(function, (1,2,3))
    Starting Process: pid: 91038
    [0.0 s] Start sleeping for 1 seconds
    [0.0001 s] Sleeping...
    Starting Process: pid: 91039
    [0.0 s] Start sleeping for 2 seconds
    [0.0001 s] Sleeping...
    Starting Process: pid: 91040
    [0.0 s] Start sleeping for 3 seconds
    [0.0002 s] Sleeping...
    [1.0003 s] Done sleeping for 1 seconds
    [2.0001 s] Done sleeping for 2 seconds
    [3.0013 s] Done sleeping for 3 seconds

.. autoclass:: ubcs_auxiliary.multi_processing.MultiProcessing
  :members:

  .. automethod:: __init__

.. automodule:: ubcs_auxiliary.multi_processing
  :members:
