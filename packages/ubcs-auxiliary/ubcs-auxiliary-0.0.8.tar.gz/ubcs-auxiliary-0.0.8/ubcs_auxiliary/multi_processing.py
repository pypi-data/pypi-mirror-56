class MultiProcessing():
    def __init__(self,function,args):
        """
        launches the input 'function' in a separate process. the args atribute has to be itterable. The class will initiate as many processes as itterables in the args.

        Parameters
        ----------
        function:
            function object
        *args:
            iterable of arguments

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
        self.jobs = []
        for arg in args:
            p = multiprocessing.Process(target=function,args=(arg,))
            p.start()
            self.jobs.append(p)

def function(N):
    """
    an example function for test purposes. It sleeps for N seconds. Prints statements when sleep starts and finishes.
    """
    from time import time, sleep
    import os
    print('Starting Process: pid: {}'.format(os.getpid()))
    t1 = time()
    print('[{} s] Start sleeping for {} seconds'.format(round(time()-t1,4),N))
    print('[{} s] Sleeping... '.format(round(time()-t1,4)))
    sleep(N)
    print('[{} s] Done sleeping for {} seconds'.format(round(time()-t1,4),N))

def test():
    """
    simple test showing how to use
    """
    mp = MultiProcessing(function,(1,2,3))
