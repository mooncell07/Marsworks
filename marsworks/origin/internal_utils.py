import inspect

__all__ = ("repr_gen",)


def repr_gen(cls, obj) -> str:
    """
    Forms a repr for obj.
    """
    attrs = [
        attr
        for attr in inspect.getmembers(obj)
        if not inspect.ismethod(attr[1])
        if not attr[0].startswith("_")
    ]
    fmt = ", ".join(f"{attr}={repr(value)}" for attr, value in attrs)
    return f"{cls.__name__}({fmt})"
