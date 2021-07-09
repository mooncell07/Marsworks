import inspect
from functools import wraps

from marsworks.origin.exceptions import BadArgumentError

__all__ = ("ensure_type",)


def ensure_type(func):  # Will enhance later
    @wraps(func)
    def inner(*args, **kwargs):
        annos = func.__annotations__
        if isinstance(args[1], list(annos.values())[0]):
            if inspect.iscoroutinefunction(func):

                async def funcrun():
                    return await func(*args, **kwargs)

                return funcrun()

            else:
                return func(*args, **kwargs)
        else:
            raise BadArgumentError(
                f"Bad args passed for {list(annos)[0]}. Please check typehints."
            )

    return inner
