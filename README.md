# timings
Provides a few utilities for async* code execution

*not actually async in terms of the asyncio library, but waiting before execution in a way that won't halt your current thread or pause the program in any way


## basics
### Timeout
To use the `Timeout` class you need only a few things: A callable (like a definition or lambda) and a time to wait.

When you want to start the timeout simply use `Timeout.start()`.
At this point you probably want to have some sort of main loop, as you will have to call `Timeout.update()` continuosly.
When the timeout is completed and the callable executed, `Timeout.is_done()` will return `True`.
While it does not harm the process, it is still not recommended to update a completed timeout.

To reuse a Timeout object, use `Timeout.reset()` and `Timeout.restart()`. 
The former will configure the object so that it may be executed again, while the latter implements the former with `Timeout.start()`
