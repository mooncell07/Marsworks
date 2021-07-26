from collections import namedtuple
from typing import Callable, Generator, Iterable

__all__ = ("lookup", "mw_pageit")


def lookup(predicate: Callable, iterable: Iterable) -> list:
    """
    Performs a lookup over the iterable and returns everything
    which meets the predicate.

    Args:
        predicate: The callable which must be called on all elements of iterable.
        iterable: The iterable.

    Returns:
        All the elemets which meet the predicate.

    Examples:
        ```py
        print(lookup(lambda p: p.camera_id == 30, listofphotos))
        ```

    *Introduced in [v0.4.0](../changelog.md#v040).*
    """
    return [i for i in iterable if predicate(i)]


def mw_pageit(mwlist: list, per_page: int, no_of_pages: int) -> Generator:
    """
    Divides the `mwlist` into `per_page` number of namedtuple `Page`s.

    Args:
        mwlist: The list to be divided into pages.
        per_page: The number of items per page.
        no_of_pages: Number of pages to return.

    Returns:
        A generator of `Page`s.

    *Introduced in [v0.4.0](../changelog.md#v040).*
    """
    ntuple = namedtuple("Page", ["pages"])
    yield from [
        ntuple(mwlist[i : i + per_page])  # noqa: E203
        for i in range(0, len(mwlist), per_page)
    ][0:no_of_pages]
