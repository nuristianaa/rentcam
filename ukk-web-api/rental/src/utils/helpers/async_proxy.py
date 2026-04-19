import asyncio
from typing import Any, Coroutine

def run_async(coro: Coroutine) -> Any:
    """
    Run an async coroutine from a synchronous context.
    Safely handles cases where an event loop is already running.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        # This is the tricky part in FastAPI (running in a thread pool)
        # We can create a new event loop just for this thread
        new_loop = asyncio.new_event_loop()
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()
    else:
        return loop.run_until_complete(coro)
