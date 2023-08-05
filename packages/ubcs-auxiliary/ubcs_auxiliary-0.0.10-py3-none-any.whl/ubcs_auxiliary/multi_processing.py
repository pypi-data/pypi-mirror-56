class MultiProcessing():
    def __init__(self, function, args, **kwargs):
        """
        launches the input 'function' in a separate process. the args atribute
        has to be itterable. The class will initiate as many processes as itterables in the args.

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
        >>> mp = MultiProcessing(function, (1,2,3))
        """
        import multiprocessing
        import os
        print(args,kwargs)
        self.jobs = []
        for arg in args:
            p = multiprocessing.Process(target=function,args=(arg,), **kwargs)
            p.start()
            self.jobs.append(p)

def function(N, **kwargs):
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
