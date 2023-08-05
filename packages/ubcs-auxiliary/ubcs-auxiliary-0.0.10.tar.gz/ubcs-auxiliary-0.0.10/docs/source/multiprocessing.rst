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
>>> def function(N, **kwargs):
      """
      an example function for test purposes. It sleeps for N seconds. Prints statements when sleep starts and finishes.
      """
      from time import time, sleep
      import os
      print_text_kwarg(**kwargs)
      print_dict_kwarg(**kwargs)
      print_var_kwarg(**kwargs)
      print('Starting Process: pid: {}'.format(os.getpid()))
      t1 = time()
      print('[{} s] Start sleeping for {} seconds'.format(round(time()-t1,4),N))
      print('[{} s] Sleeping... '.format(round(time()-t1,4)))
      sleep(N)
      print('[{} s] Done sleeping for {} seconds'.format(round(time()-t1,4),N))
>>> kwargs = {'text': 'my new text', 'var' : 15.64, 'dict' : {'key':'my new value'}}
>>> mp = MultiProcessing(function, (1,2,3), kwargs = kwargs)
kwarg text = my new text
kwarg dict = {'key': 'my new value'}
kwarg var = 15.64
Starting Process: pid: 14789
[0.0 s] Start sleeping for 1 seconds
[0.0002 s] Sleeping...
kwarg text = my new text
kwarg dict = {'key': 'my new value'}
kwarg var = 15.64
Starting Process: pid: 14790
[0.0 s] Start sleeping for 2 seconds
[0.0 s] Sleeping...
kwarg text = my new text
kwarg dict = {'key': 'my new value'}
kwarg var = 15.64
Starting Process: pid: 14792
[0.0 s] Start sleeping for 3 seconds
[0.0 s] Sleeping...
In [3]: [1.0013 s] Done sleeping for 1 seconds
[2.0001 s] Done sleeping for 2 seconds
[3.0002 s] Done sleeping for 3 seconds

  Or you can import

>>> from ubcs_auxiliary.multi_processing import MultiProcessing, test, function
>>> test()
kwarg text = my new text
kwarg dict = {'key': 'my new value'}
kwarg var = 15.64
Starting Process: pid: 14789
[0.0 s] Start sleeping for 1 seconds
[0.0002 s] Sleeping...
kwarg text = my new text
kwarg dict = {'key': 'my new value'}
kwarg var = 15.64
Starting Process: pid: 14790
[0.0 s] Start sleeping for 2 seconds
[0.0 s] Sleeping...
kwarg text = my new text
kwarg dict = {'key': 'my new value'}
kwarg var = 15.64
Starting Process: pid: 14792
[0.0 s] Start sleeping for 3 seconds
[0.0 s] Sleeping...
In [3]: [1.0013 s] Done sleeping for 1 seconds
[2.0001 s] Done sleeping for 2 seconds
[3.0002 s] Done sleeping for 3 seconds

.. autoclass:: ubcs_auxiliary.multi_processing.MultiProcessing
  :members:

  .. automethod:: __init__

.. automodule:: ubcs_auxiliary.multi_processing
  :members:
