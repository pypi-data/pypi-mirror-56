class ParallelProcessing():
    def __init__(self, function, args, **kwargs):
        """
        This is a specialized wrapper around multiprocessing.Process object. It
        launches multiple separate processes with the same input 'function' but different argument that comes from an iterable object like tuple or list.

        Parameters
        ----------
        function :: function
            function object
        args :: list or tuple
            iterable of arguments
        kwargs :: dictionary
            keyword arguments that will be passed to the function

        Returns
        -------
        jobs :: list
            list of jobs

        Examples
        --------
        >>> mp = ParallelProcessing(function, (1,2,3))
        """
        from multiprocessing import Process
        print(args,kwargs)
        self.jobs = []
        for arg in args:
            p = Process(target=function,args=(arg,), **kwargs)
            p.start()
            self.jobs.append(p)

class MultiProcessing():
    def __init__(self, function, args, **kwargs):
        parallel_processing = ParallelProcessing(function, args, **kwargs)
        self.jobs = parallel_processing.jobs
        self.deprecation_warning()

    def deprecation_warning(self):
        import warnings
        warnings.warn("MultuProcessing class will be deprecated in future versions. The new name is ParallelProcessing", DeprecationWarning)


def function(N, **kwargs):
    """
    an example function for test purposes. It sleeps for N seconds. Prints statements when sleep starts and finishes.
    """
    from time import time, sleep

    print_text_kwarg(**kwargs)
    print_dict_kwarg(**kwargs)
    print_var_kwarg(**kwargs)

    print('Starting Process')
    t1 = time()
    print('[{} s] Start sleeping for {} seconds'.format(round(time()-t1,4),N))
    print('[{} s] Sleeping... '.format(round(time()-t1,4)))
    sleep(N)
    print('[{} s] Done sleeping for {} seconds'.format(round(time()-t1,4),N))

def print_text_kwarg(**kwargs):
    print(f"kwarg text = {kwargs['text']}")
def print_dict_kwarg(**kwargs):
    print(f"kwarg dict = {kwargs['dict']}")
def print_var_kwarg(**kwargs):
    print(f"kwarg var = {kwargs['var']}")

def test():
    """
    simple test showing how to use
    """
    kwargs = {'text': 'my new text', 'var' : 15.64, 'dict' : {'key':'my new value'}}
    mp = MultiProcessing(function, args = (1,2,3), kwargs = kwargs)

def test2():
    """
    simple test showing how to use
    """
    kwargs = {'text': 'my new text', 'var' : 15.64, 'dict' : {'key':'my new value'}}
    mp = ParallelProcessing(function, args = (1,2,3), kwargs = kwargs)
