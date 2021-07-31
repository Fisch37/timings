from typing import Callable
from time import perf_counter
from inspect import signature, getfullargspec

class StoppedException(Exception):
    """Raised when an Interval was stopped, but update was called"""

class StartedException(Exception):
    """Raised when a Timeout or an Interval was supposed to be started, but it already is"""

class ArgumentError(Exception):
    """Raised when a callback function does not receive the proper arguments for execution"""

def __checkValidity__(func,*args,**kwargs):
    sig = signature(func)
    try:
        sig.bind(*args,**kwargs) # Try to match args to function, if fails raise TypeError
    except TypeError:
        return False
        pass
    finally:
        return True
    pass

class Timeout:
    """
    Executes a function after a given number of seconds.
    Note: Timeout.update has to be called a lot of times for that to work
    
    To start the clock, simply execute Timeout.start or set the startImmediately flag at creation.
    To use a Timeout object again, call Timeout.reset and then Timeout.start or just Timeout.restart
    """
    def __init__(self, callback : Callable, delay : float,startImmediately : bool = False,*args,**kwargs):
        if not __checkValidity__(callback,*args,**kwargs):
            raise ArgumentError(f"Timeout object did not receive proper arguments for {callback}:\nArgs: {args}\nKwargs: {kwargs}")
            return
        argspec = getfullargspec(callback)
        self.__no_args = argspec.varargs is None and len(argspec.args) == 0

        self.__delay = delay

        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs

        self.__start = None
        self.__done = False
        if startImmediately:
            self.start()
        pass

    def start(self):
        """
        Starts the Timeout object.\n
        If the object was already started, this will raise a `StartedException`.
        """
        if self.__start is not None:
            raise StartedException("This Timeout object was already started")
        self.__start = perf_counter()
        pass

    def reset(self):
        """
        Resets the Timeout object, so that it may run again.
        """
        self.__start = None
        self.__done = False

    def restart(self):
        """
        Resets the Timeout object and also starts it immediately.
        """
        self.reset()
        self.start()
        lambda: print("HI")

    def update(self):
        """
        Updates the object's inner clock.\n
        This will run fine if the Timeout is done or hasn't started yet, but doing so is not encouraged.
        """
        if self.__start is None or self.__done: return
        if (perf_counter() - self.__start) > self.__delay:
            if self.__no_args: self.__callback()
            else: self.__callback(*self.__args,**self.__kwargs)
            self.__done = True
            pass
        pass

    def is_done(self):
        return self.__done
    pass

class Interval:
    """
    Executes a function repeatedly every given number of seconds.\n\n
    
    To start the Interval simply execute Interval.start or set the startImmediately argument.\n
    If you want to stop the Interval, use the Interval.stop function.
    """
    def __init__(self,callback : Callable, interval : float, startImmediately : bool = False,*args, **kwargs):
        self.timeout = Timeout(callback,interval,startImmediately,args=args,kwargs=kwargs)
        self.__running = startImmediately
        pass
    
    def update(self):
        """
        Updates the Interval's timer.\n
        If the Interval object was stopped, this will raise a `StoppedException`
        """
        if not hasattr(self,"timeout"):
            raise StoppedException("This Interval object has been stopped")
        if self.timeout.is_done(): self.timeout.restart()
        self.timeout.update()
        pass

    def start(self):
        """
        Starts the Interval object.\n
        May also be called when the Interval object was stopped before.
        """
        if self.__running: raise StartedException("This Interval object was already started")
        self.timeout.start()
        pass
    
    def stop(self):
        """
        Stops the Interval object.\n
        If the object was already stopped, this will raise a `StoppedException`.
        """
        if not hasattr(self,"timeout"):
            raise StoppedException("This Interval was already stopped")
        del self.timeout
        self.__running = False
        pass

    def is_running(self):
        return self.__running
        pass


__DISREGARD_PLEASE__ = 0
def __disregardMe__():
    global __DISREGARD_PLEASE__
    __DISREGARD_PLEASE__ += 1
    print(f"This is the {__DISREGARD_PLEASE__}. time, this has been run!")

def __main__():
    from time import sleep
    print("Demonstrating Timeout:")
    timeout = Timeout(lambda a,b: print("These are a and b:",a,b),1,True,5,7) # Calling lambda with arguments 5 and 7 in 1 second, starting now
    while not timeout.is_done():
        timeout.update()
        pass
    print("Timeout complete!")
    del timeout
    sleep(1)
    print("Demonstrating Interval")
    interval = Interval(__disregardMe__,0.5,False)
    print("Interval starting in 1 second")
    sleep(1)
    interval.start()
    print("Interval will finish after ten messages!")
    while __DISREGARD_PLEASE__ < 10:
        interval.update()
        pass
    interval.stop()
    del interval
    print("Interval has finished!")
    pass

if __name__=="__main__":
    __main__()
    pass